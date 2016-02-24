from NEAT.Director.Director import Director


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
        self.simulation_name = kwargs.get('simulation')

        # used for running simulation and calculating fitness for a given genome
        self.simulation_runner = NEAT.Director.SimulationRunner(self.simulation_name)
        #   checks if simulation exists, raises exception if not
        #   checks if simulation is compatible, raises exception if not
        #   checks if simulation is configured, raises exception if not
        #   loads configuration from config file inside simulation

        # class containing huge configuration object, potentially just json no-
        # tation
        # should contain:
        # - selection_parameters
        # - decision_making_parameters (contains e.g. max population size)
        # - clustering_parameters
        # - discarding_parameters
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
        # analyst analyzes a given genome and creates an AnalysisResult based on
        # it
        self.analyst = NEAT.Analyst.GenomeAnalyst()
        # clusterer divides all existing and active genomes in clusters aka spe-
        # cies
        self.clusterer = NEAT.Analyst.GenomeClusterer(
            self.genome_repository,
            self.config.clustering_parameters
        )

    def run(self):
        pass
        # on new, creates new database
        # loads database

        # on new, creates random set of genomes based on configuration inside
        # Simulation.given_simulation.config

        while True:
            if self.decision_maker.inter_cluster_breeding_time:
                # if it's time to cross-breed, first discard a few clusters
                self.discard_genomes(clusters=True)
                # then combine clusters
                self.crossbreed_clusters()
                # and cluster again
                self.cluster_genomes()
            else:
                # if it's incest time, first discard a few genomes
                self.discard_genomes()
                # then refill the population
                # genomes that are generated in this phase will belong to the
                # cluster to which its parents belong.
                while not self.decision_maker.population_at_maximum_size():
                    self.generate_new_genome(mode=self.decision_maker.breed_or_mutate())

    def generate_new_genome(self, mode, genome=None, genome_two=None):
        """
        generates a new genome via mutation/breeding
        then analyzes, simulates and stores the new genome
        needs further parameterization
        :param genome_two:
        :param genome:
        :param mode: breed or mutate?
        :return:
        """
        if mode == 'breed':
            if genome is None or genome_two is None:
                genome, genome_two = self.selector.select_genomes_for_breeding()
            new_genome = self.breeder.breed_genomes(genome, genome_two)
        elif mode == 'mutate':
            if genome is None:
                genome = self.selector.select_genome_for_mutation()
            new_genome = self.mutator.mutate_genome(genome)
        else:
            return
        analysis_result = self.analyst.analyze_genome(new_genome)
        new_genome.analysis_result = analysis_result
        new_genome.cluster = genome.cluster
        self.genome_repository.add_genome(new_genome)

    def crossbreed_clusters(self):
        """
        combinates two clusters
        :return:
        """
        cluster_one, cluster_two = self.selector.select_clusters_for_combination()
        for genome_one, genome_two in self.selector.select_cluster_combinations(cluster_one, cluster_two):
            self.generate_new_genome(mode='breed', genome=genome_one, genome_two=genome_two)
        # now interbreed cluster_one and cluster_two

    def cluster_genomes(self):
        """
        clusters all currently stored genomes
        :return:
        """
        self.clusterer.cluster_genomes()
        pass

    def discard_genomes(self, clusters=False):
        """
        discards a number of genomes
        :param clusters: True, if the lowest X clusters should be discarded,
                         False, if the lowest X% of genomes should be discarded
        :return:
        """
        if clusters:
            for cluster in self.decision_maker.select_clusters_for_discarding():
                self.genome_repository.discard_genomes_by_cluster(cluster)
        else:
            for genome in self.decision_maker.select_genomes_for_discarding():
                self.genome_repository.discard_genome(genome)
