from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.ErrorHandling.Exceptions.StartupCheckException import StartupCheckException


class StartupCheck(object):

    def __init__(self):
        self.con = DatabaseConnector("error_check_dummy")
        self.rep = GenomeRepository(self.con)

    def run(self):
        genome = self.rep.get_new_genome()
        try:
            self.rep.insert_genome(genome)
        except Exception:
            raise StartupCheckException(
                "Startup check failed. Check if mongoDB is running."
            )
