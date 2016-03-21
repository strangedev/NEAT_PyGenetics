import json
import os

from NEAT.ErrorHandling.Exceptions.NetworkProtocolException import NetworkProtocolException


class NEATConfig(object):
    """
    A huge configuration object which loads it's parameters
    from disk, or reverts to default values whenever a
    configuration file isn't found or can't be opened.
    Config files are in JSON notation.

    Configuration files are listed in self.config_categories
    and should be present as CATEGORYNAME.conf in the
    provided config_path. If no config path is specified, the builtin
    config files in NEAT/Config are used.

    All config files except one can be loaded from defaults.
    The only exception is genomes.conf, the config file specifying
    the input and output nodes of the genomes to use, because it
    is dependent on the simulation.
    """

    def __init__(self, config_path=None):

        self.parameters = dict({})

        self.config_directory = os.path.dirname(__file__) \
            if not config_path \
            else config_path
        self.working_directory = os.path.join(
            self.config_directory,
            "../../"
        )

        self.config_categories = [
            "clustering",
            "selection",
            "decision_making",
            "breeding",
            "mutating",
            "genomes"
        ]

        self.load_config()

        self.load_defaults()

    def load_config(self):
        """
        Tries to initialize self.parameters with data
        from the configuration files. It uses the base file
        names from self.config_categories and is agnostic to the number
        and names of the existing categories.
        Config files need to be in JSON notation.

        :return: None
        """

        for category in self.config_categories:

            try:
                config_file_path = os.path.join(
                    self.config_directory,
                    ("./" + category + ".conf")
                )
                with open(config_file_path) as config_file:
                    self.parameters[category] = json.loads(
                        config_file.read()
                    )

            except Exception as e:

                print(e, " - loading defaults.")

    def load_defaults(self):
        """
        This method is called by __init__ after the config
        files are loaded. It's job is to test whether the
        config files were loaded by self.load_config() and provide
        the appropriate default values (or crash if there are no defaults)
        for the missing config parameters.

        Because this error-handling method cannot rely on file I/O,
        the defaults are hard-coded.

        :return: None
        """

        if "clustering" not in self.parameters.keys():
            self.parameters["clustering"] = {
                    "delta_threshold": 1,
                    "excess_coefficient": 1,
                    "disjoint_coefficient": 1,
                    "weight_difference_coefficient": 1,
                    "max_population": 10,
                    "discarding_percentage": 0.2
            }
            print("defaults for clustering loaded.")

        if "selection" not in self.parameters.keys():
            self.parameters["selection"] = {
                    "discarding_by_genome_fitness": 0.2,
                    "discarding_by_cluster_fitness": 0.2
            }
            print("defaults for selection loaded.")

        if "decision_making" not in self.parameters.keys():
            self.parameters["decision_making"] = {
                    "todo": "fail"  # TODO:
            }
            print("defaults for decision_making loaded.")

        if "breeding" not in self.parameters.keys():
            self.parameters["breeding"] = {
                    "fitness_difference_threshold": 1,
                    "inherit_randomly_if_same_fitness_probability": 0.5,
                    "gene_inherited_as_disabled_probability": 0.5
                }
            print("defaults for breeding loaded.")

        if "mutating" not in self.parameters.keys():
            self.parameters["mutating"] = {
                    "add_edge_probability": 0.5,
                    "new_gene_enabled_probability": 1,
                    "perturb_gene_weight_probability": 0.5
                }
            print("defaults for mutating loaded.")

        if "genomes" not in self.parameters.keys():
            raise NetworkProtocolException(
                "Genome configuration couldn't be loaded."
            )
