import re
def pretty_print(message):
    print('\n\n'.join('\n'.join(line.strip() for line in re.findall(r'.{1,100}(?:\s+|$)', paragraph.strip('\n'))) for paragraph in re.split(r'\n\n+', message)))

def generate_variable_values(train_data, ontology, test_data):
    VARIABLES = ["Table", "Ontology", "Step1", "Step2"]
    variables = ["$" + i.upper() for i in VARIABLES]
    variable_values = {}
    for variable in variables:
        print("Enter value for variable:", variable)
        if variable == "$TABLE":
            # variable_values[variable] = str(test_data[0]['table'])
            table = ""
            for i, example_data in enumerate(train_data):
                table += f"<Table{i}>\n{example_data['table']}\n</Table{i}>\n"
            variable_values[variable] = table
        if variable == "$STEP1":
            step1 = ""
            for i, example_data in enumerate(train_data):
                step1 += f"<Table{i}>\n<Step1>\n{example_data['semantic_graph']['semantic_triples']}\n</Step1>\n</Table{i}>\n"
            variable_values[variable] = step1
        if variable == "$STEP2":
            step2 = ""
            for i, example_data in enumerate(train_data):
                step2 += f"<Table{i}>\n<Step2>\n{example_data['semantic_graph']['internal_link_triples']}\n</Step2>\n</Table{i}>\n"
            variable_values[variable] = step2
        if variable == "$ONTOLOGY":
            nodes = []
            properties = []
            potential_triples = []
            ontologies = ""
            for node in ontology['Nodes']:
                nodes.append(node)
            for prop in ontology['Properties']:
                properties.append(prop)
            for triples in ontology['Potential triples']:
                potential_triples.append(triples.replace("<", "[").replace(">", "]"))
            ontologies += f"<Class> {nodes}</Class>\n<Property> {properties}</Property>\n<Relation> {potential_triples}</Relation>\n"
            variable_values[variable] = ontologies
    return variable_values

import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def mean_reciprocal_rank(predicted, gold):
    ranks = []
    for item in gold:
        if item in predicted:
            rank = predicted.index(item) + 1
            ranks.append(1 / rank)
    return sum(ranks) / len(gold) if ranks else 0


    from sklearn.metrics import precision_score, recall_score

def calculate_precision_recall(gold_semantics, predicted_semantics):

    # Convert lists to sets for comparison
    gold_set = set(tuple(item) for item in gold_semantics)
    predicted_set = set(tuple(item) for item in predicted_semantics)

    # Calculate true positives, false positives, and false negatives
    true_positives = len(gold_set.intersection(predicted_set))
    false_positives = len(predicted_set - gold_set)
    false_negatives = len(gold_set - predicted_set)
    print(f"Wrong: {str(predicted_set - gold_set)}")
    # print(predicted_set)
    # print(len(list(predicted_set)[0]))
    # print(list(predicted_set)[0])

    # Calculate precision and recall
    if len(predicted_set) == 1 and len(gold_set) == 0 and len(list(predicted_set)[0][0]) == 0:
        precision = 1
        recall = 1
    else:
        precision = true_positives / (len(predicted_set)) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / len(gold_set) if (true_positives + false_negatives) > 0 else 0
    return precision, recall

def find_differences(list1, list2):
    set1 = set(tuple(item) for item in list1)
    set2 = set(tuple(item) for item in list2)
    differences = set1.symmetric_difference(set2)
    return [list(item) for item in differences]

# Load the JSON files

def generate_reason(train_data, ontology, test_data, prompt_path, chain_path1, chain_path2, model):
    with open(prompt_path, "r") as f:
        extracted_prompt_template = f.read()
    variable_values = generate_variable_values(train_data, ontology, test_data)

    prompt_with_variables = extracted_prompt_template
    for variable in variable_values:
        prompt_with_variables = prompt_with_variables.replace("{" + variable + "}", variable_values[variable])
    pre = []
    rec = []
    print_res = ""
    with open(chain_path1, "r") as f:
        chain1 = f.read()
    for i, table in enumerate(test_data):
        prompt_with_variables += "/n" + chain1.replace("$INPUT", str(table['table']))
        promtp = open("prompt_new.txt", "w")
        promtp.write(prompt_with_variables)
        promtp.close()
        messages = [
            {
                "role": "user",
                    "content":  prompt_with_variables
                }
        ]
        message = model.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4096,
                messages= messages,
            )
        # print("Claude's output on your prompt:\n\n")
        # pretty_print(message.choices[0].message.content)
        print_res += message.content[0].text
        messages.append({"role": "assistant", "content": message.content[0].text})
        step1 = message.content[0].text.split("<Step1>")[1].split("</Step1>")[0].strip()
        step1 = [i.replace('\'', '').split(", ")for i in step1[2:-2].split("], [")]
        with open(chain_path2, "r") as f:
            chain2 = f.read()
        messages.append({"role": "user", "content": chain2})
        message = model.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            messages= messages,
        )
        # print("Claude's output on your prompt:\n\n")
        # pretty_print(message.choices[0].message.content)
        print_res += message.content[0].text
        messages.append({"role": "assistant", "content": message.content[0].text})
        all_step2_content = message.content[0].text.split("<Step2>")[1:]
        last_step2 = all_step2_content[-1].split("</Step2>")[0].strip()
        step2 = [i.replace('\'', '').split(", ") for i in last_step2[2:-2].split("],\n[")]
        step2 = [[elem.replace("]'", "']") for elem in inner] for inner in step2]
        step2 = [[elem.replace("'\n[", "['") for elem in inner] for inner in step2]
        with open(f'{i}.txt', 'w') as f:
            f.write(print_res)
        gold_semantics= table['semantic_graph']['internal_link_triples']
        predicted_semantics = step2

        precision, recall = calculate_precision_recall(gold_semantics, predicted_semantics)
        pre.append(precision)
        rec.append(recall)
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
    print(f"Mean Precision: {sum(pre) / len(pre)}")
    print(f"Mean Recall: {sum(rec) / len(rec)}")
