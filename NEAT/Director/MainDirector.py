class MainDirector(object):
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
        self.simulation_name = kwargs.get('simulation')

        # used for running simulation and calculating fitness for a given genome
        self.simulation_runner = NEAT.Director.SimulationRunner(self.simulation_name)
        #   checks if simulation exists, raises exception if not
        #   checks if simulation is compatible, raises exception if not
        #   checks if simulation is configured, raises exception if not

        # class containing huge configuration object, potentially just json no-
        # tation
        self.config = NEAT.config

        # database connection is a connection to an arbitrary database that is
        # used to store genes, genomes and nodes
        self.database_connection = NEAT.Repository.DatabaseConnector(
            self.simulation_name
        )
        # gene_repository administrates all genes ever created
        self.gene_repository = NEAT.Repository.GeneRepository(
            self.database_connection
        )
        # genome_repository administrates all genomes ever created
        self.genome_repository = NEAT.Repository.GenomeRepository(
            self.database_connection,
            self.gene_repository
        )
        self.node_repository = NEAT.Repository.NodeRepository(
            self.database_connection
        )

        # selector selects genes and is parameterized by a global config
        # selecting can mean:
        #   - selecting a single genome for mutation
        #   - selecting two genomes for breeding
        #   - selecting two clusters for combination
        #   - selecting two genomes from two given clusters for inter cluster
        #    breeding (since we don't really want to create ALL combinations)
        self.selector = NEAT.Analyst.GenomeSelector(
            self.genome_repository,
            self.config.selection_parameters
        )
        # makes decisions lol
        # things like what to do and stuff (breeding or mutation, if clustering
        # is necessary etc)
        self.decision_maker = NEAT.Analyst.DecisionMaker(
            self.genome_repository,
            self.config.decision_making_parameters
        )
        # breeder creates a new genome from two given genomes
        # it needs the gene_repository to register new genes and to look up used
        # ones
        self.breeder = NEAT.Generator.Breeder(
            self.gene_repository
        )
        # mutator creates a new genome from a given genome
        # it needs the gene_repository to register new genes and to look up used
        # ones
        self.mutator = NEAT.Generator.Mutator(
            self.genome_repository
        )
        # clusterer divides all existing and active genomes in clusters aka spe-
        # cies
        self.clusterer = NEAT.Analyst.GenomeClusterer(
            self.genome_repository
        )

    def run(self):
        pass
        # on new, creates new database
        # loads database

        # on new, creates random set of genomes based on configuration inside
        # Simulation.given_simulation.config

        while True:
            if self.genome_repository.population_size > self.config.max_population_size:
                self.discard_phase()

            if self.decision_maker.inter_cluster_breeding_time():
                cluster_one, cluster_two = self.selector.select_clusters_for_combination()
                self.combination_phase(cluster_one, cluster_two)
            else:
                while not self.decision_maker.is_cluster_time():
                    self.generation_phase(self.decision_maker.breed_or_mutate())

            self.cluster_phase()

    def generation_phase(self, mode):
        """
        generates a new genome via mutation/breeding
        then analyzes, simulates and stores the new genome
        needs further parameterization
        :param mode: breed or mutate?
        :return:
        """
        pass

    def combination_phase(self, cluester_one, cluster_two):
        """
        combinates two clusters
        :return:
        """
        pass

    def cluster_phase(self):
        """
        clusters all currently stored genomes
        :return:
        """
        pass

    def discard_phase(self):
        """
        discards a number of genomes
        :return:
        """
        pass
