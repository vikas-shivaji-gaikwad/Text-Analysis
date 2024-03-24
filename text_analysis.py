# -*- coding: utf-8 -*-
"""Text Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K4hEiSsCw1A0V0FrS-efZD3g0eecsXh2
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import zipfile
import os

# Load the input Excel file
input_file = 'Input.xlsx'
df = pd.read_excel(input_file)

# Function to extract article text from URL
def extract_article_text(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the article title
        title = soup.find('title').get_text()

        # Find the article text
        article_text = ''
        for paragraph in soup.find_all('p'):
            article_text += paragraph.get_text() + '\n'

        return title, article_text.strip()  # Strip extra whitespaces

    except Exception as e:
        print(f"Error occurred while extracting article from {url}: {e}")
        return None, None

# Create a directory to store text files
output_dir = 'extracted_articles'
os.makedirs(output_dir, exist_ok=True)

# List to store file paths for zip creation
file_paths = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    # Extract article text
    title, article_text = extract_article_text(url)

    if title and article_text:
        # Save the article text to a text file
        file_name = f"{url_id}.txt"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(article_text)
        print(f"Article extracted from {url} saved as {file_name}")

        # Add file path to the list
        file_paths.append(file_path)
    else:
        print(f"Failed to extract article from {url}")

# Create a zip file
zip_file_path = 'extracted_articles.zip'
with zipfile.ZipFile(zip_file_path, 'w') as zipf:
    # Write each file into the zip
    for file_path in file_paths:
        zipf.write(file_path, os.path.basename(file_path))

print("Extraction and zip creation completed.")

# Download the zip file
from google.colab import files
files.download(zip_file_path)

import nltk
nltk.download('punkt')
nltk.download('stopwords')

import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string

# Load the extracted article texts
input_dir = 'extracted_articles'
output_file = 'Output.xlsx'

# Function to perform textual analysis
def perform_textual_analysis(article_text):
    # Word count
    words = article_text.split()
    word_count = len(words)

    # Sentence count
    sentences = nltk.sent_tokenize(article_text)
    sentence_count = len(sentences)

    # Average word length
    total_word_length = sum(len(word) for word in words)
    average_word_length = total_word_length / word_count if word_count > 0 else 0

    # Most common words (excluding stop words and punctuation)
    stop_words = set(stopwords.words('english'))
    translator = str.maketrans('', '', string.punctuation)
    words_cleaned = [word.translate(translator).lower() for word in words if word.lower() not in stop_words]
    word_counter = Counter(words_cleaned)
    most_common_words = word_counter.most_common(5)

    return word_count, sentence_count, average_word_length, most_common_words

# Create a list to store the analysis results
output_data = []

# Iterate through each text file
for file_name in os.listdir(input_dir):
    if file_name.endswith('.txt'):
        url_id = file_name.split('.')[0]
        with open(os.path.join(input_dir, file_name), 'r', encoding='utf-8') as file:
            article_text = file.read()

        # Perform textual analysis
        word_count, sentence_count, average_word_length, most_common_words = perform_textual_analysis(article_text)

        # Store the analysis results in the list
        output_data.append({
            'URL_ID': url_id,
            'Word Count': word_count,
            'Sentence Count': sentence_count,
            'Average Word Length': average_word_length,
            'Most Common Words': ', '.join([word for word, _ in most_common_words])
        })

# Create a DataFrame from the list
output_df = pd.DataFrame(output_data)

# Save the analysis results to an Excel file
output_df.to_excel(output_file, index=False)
print(f"Textual analysis results saved to {output_file}")

output_file = '/content/drive/MyDrive/Output.xlsx'

import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict
import re

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('cmudict')

# Load the extracted article texts
input_dir = 'extracted_articles'
output_file = 'Output.xlsx'

# Load stop words
stop_words = set(stopwords.words('english'))

# Load positive and negative words
positive_words = set()
negative_words = set()

positive_file = 'positive-words.txt'
negative_file = 'negative-words.txt'

with open(positive_file, 'r') as file:
    positive_words = set(file.read().split())

with open(negative_file, 'r', encoding='ISO-8859-1') as file:
    negative_words = set(file.read().split())

# Function to calculate syllable count per word
def syllable_count(word):
    if word.lower() in stop_words:
        return 0

    # Remove non-alphabetic characters
    word = re.sub(r'[^a-zA-Z]', '', word.lower())

    # Exception cases
    if len(word) <= 3:
        return 1
    if word.endswith('es') or word.endswith('ed'):
        return 0

    # Calculate syllable count based on vowels
    count = 0
    vowels = 'aeiouy'
    prev_char_is_vowel = False
    for char in word:
        if char in vowels and not prev_char_is_vowel:
            count += 1
            prev_char_is_vowel = True
        elif char not in vowels:
            prev_char_is_vowel = False
    return count

# Function to perform textual analysis
def perform_textual_analysis(article_text):
    # Clean text
    tokens = word_tokenize(article_text)
    cleaned_tokens = [word.lower() for word in tokens if word.lower() not in stop_words and word.isalpha()]
    cleaned_text = ' '.join(cleaned_tokens)

    # Extract derived variables
    positive_score = sum(1 for word in cleaned_tokens if word in positive_words)
    negative_score = sum(1 for word in cleaned_tokens if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_tokens) + 0.000001)

    # Analyze readability
    sentences = sent_tokenize(article_text)
    total_words = len(cleaned_tokens)
    total_sentences = len(sentences)
    avg_sentence_length = total_words / total_sentences
    complex_words = [word for word in cleaned_tokens if syllable_count(word) > 2]
    percentage_complex_words = len(complex_words) / total_words
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = total_words / total_sentences
    complex_word_count = len(complex_words)
    word_count = total_words

    # Calculate average word length
    total_characters = sum(len(word) for word in cleaned_tokens)
    avg_word_length = total_characters / total_words

    # Count personal pronouns
    personal_pronouns = re.findall(r'\b(I|we|my|ours|us)\b', cleaned_text, flags=re.IGNORECASE)
    personal_pronoun_count = len(personal_pronouns)

    return positive_score, negative_score, polarity_score, subjectivity_score, \
           avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, \
           complex_word_count, word_count, personal_pronoun_count, avg_word_length

# Create a list to store the analysis results
output_data = []

# Iterate through each text file
for file_name in os.listdir(input_dir):
    if file_name.endswith('.txt'):
        url_id = file_name.split('.')[0]
        with open(os.path.join(input_dir, file_name), 'r', encoding='utf-8') as file:
            article_text = file.read()

        # Perform textual analysis
        analysis_results = perform_textual_analysis(article_text)

        # Store the analysis results in the list
        output_data.append({
            'URL_ID': url_id,
            'Positive Score': analysis_results[0],
            'Negative Score': analysis_results[1],
            'Polarity Score': analysis_results[2],
            'Subjectivity Score': analysis_results[3],
            'Avg Sentence Length': analysis_results[4],
            'Percentage of Complex Words': analysis_results[5],
            'Fog Index': analysis_results[6],
            'Avg Number of Words Per Sentence': analysis_results[7],
            'Complex Word Count': analysis_results[8],
            'Word Count': analysis_results[9],
            'Personal Pronouns': analysis_results[10],
            'Avg Word Length': analysis_results[11]
        })

# Create a DataFrame from the list
output_df = pd.DataFrame(output_data)

# Save the analysis results to an Excel file
output_df.to_excel(output_file, index=False)
print(f"Textual analysis results saved to {output_file}")

