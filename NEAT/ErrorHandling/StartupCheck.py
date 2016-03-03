from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.GenomeRepository import GenomeRepository

class StartupCheck(object):

    def __init__(self):
        self.con = DatabaseConnector("error_check_dummy")
        self.rep = GenomeRepository(self.con)

    def run(self):
        genome = self.rep.get_new_genome()

        try:
            self.rep.insert_genome(genome)
        except Exception as e:
            print("An Error occurred while error checking.")
            print("Error checking occurs while NEATConfig is loading the configuration files.")
            print("\n", e)
            print("\nThis usually means MongoDB isn't running.")

            raise e # TODO: custom error classes!