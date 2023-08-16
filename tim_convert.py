import re

# Patterns for Bengali names for months and days of the week
months = "জানুয়ারি|ফেব্রুয়ারি|মার্চ|এপ্রিল|মে|জুন|জুলাই|আগস্ট|সেপ্টেম্বর|অক্টোবর|নভেম্বর|ডিসেম্বর"
days = "রবিবার|সোমবার|মঙ্গলবার|বুধবার|বৃহস্পতিবার|শুক্রবার|শনিবার"

# Advanced regex pattern for time-related entity extraction in Bengali
advanced_pattern = re.compile('|'.join([
    rf'\d{{1,2}} ({months}) \d{{4}}',   # Specific Dates
    r'\d{4}-\d{2}',                     # Year Ranges
    rf'(\d{{4}}|{months})',             # Individual Years and Months
    r'গত \w+',                         # Relative Time Expressions
    rf'({days})',                       # Weekdays
    rf'\d{{1,2}} ও \d{{1,2}} ({months})' # Date Ranges
]))

# Reading the content of the uploaded text file
file_path = '/home/ehz/Downloads/original_sentences.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    sentences = file.readlines()

# Processing sentences to extract time-related entities
time_related_entities = []
for idx, sentence in enumerate(sentences):
    sentence = sentence.strip()
    label = []
    for match in advanced_pattern.finditer(sentence):
        start, end = match.span()
        label.append([start, end, "TIME"])
    time_related_entities.append({
        "id": idx + 1,
        "label": label
    })

# Output file path for saving the extracted time-related entities
output_file_path = '/home/ehz/Downloads/time.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    for entry in time_related_entities:
        file.write(str(entry) + '\n')
