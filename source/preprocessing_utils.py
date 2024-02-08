import string

import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def entity_recognizer(df):
    nlp = spacy.load("en_core_web_sm")
    ents = []

    for i, row in df.iterrows():
        question = row["question"]
        doc = nlp(question)
        ents.append([ent.lemma_.lower() for ent in doc.ents])
    return ents


def find_most_frequent_entity(entity_list):
    # Flatten the list of lists
    flat_list = []
    for row in entity_list:
        flat_list.extend(row)

    # Find the most frequent entity
    entity = max(set(flat_list), key=flat_list.count)
    return entity


def questions_replace_entity(df, entity_to_replace, replacement_entity="company"):
    # Load stopwords
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

    # Load stop_list and punctuation
    stop_list = [",", "?", "\n", "/", ".", "(", ")", "&", "-", "\t\t", " "]
    punctuation = string.punctuation
    stpwrd = nltk.corpus.stopwords.words("english")
    stpwrd.extend(stop_list)
    stpwrd.extend(punctuation)

    # Create a lemmatizer
    lemmatizer = WordNetLemmatizer()

    cleaned_questions = []

    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        question = row["question"]
        words = word_tokenize(question)
        lemmas = [
            lemmatizer.lemmatize(word.lower())
            for word in words
            if word.lower() not in stop_words and word not in punctuation
        ]
        new_word_list = [replacement_entity if word == entity_to_replace else word for word in lemmas]
        cleaned_questions.append(new_word_list)

    return cleaned_questions
