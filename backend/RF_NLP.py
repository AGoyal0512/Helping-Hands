import pandas as pd
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
import string
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.metrics import accuracy_score

lemmatizer = WordNetLemmatizer()
stop = stopwords.words("english")
punctuations = list(string.punctuation)
stop += punctuations

def get_simple_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def clean(words):
    output_words = []
    for w in words:
        if w.lower() not in stop:
            pos = pos_tag([w])
            clean_word = lemmatizer.lemmatize(w, pos = get_simple_pos(pos[0][1])).lower()
            output_words.append(clean_word)
    return output_words


class suicide_predictor:
    def __init__(self):
        
        
        # Reading the dataset and subsetting the columns
        df = pd.read_csv('Suicide_Detection.csv', index_col="Unnamed: 0")
        # Text input
        text = pd.Series(df['text'])
        # One-hot encoding the Label column
        suicide = pd.Series(pd.get_dummies(df['class'], drop_first=True)['suicide'])
    
        # Reorganizing our dataset after one-hot encoding to have a 0/1 label
        df = { 'Text': text, 'suicide': suicide }
        df = pd.DataFrame(df)
        df = df.reset_index().drop('index', axis = 1)
    
        # Splitting the data
        train_data, test_data = train_test_split(df, test_size=0.25, random_state=10)
        Xtrain_text = np.array(train_data["Text"].astype(str))
        Xtrain_text = [clean(word_tokenize(words)) for words in Xtrain_text]
        Xtrain_text = [" ".join(words) for words in Xtrain_text]
        self.count_vec = CountVectorizer(max_features = 2000)
        temp = self.count_vec.fit_transform(Xtrain_text)
        X_train_features = temp.todense()
    
        self.clf = rf(n_estimators = 80, random_state = 18, max_depth = 100)
        self.clf.fit(X_train_features, train_data['suicide'])
    
    def clean_str(self, msg):
        msg_text = clean(word_tokenize(msg))
        msg_text = [" ".join(msg_text)]
        msg_features = self.count_vec.transform(msg_text).todense()
        return msg_features
        
    def predict(self, msg):
        return self.clf.predict(msg)