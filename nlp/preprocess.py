import matplotlib.pyplot as plt
import string
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import spacy
import re


nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub(r'\d+', ' ', text)    
    text = re.sub(r'\s+', ' ', text, flags=re.I)

    stop = stopwords.words('english')
    text_split = text.split()
    result = [word for word in text_split if word not in stop]
    text = ' '.join(result) 

    text_split = text.split()
    result = [word for word in text_split if len(word) > 2]
    text = ' '.join(result) 

    doc = nlp(text)
    named_entities = set(ent.text.lower() for ent in doc.ents)

    cleaned_tokens = []
    for token in doc:
        if (
            token.text not in STOP_WORDS and 
            not token.is_punct and 
            not token.is_space and
            token.text.lower() not in named_entities
        ):
            cleaned_tokens.append(token.lemma_)

    cleaned_tokens = ' '.join(cleaned_tokens)
    return text