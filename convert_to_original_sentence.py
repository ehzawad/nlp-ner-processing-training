def convert_annotated_text_to_sentences_revised(text):
    sentences = []
    sentence = []
    for line in text.split('\n'):
        if line.strip() == '':
            sentences.append(' '.join(sentence))
            sentence = []
        else:
            word = line.split('\t')[0]  # Only considering the part before the first tab
            sentence.append(word)
    if sentence:
        sentences.append(' '.join(sentence))
    return '\n'.join(sentences)

# Path to the file
file_path = '/home/ehz/Downloads/all_data.txt'

# Reading the uploaded file
with open(file_path, 'r', encoding='utf-8') as file:
    annotated_text = file.read()

# Converting the annotated text to original sentences using the revised function
original_sentences_revised = convert_annotated_text_to_sentences_revised(annotated_text)

# Optionally, you can write the converted text to a new file
with open('/home/ehz/Downloads/original_sentences.txt', 'w', encoding='utf-8') as file:
    file.write(original_sentences_revised)

print("Conversion successful!")
