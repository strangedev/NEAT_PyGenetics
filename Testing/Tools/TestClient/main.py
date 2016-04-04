from NEAT.Networking.Client.SimulationClient import SimulationClient

cli = SimulationClient("127.0.0.1", 8081)
cli.announce_session(
    "testSession",
    "/home/strangedev/Dokumente/NEAT_PyGenetics/NEAT/Config",
    1
)
block = cli.get_block(0)
print(block)
exit()
for genome in block:
    pass