from bson import ObjectId

from NEAT.Analyst.Cluster import Cluster

class mock_ClusterRepository(object):

    def __init__(self):

        self.clusters = []
        self.next_id = 0

    def reset(self):
        self.__init__()

    def get_cluster_count(self):

        return len(self.clusters)

    def add_cluster_with_representative(self, genome_id: ObjectId):

        cluster = Cluster(ObjectId("00000000000000000000000" + str(self.next_id)), genome_id)
        cluster.fitness = int(str(genome_id))
        self.clusters.append(cluster)
        self.next_id += 1

    def get_current_clusters(self):

        return self.clusters

    def get_cluster_by_representative(self, genome_id: ObjectId):

        for cluster in self.clusters:

            if cluster.representative == genome_id:

                return cluster

    def update_fitness_for_cluster(self, cluster_id: ObjectId, fitness):

        for cluster in self.clusters:

            if cluster._id == cluster_id:

                cluster.fitness = fitness

                break

    def update_max_population_for_cluster(self, cluster_id: ObjectId, max_population):

        for cluster in self.clusters:

            if cluster._id == cluster_id:

                cluster.max_population = max_population

                break

    def update_offspring_for_cluster(self, cluster_id: ObjectId, offspring):

        for cluster in self.clusters:

            if cluster._id == cluster_id:

                cluster.offspring = offspring

                break