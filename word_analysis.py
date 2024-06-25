import nltk
from nltk.corpus import wordnet
import pandas as pd

# Ensure NLTK data is downloaded
nltk.download('wordnet')

# Load the input CSV file, specifying the encoding
input_file = '/content/word convert.csv'
words_df = pd.read_csv(input_file, encoding='latin-1')

# Print the column names to check the available columns
print("Column names in the CSV:", words_df.columns)

# Ensure the column name is correct
if 'Training Data' not in words_df.columns:
    raise KeyError("The column 'Training Data' is not found in the CSV file. Please check the column names.")

# Initialize containers for results
results = []

# Define some pairs of words to compare for similarity
comparison_pairs = [
    ('run.v.01', 'sprint.v.01'),
    ('ship.n.01', 'boat.n.01')
]

# Process each word in the CSV
for word in words_df['Training Data']:
    word_data = {'word': word}

    # Find synsets
    syns = wordnet.synsets(word)
    if syns:
        first_synset = syns[0]
        word_data['synset'] = first_synset.name()
        word_data['lemma'] = first_synset.lemmas()[0].name()
        word_data['definition'] = first_synset.definition()
        word_data['examples'] = first_synset.examples()
    else:
        word_data['synset'] = None
        word_data['lemma'] = None
        word_data['definition'] = None
        word_data['examples'] = None

    # Find synonyms and antonyms
    synonyms = []
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    word_data['synonyms'] = set(synonyms)
    word_data['antonyms'] = set(antonyms)

    # Calculate similarities for the specified pairs
    for pair in comparison_pairs:
        w1 = wordnet.synset(pair[0])
        w2 = wordnet.synset(pair[1])
        similarity = w1.wup_similarity(w2)
        word_data[f'similarity_{pair[0]}_{pair[1]}'] = similarity

    # Append the word data to results
    results.append(word_data)

# Convert results to a DataFrame and save to CSV
results_df = pd.DataFrame(results)
output_file = '/content/word_analysis_results.csv'
results_df.to_csv(output_file, index=False)

print(f'Results saved to {output_file}')
