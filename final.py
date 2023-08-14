import json

def process_labels(labeled_words):
    new_labeled_words = []
    i = 0
    while i < len(labeled_words):
        word, label = labeled_words[i]
        if label == "TIM":
            # Check the immediate previous neighbor if it's 'O'
            if i > 0 and labeled_words[i - 1][1] == "O":
                new_labeled_words[-1] = (new_labeled_words[-1][0], "TIM")
            # Check the immediate next neighbor if it's 'O'
            if i < len(labeled_words) - 1 and labeled_words[i + 1][1] == "O":
                i += 1
                new_labeled_words.append((labeled_words[i][0], "TIM"))
            new_labeled_words.append((word, label))
        else:
            new_labeled_words.append((word, label))
        i += 1
    return new_labeled_words

def convert_labeled_words_to_jsonl_entry(labeled_words, sentence_id):
    processed_sentence = process_labels(labeled_words)
    sentence_text = ""
    entity_labels = []
    current_index = 0
    entity_start_index = None
    entity_type = None
    for word, label in processed_sentence:
        if label != "O":
            current_entity_type = label
            if entity_start_index is None:
                entity_start_index = current_index
                entity_type = current_entity_type
            elif current_entity_type != entity_type:
                entity_labels.append([entity_start_index, current_index - 1, entity_type])
                entity_start_index = current_index
                entity_type = current_entity_type
        elif entity_start_index is not None:
            entity_labels.append([entity_start_index, current_index - 1, entity_type])
            entity_start_index = None
            entity_type = None
        sentence_text += word + " "
        current_index += len(word) + 1
    if entity_start_index is not None:
        entity_labels.append([entity_start_index, current_index - 2, entity_type])
    sentence_text = sentence_text.strip()
    return {"id": sentence_id, "text": sentence_text, "label": entity_labels, "Comments": []}

def read_labeled_sentences_from_file(file_path):
    sentences = []
    current_sentence = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split("\t")
                if len(parts) != 2:
                    continue
                word, label = parts
                current_sentence.append((word, label))
            elif current_sentence:
                sentences.append(current_sentence)
                current_sentence = []
        if current_sentence:
            sentences.append(current_sentence)
    return sentences

input_file_path = '/home/ehz/nlp-processing/input_data.txt'
labeled_sentences = read_labeled_sentences_from_file(input_file_path)
jsonl_objects = [convert_labeled_words_to_jsonl_entry(sentence, sentence_id=i+1) for i, sentence in enumerate(labeled_sentences)]
output_file_path = '/home/ehz/nlp-processing/outputfile.jsonl'

with open(output_file_path, 'w', encoding='utf-8') as file:
    for obj in jsonl_objects:
        json.dump(obj, file, ensure_ascii=False)
        file.write('\n')

print("JSONL file has been successfully created.")
