from NEAT.Genes import GeneticDescription
from NEAT.Genes import GeneticTemplate
from NEAT.Connections import Connection

in_nodes = ["u", "d", "l", "r"]
out_nodes = ["u_o", "d_o", "l_o", "r_o"]

temp = GeneticTemplate.GeneticTemplate(in_nodes, out_nodes)
desc = GeneticDescription.GeneticDescription()
desc.init_from_template(temp)

desc.add_connection("u", "u_o", 0.5, 1)


print(desc, temp)
print(temp.input_nodes)
print(desc.input_nodes, desc.output_nodes)
print(desc.connections)
print(desc.get_connections("u")[0].weight, desc.get_connections("u")[0].target)
