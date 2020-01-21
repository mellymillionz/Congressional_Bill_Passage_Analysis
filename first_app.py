import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector 
import config_final
import requests

from sodapy import Socrata
import sqlalchemy as db

import config_final as config
from schema import DbSchema

import spacy
from spacy.lang.en import English
import en_core_web_sm
import string
import re

import seaborn as sns
import matplotlib.pyplot as plt

# %matplotlib inline

# from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

import pickle
from sklearn.model_selection import train_test_split

from tokenizer import Tokenizer

import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt

# import plotly_express as px


st.title("Sittin' Here on Capital Hill")
st.header("Analysis of Congressional Bill Passage")
"""
Call to MySQL
"""
bills_db = DbSchema(config)

df = bills_db.query("""
    SELECT
        cb.Title,
        cb.Cong,
        cb.PassH,
        tp.dominant_topic
    FROM con_bills.current_bills as cb
    JOIN con_bills.topics as tp
    ON cb.BillID = tp.BillID
    WHERE cb.Cong >=110
    """)

st.dataframe(df.head())


def make_graph(df, x, y, hue, title_):

    plt.figure(figsize=(20,5))

    hue_order = ["1", "0"]

    (df[x]
        .groupby(df[hue])
        .value_counts(normalize=True)
        .rename(y)
        .reset_index()
        .pipe((sns.barplot, "data"), x=x, y=y, hue=hue)
        .set_title(title_))
    return st.pyplot()

make_graph(df, 'Cong', 'proportion', 'PassH', 'Passage by Congress')


tokenizer = Tokenizer()

#full combined text df
# com_text = 'combined_text.sav'
# combined_text_df = pickle.load(open(com_text, 'rb'))

# combined_text_df.head()
# st.write()

# X1 = combined_text_df['combined_text']
# y1 = combined_text_df['PassH']

# X_train, X_test, y_train1, y_test1 = train_test_split(X1, y1, random_state=2)

# vectorizer = CountVectorizer(tokenizer = tokenizer.tokenize, max_df = 0.90, max_features = 10000) # max_df=0.90, min_df=10
# transformed = vectorizer.fit_transform(X1, y1)

#final CV model for topic modeling
#transformed
filename = 'finalized_countvectorizer_model.sav'
transformed = pickle.load(open(filename, 'rb'))


# #vectorizer
filename1 = 'finalized_vectorizer.sav'
vectorizer = pickle.load(open(filename1, 'rb'))


#vectorizer
filename2 = 'finalized_lda_model.sav'
best_lda_model = pickle.load(open(filename2, 'rb'))


#load topics graph
pyLDAvis.enable_notebook()
panel = pyLDAvis.sklearn.prepare(best_lda_model, transformed, vectorizer, mds='tsne')
panel
st.pyplot()

# topics_viz = 'finalized_pyDavis_graph.sav'
# topics= pickle.load(open(topics_viz, 'rb'))
# st.pyplot()



# load the model from disk
# tk_titles = 'tokenized_titles.sav'
# df= pickle.load(open(tk_titles, 'rb'))
# st.dataframe(df.head())


X = df['Title']
y = df['PassH']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state=1)

# def dummy(doc):
#     return doc



lr_clf = Pipeline([('vect', CountVectorizer(tokenizer = tokenizer.tokenize, max_df=0.5, max_features=None)),
               ('clf', LogisticRegression(class_weight='balanced', C=.8)),
              ])

# Logistic Regression Classifier

# lr_clf = LogisticRegression(class_weight='balanced', C=.8)

# load the model from disk

# lr_word_model = 'finalized_logistic_regression_word_model.sav'

# Final_Model = pickle.load(open(lr_word_model, 'rb'))

# test_ = lr_clf.predict(['A bill to provide tax releif and tax incentives and jobs and reduce recidivism'])

lr_clf.fit(X_train, y_train)

bill_title = st.text_input('Enter Bill Title')



prediction = lr_clf.predict(bill_title)

st.write(prediction)



