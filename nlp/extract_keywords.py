# # # nlp_utils/extract_keywords.py
# # from sklearn.feature_extraction.text import TfidfVectorizer

# # def extract_keywords(preprocessed_text, top_k=10):
# #     corpus = [preprocessed_text]
# #     vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
# #     matrix = vectorizer.fit_transform(corpus)
# #     names = vectorizer.get_feature_names_out()
# #     scores = matrix.toarray()[0]
# #     keywords = sorted(zip(names, scores), key=lambda x: x[1], reverse=True)
# #     return [word for word, score in keywords[:top_k] if score > 0]

# # nlp/extract_keywords.py
# import pandas as pd
# from gensim import corpora, models
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# import os
# import tempfile
# import re
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# import nltk

# # Download required NLTK data
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

# try:
#     nltk.data.find('corpora/stopwords')
# except LookupError:
#     nltk.download('stopwords')

# try:
#     nltk.data.find('corpora/wordnet')
# except LookupError:
#     nltk.download('wordnet')

# def preprocess_text(text):
#     """
#     Preprocess text for LDA model training and keyword extraction
#     """
#     # Convert to lowercase
#     text = text.lower()
    
#     # Remove special characters and digits
#     text = re.sub(r'[^a-zA-Z\s]', '', text)
    
#     # Tokenize
#     tokens = word_tokenize(text)
    
#     # Remove stopwords
#     stop_words = set(stopwords.words('english'))
#     tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
#     # Lemmatize
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
#     return ' '.join(tokens)

# def train_lda_model(documents, num_topics=5):
#     """
#     Train LDA model for topic modeling and keyword extraction
#     """
#     try:
#         # Preprocess documents
#         processed_docs = [preprocess_text(doc).split() for doc in documents]
        
#         # Filter out empty documents
#         processed_docs = [doc for doc in processed_docs if doc]
        
#         if not processed_docs:
#             return None, None, None
        
#         # Create dictionary and corpus
#         dictionary = corpora.Dictionary(processed_docs)
        
#         # Filter extremes to improve model quality
#         dictionary.filter_extremes(no_below=1, no_above=0.8)
        
#         corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
        
#         if not corpus or not any(corpus):
#             return None, None, None
        
#         # Train LDA model
#         lda_model = models.LdaModel(
#             corpus=corpus,
#             id2word=dictionary,
#             num_topics=num_topics,
#             passes=10,
#             alpha='auto',
#             eta='auto',
#             random_state=42,
#             eval_every=None  # Disable perplexity calculation for speed
#         )
        
#         return lda_model, corpus, dictionary
    
#     except Exception as e:
#         print(f"Error training LDA model: {e}")
#         return None, None, None

# def extract_keywords_lda(text, num_topics=5, top_k=10):
#     """
#     Extract keywords using LDA topic modeling
#     """
#     try:
#         # For single document, we'll create multiple "documents" by splitting into sentences
#         # This gives LDA more data to work with
#         sentences = re.split(r'[.!?]+', text)
#         sentences = [s.strip() for s in sentences if len(s.strip()) > 20]  # Filter short sentences
        
#         if len(sentences) < 2:
#             # Fallback to TF-IDF if we don't have enough sentences
#             return extract_keywords_tfidf(text, top_k)
        
#         # Train LDA model
#         lda_model, corpus, dictionary = train_lda_model(sentences, num_topics)
        
#         if lda_model is None:
#             # Fallback to TF-IDF if LDA fails
#             return extract_keywords_tfidf(text, top_k)
        
#         # Extract keywords from all topics
#         keywords = []
#         for topic_id in range(num_topics):
#             topic_words = lda_model.show_topic(topic_id, topn=top_k//num_topics + 2)
#             for word, prob in topic_words:
#                 if word not in keywords and len(word) > 2:
#                     keywords.append(word)
        
#         return keywords[:top_k] if keywords else extract_keywords_tfidf(text, top_k)
    
#     except Exception as e:
#         print(f"Error in LDA keyword extraction: {e}")
#         # Fallback to TF-IDF
#         return extract_keywords_tfidf(text, top_k)

# def extract_keywords_tfidf(text, top_k=10):
#     """
#     Fallback keyword extraction using TF-IDF
#     """
#     try:
#         preprocessed_text = preprocess_text(text)
        
#         if len(preprocessed_text.strip()) == 0:
#             return []
        
#         corpus = [preprocessed_text]
#         vectorizer = TfidfVectorizer(
#             max_features=100, 
#             stop_words='english',
#             ngram_range=(1, 2),  # Include bigrams
#             min_df=1
#         )
        
#         matrix = vectorizer.fit_transform(corpus)
#         feature_names = vectorizer.get_feature_names_out()
#         scores = matrix.toarray()[0]
        
#         # Get top keywords
#         keywords_with_scores = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
#         keywords = [word for word, score in keywords_with_scores[:top_k] if score > 0]
        
#         return keywords
    
#     except Exception as e:
#         print(f"Error in TF-IDF keyword extraction: {e}")
#         return []

# def extract_keywords(text, method='lda', top_k=10):
#     """
#     Main keyword extraction function with multiple methods
    
#     Args:
#         text (str): Input text for keyword extraction
#         method (str): Method to use ('lda', 'tfidf', or 'hybrid')
#         top_k (int): Number of top keywords to return
    
#     Returns:
#         list: List of extracted keywords
#     """
#     if not text or len(text.strip()) < 50:
#         return []
    
#     try:
#         if method == 'lda':
#             return extract_keywords_lda(text, top_k=top_k)
#         elif method == 'tfidf':
#             return extract_keywords_tfidf(text, top_k=top_k)
#         elif method == 'hybrid':
#             # Combine both methods
#             lda_keywords = extract_keywords_lda(text, top_k=top_k//2)
#             tfidf_keywords = extract_keywords_tfidf(text, top_k=top_k//2)
            
#             # Merge and deduplicate
#             all_keywords = []
#             for kw in lda_keywords + tfidf_keywords:
#                 if kw not in all_keywords:
#                     all_keywords.append(kw)
            
#             return all_keywords[:top_k]
#         else:
#             # Default to LDA
#             return extract_keywords_lda(text, top_k=top_k)
    
#     except Exception as e:
#         print(f"Error in keyword extraction: {e}")
#         # Final fallback
#         return extract_keywords_tfidf(text, top_k=top_k)

# nlp/extract_keywords.py
import pandas as pd
from gensim import corpora, models
import os
import tempfile
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def preprocess_text(text):
    """
    Preprocess text for LDA model training and keyword extraction
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(tokens)

def train_lda_model(documents, num_topics=5):
    """
    Train LDA model for topic modeling and keyword extraction
    """
    try:
        # Preprocess documents
        processed_docs = [preprocess_text(doc).split() for doc in documents]
        
        # Filter out empty documents
        processed_docs = [doc for doc in processed_docs if doc]
        
        if not processed_docs:
            return None, None, None
        
        # Create dictionary and corpus
        dictionary = corpora.Dictionary(processed_docs)
        
        # Filter extremes to improve model quality
        dictionary.filter_extremes(no_below=1, no_above=0.8)
        
        corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
        
        if not corpus or not any(corpus):
            return None, None, None
        
        # Train LDA model
        lda_model = models.LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=num_topics,
            passes=10,
            alpha='auto',
            eta='auto',
            random_state=42,
            eval_every=None  # Disable perplexity calculation for speed
        )
        
        return lda_model, corpus, dictionary
    
    except Exception as e:
        print(f"Error training LDA model: {e}")
        return None, None, None

def extract_keywords(text, top_k=10):
    """
    Extract keywords using LDA topic modeling
    
    Args:
        text (str): Input text for keyword extraction
        top_k (int): Number of top keywords to return
    
    Returns:
        list: List of extracted keywords
    """
    if not text or len(text.strip()) < 50:
        return []
    
    try:
        # For single document, we'll create multiple "documents" by splitting into sentences
        # This gives LDA more data to work with
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]  # Filter short sentences
        
        if len(sentences) < 2:
            # If we don't have enough sentences, return empty list
            print("Not enough sentences for LDA analysis")
            return []
        
        # Train LDA model
        lda_model, corpus, dictionary = train_lda_model(sentences, num_topics=5)
        
        if lda_model is None:
            print("LDA model training failed")
            return []
        
        # Extract keywords from all topics
        keywords = []
        for topic_id in range(5):  # num_topics = 5
            topic_words = lda_model.show_topic(topic_id, topn=top_k//5 + 2)
            for word, prob in topic_words:
                if word not in keywords and len(word) > 2:
                    keywords.append(word)
        
        return keywords[:top_k] if keywords else []
    
    except Exception as e:
        print(f"Error in LDA keyword extraction: {e}")
        return []