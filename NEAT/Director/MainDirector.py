from NEAT.Director.Director import Director
from NEAT.Config.NEATConfig import NEATConfig
from NEAT.Simulator.Simulator import Simulator
from NEAT.Networking.Server.SimulationConnector import SimulationConnector
from NEAT.ErrorHandling.StartupCheck import StartupCheck
from NEAT.ErrorHandling.Exceptions.NetworkProtocolException import NetworkProtocolException
from NEAT.ErrorHandling.Exceptions.NetworkTimeoutException import NetworkTimeoutException
from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.Repository.ClusterRepository import ClusterRepository
from NEAT.Repository.GeneRepository import GeneRepository
from NEAT.Decisions.DecisionMaker import DecisionMaker
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.GenomeStructures.AnalysisStructure.AnalysisGenome import AnalysisGenome
from NEAT.Generator.Breeder import Breeder
from NEAT.Generator.Mutator import Mutator
from NEAT.Analyst.GenomeAnalyst import GenomeAnalyst
from NEAT.Analyst.GenomeClusterer import GenomeClusterer
from NEAT.Analyst.GenomeSelector import GenomeSelector
import math
from bson.objectid import ObjectId
from typing import Dict
import itertools


class MainDirector(Director):
    def __init__(self, **kwargs):
        """
        :param kwargs:
            - mode:
                - exit: exits the program, default action if nothing is provided.
                - new: creates a new database for a given simulation. requires parame-
                 ter simulation to be set.
                - load: loads a database for a given simulation. requires parameter
                 simulation to be set.
            - simulation: the name of the simulation that should be used. must cor-
              respond to a module name in Simulation.
        :return:
        """
        self._maximum_timeouts = 5000
        self.mode = kwargs.get('mode', 'exit')
        self.selector = None  # type: GenomeSelector
        self.decision_maker = None  # type: DecisionMaker
        self.breeder = None  # type: Breeder
        self.mutator = None  # type: Mutator
        self.analyst = None  # type: GenomeAnalyst
        self.clusterer = None  # type: GenomeClusterer
        self.simulator = None  # type: Simulator
        self.simulation_connector = SimulationConnector()  # type: SimulationConnector
        self.database_connector = None  # type: DatabaseConnector
        self.gene_repository = None  # type: GeneRepository
        self.genome_repository = None  # type: GenomeRepository
        self.cluster_repository = None  # type: ClusterRepository
        self.config = None  # type: NEATConfig
        self._session = None  # type: dict
        self._discarded_genomes_count = 0  # type: int

        if self.mode == 'exit':
            exit()
        elif self.mode == 'run_server':

            startup_check = StartupCheck()
            startup_check.run()

            while True:
                try:
                    self.idle()  # TODO: exit command
                except NetworkProtocolException as e:
                    print(e)
                    pass

    def idle(self):
        """
        Standard method that will be executed if local startup is done.
        In this state, the Director will wait for the client.
        """

        self._session = self.simulation_connector.get_session()

        # Session tokens will identify a client.
        # They can be useful for later parallelization.
        # They also identify the database collections which will be used,
        # so that different users can have their own storage and previous
        # sessions can be loaded from storage.

        self.dynamic_init()  # This can be called after the client has connected

        # In case of simulation run:
        self.run()

    def dynamic_init(self):
        """
        Initializes all parts of NEAT that are dependent upon
        the client.
        """

        self.init_db()

        # Class containing huge configuration object.
        # Loads config from JSON or uses default config.
        self.config = NEATConfig(self._session["config_path"])

        # selecting can mean:
        #   - selecting a single genome for mutation
        #   - selecting two genomes for breeding
        #   - selecting two clusters for combination
        #   - selecting two genomes from two given clusters for inter cluster
        #    breeding (since we don't really want to create ALL combinations)
        self.selector = GenomeSelector(
            self.genome_repository,
            self.cluster_repository,
            self.config.parameters["selection"]
        )
        # makes decisions lol
        # things like what to do and stuff (breeding or mutation, if clustering
        # is necessary etc)
        self.decision_maker = DecisionMaker(
            self.config.parameters["decision_making"]
        )
        # breeder creates a new genome from two given genomes
        # it needs the gene_repository to register new genes and to look up used
        # ones
        self.breeder = Breeder(
            self.config.parameters["breeding"]
        )
        # Mutator creates a new genome from a given genome
        # it needs the gene_repository to register new genes and to look up used
        # ones
        self.mutator = Mutator(
            self.genome_repository,
            self.config.parameters["mutating"]
        )
        # Analyst analyzes a given genome and creates an AnalysisResult based on
        # it
        self.analyst = GenomeAnalyst()
        # clusterer divides all existing and active genomes in clusters aka spe-
        # cies
        self.clusterer = GenomeClusterer(
            self.genome_repository,
            self.cluster_repository,
            self.config.parameters["clustering"]
        )

        self.simulator = Simulator(self.gene_repository)

    def init_db(self):

        # database connection is a connection to an arbitrary database that is
        # used to store genes, genomes and nodes
        self.database_connector = DatabaseConnector(
            self._session["session_id"]
        )

        # gene_repository administrates all genes ever created
        self.gene_repository = GeneRepository(
            self.database_connector
        )
        # genome_repository administrates all genomes ever created
        self.genome_repository = GenomeRepository(
            self.database_connector
        )
        # cluster_repository administrates all clusters ever created
        self.cluster_repository = ClusterRepository(
            self.database_connector
        )

    def run(self):
        """
        The main function where the simulation is run, new
        genomes are created and discarded
        This is where the evolutionary magic happens.
        """

        # on new, creates random set of genomes based on configuration inside
        # Simulation.given_simulation.config
        self.decision_maker.reset_time()

        # Init population if its not present yet.
        if len(
                list(self.genome_repository.get_current_population())
        ) == 0:
            self.init_population()

        while True:

            # 1. Simulation / wait for client
            timeout_count = 0
            advance_generation = False
            while timeout_count < self._maximum_timeouts:
                try:
                    advance_generation = self.perform_simulation_io()
                except NetworkTimeoutException:
                    # TODO: log timeout event
                    timeout_count += 1
            if not timeout_count < self._maximum_timeouts:
                raise NetworkTimeoutException

            # Either:
            #   * go on with loop, generate next generation
            #   * save database for later use, hand out session id to client
            if not advance_generation:
                exit()  # TODO: archive session

            # 2. Calculate offspring values

            self.calculate_cluster_offspring()

            # 3. Discarding / Regeneration

            if self.decision_maker.inter_cluster_breeding_time:
                # if it's time to cross-breed, first discard a few clusters
                self.discard_clusters()
                # then combine clusters
                self.crossbreed_clusters()
            else:
                # if it's incest time, first discard a few genomes
                self.discard_genomes()
                # then refill the population
                self.generate_new_genomes()

            # 4. Advance time

            self.decision_maker.advance_time()

    def generate_new_genomes(self):
        """
        Regenerates the population by selecting genomes for
        mutation / breeding, running the generation process and performing analysis.
        :return:
        """

        mutation_percentage = self.decision_maker.mutation_percentage
        genomes_for_mutation = self.selector.select_genomes_for_mutation(mutation_percentage)
        genomes_for_breeding = self.selector.select_genomes_for_breeding(1 - mutation_percentage)
        new_genomes = []

        for genome in genomes_for_mutation:
            new_genome = self.mutator.mutate_genome(genome)
            new_genomes.append(new_genome)

        for genome_one, genome_two in genomes_for_breeding:
            new_genome = self.breeder.breed_genomes(
                genome_one,
                genome_two
            )
            new_genomes.append(new_genome)

        for genome in new_genomes:
            self.analyze_and_insert(genome)

    def crossbreed_clusters(self):
        """
        combines two clusters by breeding genomes of both clusters
        :return:
        """
        cluster_one, cluster_two = self.selector.select_clusters_for_combination()
        for genome_one, genome_two in self.selector.select_cluster_combinations(
                cluster_one,
                cluster_two,
                self._discarded_genomes_count
        ):
            new_genome = self.breeder.breed_genomes(genome_one, genome_two)
            self.analyze_and_insert(new_genome)

        self._discarded_genomes_count = 0

    def analyze_and_insert(self, genome: StorageGenome):

        analysis_genome = AnalysisGenome(self.gene_repository, genome)
        analysis_result = self.analyst.analyze(analysis_genome)
        genome.analysis_result = analysis_result
        self.genome_repository.insert_genome(genome)
        self.clusterer.cluster_genome(genome)

    def calculate_cluster_offspring(self):
        """
        Calculates fitness values and offspring for clusters.
        :return:
        """
        self.clusterer.calculate_cluster_offspring_values()

    def discard_genomes(self):
        """
        discards a number of genomes
        :return:
        """
        for genome in self.selector.select_genomes_for_discarding():
            self.genome_repository.disable_genome(genome.genome_id)

    def discard_clusters(self):
        """
        Discards a number of clusters
        :return:
        """
        for cluster in self.selector.select_clusters_for_discarding():
            genomes_to_discard = self.genome_repository.get_genomes_in_cluster(cluster.cluster_id)
            self._discarded_genomes_count += len(list(genomes_to_discard))
            self.genome_repository.disable_genomes([i.genome_id for i in genomes_to_discard])

    def perform_simulation_io(self):
        genomes = list(self.genome_repository.get_current_population())
        block_count = math.ceil(len(genomes) / self._session["block_size"])
        genome_index = 0
        fitness_values = []

        for block_id in range(block_count):

            block = genomes[genome_index: genome_index + self._session["block_size"]]
            self.simulation_connector.send_block(block, block_id)
            block_inputs = self.simulation_connector.get_block_inputs(block_id)
            self.simulation_connector.send_block_outputs(
                self.compute_genome_outputs(block_inputs),
                block_id
            )
            fitness_values.append(
                self.simulation_connector.get_fitness_values(block_id)
            )
            genome_index += self._session["block_size"]

        self.update_fitness_values(
            itertools.chain(*fitness_values)
        )
        return self.simulation_connector.get_advance_generation()

    def compute_genome_outputs(
            self,
            block_inputs: Dict[ObjectId, Dict[str, float]]
    ) -> Dict[ObjectId, Dict[str, float]]:
        results = dict({})
        for genome_id, inputs in block_inputs.items():
            storage_genome = self.genome_repository.get_genome_by_id(genome_id)
            outputs = self.simulator.simulate_genome(storage_genome, inputs)
            results[genome_id] = outputs
        return results

    def update_fitness_values(
            self,
            fitness_values: Dict[ObjectId, float]
    ) -> None:
        for genome_id, fitness_value in fitness_values:
            self.genome_repository.update_genome_fitness(
                genome_id,
                fitness_value
            )

    def init_population(self):
        population_size = self.config.parameters["clustering"]["max_population"]
        input_labels = self.config.parameters["genomes"]["inputs"]
        output_labels = self.config.parameters["genomes"]["outputs"]
        for i in range(population_size):
            genome = StorageGenome(
                inputs=input_labels,
                outputs=output_labels
            )
            self.analyze_and_insert(genome)
