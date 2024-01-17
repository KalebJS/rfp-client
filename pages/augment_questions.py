import os
import re

import dotenv
import openai
import pandas as pd
import streamlit as st
from tqdm import tqdm
from transformers import set_seed # add
import nlpaug.augmenter.word as naw # add

from libraries.db import Question
from libraries.st_utils import get_db

set_seed(3) # add
aug = naw.ContextualWordEmbsAug(model_path="distilbert-base-uncased", device="cpu", action="substitute") # add

db = get_db()

st.title("Question Augmentation")
st.write(
    "This is simply a script to augment the questions in the "
    "questions table. Set the number of augmentations and click run. "
    "An LLM will create differently worded questions that we'd expect "
    "to have the same answer."
)

with st.sidebar:
    n_augmentations = st.number_input("Number of Augmentations", min_value=1, max_value=10, value=5)

if not st.button("Run"):
    st.stop()

with open("resources/question_augment_prompt.txt", "r") as f:
    prompt = f.read()

questions = db.get_questions()

question_pattern = re.compile(r"\d\. (.*)\n?")

for question in tqdm(questions):
    answer = db.get_answer_by_id(question.answer_id)
    augmented_question = aug.augment(question.text) # add
    print(augmented_question)
    # # content = prompt.format(question=question.text, answer=answer.text, n=n_augmentations)
    # content = prompt.format(question=augmented_question, answer=answer.text, n=n_augmentations) # change
    # conversation = [{"role": "user", "content": content}]
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=conversation,
    #     max_tokens=1000,
    # )
    # text = response["choices"][0]["message"]["content"]
    # choices = question_pattern.findall(text)
    # choices = [choice.strip().strip('"') for choice in choices]
    # for choice in choices:
    #     new_question = Question(text=choice, answer_id=answer.id)
    #     db.insert_question(new_question)
