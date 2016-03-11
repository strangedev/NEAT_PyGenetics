from NEAT.Director.Director import Director
from NEAT.Config.NEATConfig import NEATConfig
from NEAT.Networking.Server.SimulationClient import SimulationClient
from NEAT.ErrorHandling.StartupCheck import StartupCheck
from NEAT.ErrorHandling.Exceptions.NetworkProtocolException import NetworkProtocolException
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
from bson import ObjectId
from typing import Dict


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
        self.mode = kwargs.get('mode', 'exit')
        if self.mode == 'exit':
            exit()
        elif self.mode == 'run_server':

            startup_check = StartupCheck()
            startup_check.run()

            self.static_init()

            while True:
                try:
                    self.idle()
                except NetworkProtocolException as e:
                    print(e)
                    pass

    def static_init(self):
        """
        Initializes all parts of NEAT that are not dependent
        upon the client.
        """
        # An interface to a client connected via the REST API.
        self.simulation_client = SimulationClient()

        # Used to keep track of the number of discarded
        # genomes when clusters are discarded.
        self._discarded_genomes_count = 0

    def dynamic_init(self):
        """
        Initializes all parts of NEAT that are dependent upon
        the client.
        """

        self.init_db()

        # Class containing huge configuration object.
        # Loads config from JSON or uses default config.
        self.config = NEATConfig(self._config_path)

        # selecting can mean:
        #   - selecting a single genome for mutation
        #   - selecting two genomes for breeding
        #   - selecting two clusters for combination
        #   - selecting two genomes from two given clusters for inter cluster
        #    breeding (since we don't really want to create ALL combinations)
        self.selector = GenomeSelector(
            self.genome_repository,
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

    def init_db(self, archive_existing_db=False):

        # database connection is a connection to an arbitrary database that is
        # used to store genes, genomes and nodes
        self.database_connection = DatabaseConnector(
            self.simulation_client.session.token
        )

        # gene_repository administrates all genes ever created
        self.gene_repository = GeneRepository(
            self.database_connection
        )
        # genome_repository administrates all genomes ever created
        self.genome_repository = GenomeRepository(
            self.database_connection
        )
        # cluster_repository administrates all clusters ever created
        self.cluster_repository = ClusterRepository(
            self.database_connection
        )

    def idle(self):
        """
        Standard method that will be executed if local startup is done.
        In this state, the Director will wait for the client.
        """

        self.simulation_client.wait_for_session()
        self._config_path = self.simulation_client.get_config_path()

        # Session tokens will identify a client.
        # They can be useful for later parallelization.
        # They also identify the database collections which will be used,
        # so that different users can have their own storage and previous
        # sessions can be loaded from storage.

        self.dynamic_init() # This can be called after the client has connected

        # In case of simulation run:
        self.run()

    def run(self):
        """
        The main function where the simulation is run, new
        genomes are created and discarded
        This is where the evolutionary magic happens.
        """
        self.decision_maker.reset_time()

        # on new, creates random set of genomes based on configuration inside
        # Simulation.given_simulation.config
        self._block_size = self.simulation_client.get_block_size()
        self.perform_simulation_setup()

        # TODO: Init population if necessary

        while True:

            ### 1. Simulation / wait for client
            advance_generation = self.perform_simulation_io()

            # Either:
            #   * go on with loop, generate next generation
            #   * save database for later use, hand out session id to client
            if not advance_generation:
                return # TODO: archive session


            ### 2. Calculate offspring values

            self.calculate_cluster_offspring()

            ### 3. Discarding / Regeneration

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

            ### 4. Advance time

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
        genome.cluster = self.clusterer.cluster_genome(genome)
        self.genome_repository.insert_genome(genome)

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
            self.genome_repository.discard_genome(genome)

    def discard_clusters(self):
        """
        Discards a number of clusters
        :return:
        """
        for cluster in self.selector.select_clusters_for_discarding():
            genomes_to_discard = self.genome_repository.get_genomes_in_cluster(cluster._id)
            self._discarded_genomes_count += len(list(genomes_to_discard))
            self.genome_repository.discard_genomes_by_cluster(cluster)

    def perform_simulation_setup(self):
        pass

    def perform_simulation_io(self):
        genomes = list(self.genome_repository.get_current_population())
        block_count = math.ceil(len(genomes) / self._block_size)
        genome_index = 0

        for block_id in range(block_count):
            block = genomes[genome_index : genome_index + self._block_size]
            self.simulation_client.send_block(block, block_id)
            block_inputs = self.simulation_client.get_block_inputs(block_id)
            self.simulation_client.send_block_outputs(
                self.compute_genome_output(block_inputs),
                block_id
            )
            self.update_fitness_values(
                self.simulation_client.get_fitness_values(block_id)
            )
            genome_index += self._block_size

        return self.simulation_client.get_advance_generation()

    def compute_genome_output(
            self,
            block_inputs: Dict[ObjectId, Dict[str, float]]
    ) -> Dict[ObjectId, Dict[str, float]]:
        pass # TODO:

    def update_fitness_values(
            self,
            fitness_values: Dict[ObjectId, float]
    ) -> None:
        pass # TODO: