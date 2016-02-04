from NEAT.Graph import NeuralGraph
from NEAT.Genes import GraphTemplate
from NEAT.Connections import Connection

in_nodes = list(range(0, 9))
out_nodes = ["up", "down", "left", "right"]

temp = GraphTemplate.GraphTemplate(in_nodes, out_nodes)
desc = NeuralGraph.NeuralGraph()
desc.init_from_template(temp)

desc.add_connection(1, "up", 0.5, 1)


print(desc, temp)
print(temp.input_nodes)
print(desc.input_nodes, desc.output_nodes)
print(desc.connections)
print(desc.get_connections(1)[0].weight, desc.get_connections(1)[0].target)
