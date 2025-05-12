import json

def json_to_dot(input_json_file, output_dot_file):
    with open(input_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    semantic_triples = data.get("semantic_triples", [])
    internal_link_triples = data.get("internal_link_triples", [])

    nodes = {}
    edges = []

    for head, relation, tail in semantic_triples:

        if head not in nodes:
            nodes[head] = 'non-leaf'

        if tail not in nodes:
            nodes[tail] = 'leaf'

        edges.append((head, relation, tail))

    for head, relation, tail in internal_link_triples:

        if head not in nodes:
            nodes[head] = 'non-leaf'

        if tail not in nodes:
            nodes[tail] = 'non-leaf'

        edges.append((head, relation, tail))

    with open(output_dot_file, 'w', encoding='utf-8') as f:
        f.write('digraph n0 {\n')
        f.write('fontcolor="blue"\nremincross="true"\n')
        f.write('subgraph cluster {\nlabel="model"\n')

        for node, node_type in nodes.items():
            if node_type == 'leaf':
                f.write(f'"{node}"[shape="plaintext",style="filled",fillcolor="gold",label="{node}"];\n')
            else:
                f.write(f'"{node}"[style="filled",color="white",fillcolor="lightgray",label="{node}"];\n')

        f.write('}\n')

        for head, relation, tail in edges:
            f.write(f'"{head}" -> "{tail}"[color="brown",fontcolor="black",label="{relation}"];\n')
        
        f.write('}\n')

input_json_file = ''
output_dot_file = ''
json_to_dot(input_json_file, output_dot_file)
