from NEAT.Networking.Client.SimulationClient import SimulationClient
import time

cli = SimulationClient("127.0.0.1", 8081)

print(">> Announcing session...")
cli.announce_session(
    "testSession5",
    "./NEAT/Config",
    1
)

for i in range(10):

    print(">> Getting block...")
    block = cli.get_block(i)
    print(">> Got block: ", block)

    for genome, inputs in block.items():
        for input in inputs:
            block[genome][input] = 0.5

    print(">> Setting inputs...")
    cli.set_block_inputs(block, i)

    print(">> Getting outputs...")
    outputs = cli.get_block_outputs(i)
    print(">> Got outputs: ", outputs)

    fitness_values = {
        genome: 0.0 for genome in block.keys()
    }
    print(">> Setting fitness values")
    cli.set_fitness_values(fitness_values, i)

cli.archive_session()
