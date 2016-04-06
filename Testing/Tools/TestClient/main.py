from NEAT.Networking.Client.SimulationClient import SimulationClient
import time

cli = SimulationClient("127.0.0.1", 8081)
cli.announce_session(
    "testSession2",
    "/home/strangedev/Dokumente/NEAT_PyGenetics/NEAT/Config",
    1
)
block = cli.get_block(0)
print(block)

for genome, inputs in block.items():
    for input in inputs:
        block[genome][input] = 0.5
time.sleep(1)
cli.set_block_inputs(block, 0)

