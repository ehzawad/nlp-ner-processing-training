import json

# Function to convert labeled words into the desired JSON format
def convert_to_json(labeled_words):
    text = ""
    label = []
    start_index = 0
    entity_start = None
    entity_type = None
    for word, lbl in labeled_words:
        if lbl != "O":
            entity_lbl = lbl.split("-")[1]
            if entity_start is None:
                entity_start = start_index
                entity_type = entity_lbl
            elif entity_lbl != entity_type:
                label.append([entity_start, start_index - 1, entity_type])
                entity_start = start_index
                entity_type = entity_lbl
        elif entity_start is not None:
            label.append([entity_start, start_index - 1, entity_type])
            entity_start = None
            entity_type = None
        
        text += word + " "
        start_index += len(word) + 1

    if entity_start is not None:
        label.append([entity_start, start_index - 2, entity_type])

    text = text.strip()

    result_json = {
        "text": text,
        "label": label,
        "Comments": []
    }

    return result_json

# Function to read sentences and labels from the given text file, handling corner cases
def read_sentences_from_file_with_corner_cases(file_path):
    sentences = []
    current_sentence = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                parts = line.split("\t")
                if len(parts) != 2:
                    continue
                word, label = parts
                if "-" not in label:
                    label = "O"
                current_sentence.append((word, label))
            elif current_sentence:
                sentences.append(current_sentence)
                current_sentence = []
        if current_sentence:
            sentences.append(current_sentence)
    return sentences

# Path to the uploaded text file
file_path = '/home/ehz/nlp-processing/input_data.txt'

# Read the sentences from the uploaded file using the updated function with corner case handling
sentences = read_sentences_from_file_with_corner_cases(file_path)

# Convert the sentences into the desired JSON format
converted_json_objects = [convert_to_json(sentence) for sentence in sentences]

# Output the result as a true JSON object
output_file_path = '/home/ehz/nlp-processing/outputfile.json'
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(converted_json_objects, file, ensure_ascii=False)

