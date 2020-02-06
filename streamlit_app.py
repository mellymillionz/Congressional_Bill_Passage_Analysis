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
from PIL import Image
# import plotly_express as px


st.title("Can you write a Congressional Bill that will pass the House of Representatives?")
# st.header("Analysis of Congressional Bill Passage")

capital = Image.open('2919_header-capitol.png')
st.image(capital, width=700)


bills_db = DbSchema(config)

df = bills_db.query("""
    SELECT
        cb.Cong,
        cb.Title,
        cb.NameFull,
        tp.dominant_topic,
        cb.PassH
    FROM con_bills.current_bills as cb
    JOIN con_bills.topics as tp
    ON cb.BillID = tp.BillID
    WHERE cb.Cong >=110
    """)





# option = st.sidebar.selectbox(
#     'Which bill topic would you like to review?',
#      df['dominant_topic'])

# 'You selected:', option


# def make_graph(df, x, y, hue, title_):

#     plt.figure(figsize=(20,5))

#     hue_order = ["1", "0"]

#     (df[x]
#         .groupby(df[hue])
#         .value_counts(normalize=True)
#         .rename(y)
#         .reset_index()
#         .pipe((sns.barplot, "data"), x=x, y=y, hue=hue)
#         .set_title(title_))
#     return st.pyplot()

# make_graph(df, 'Cong', 'proportion', 'PassH', 'Passage by Congress')

# import plotly.express as px  # Be sure to import express

# colorscale='RdBu'

# fig = px.choropleth(percent_df,  # Input Pandas DataFrame
#                     locations="State",  # DataFrame column with locations
#                     color="Percent_Passed",  # DataFrame column with color values
#                     hover_name="State", # DataFrame column hover info
#                     locationmode = 'USA-states') # Set to plot as US States
# fig.update_layout(
#     title_text = 'Percentage of Passed Bills by Proposing State Representative', # Create a Title
#     geo_scope='usa',
# )
# fig.show()
# st.pyplot()


tokenizer = Tokenizer()

X = df['Title']
y = df['PassH']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state=1)

# lr_clf = Pipeline([('vect', CountVectorizer(tokenizer = tokenizer.tokenize, max_df=0.5, max_features=None)),
#                ('clf', LogisticRegression(class_weight='balanced', C=.8)),
#               ])
# @st.cache
# lr_clf.fit(X_train, y_train)
# @st.cache(allow_output_mutation=True)

@st.cache(allow_output_mutation=True)
def logistic_regression(X_train, y_traint):
	# Train the model
	lr_clf = Pipeline([('vect', CountVectorizer(tokenizer = tokenizer.tokenize, max_df=0.5, max_features=None)),
               ('clf', LogisticRegression(class_weight='balanced', C=.8)),
              ])
	lr_clf.fit(X_train, y_train)
	return lr_clf

st.header('Write your Bill:')
bill_title = st.text_input('Enter text here')

sad = Image.open('sad3.png')
happy = Image.open('happy.png')

def pretty_pred(prediction):
        if prediction == 0:
            st.error('Sorry, your bill did not pass.')
            # st.write('The bill did not pass!')
            st.image(sad, width=300)
        if prediction == 1:
            st.success('Congratulations! Your bill passed!')
            # st.write('Congratulations! The bill passed!')
            st.image(happy, width=300)


def submit(bill_title):
    bill_list = bill_title.split(',')
    lr_clf = logistic_regression(X_train, y_train)
    prediction = lr_clf.predict(bill_list)
    return prediction

raw_prediction = submit(bill_title)
st.write(pretty_pred(raw_prediction))





