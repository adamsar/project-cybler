"""
Defines methods for training data
"""
import re
import numpy as np
from nltk.probability import FreqDist
from nltk.classify import SklearnClassifier
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

pipeline = Pipeline([('tfidf', TfidfTransformer()),
                     ('chi2', SelectKBest(chi2, k=1000)),
                     ('nb', MultinomialNB())])
classifier = SklearnClassifier(pipeline)
is_word = re.compile("a-zA-z")
    
def tokenize(text, stop_words=stopwords.words('english')):
    """
    Breaks text into a list of properly tokenized words
    """
    
    # Note, remove '=' symbols before tokenizing, since these
    # sometimes occur within words to indicate, e.g., line-wrapping.
    msg_words = [wordpunct_tokenize(text.replace('=\n', '').lower())]

    # Get rid of punctuation tokens, numbers, and single letters.
    return [w for w in msg_words if len(w) > 1  and w not in stop_words and is_word.search(w)]

    
def get_features(tokens):
    """
    Get a distributed feature list for all inputed tokens. For
    now returns a simple frequency distribution. Needs to be
    updated to take titles and other factors into consideration.
    """
    return FreqDist(tokens)
    

def train(category, text):
    """
    Trains a category based on a chunk of text
    """
    features = get_features(tokenize(text))
    print features
    classifier.train([(features, category)])
                
        
