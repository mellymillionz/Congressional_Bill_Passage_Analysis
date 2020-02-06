# Analysis and Predictions of Congressional Bill Passage in the House of Representatives

# Overview:  
This project used Congressional bill data from 110th to 114th Congresses (2011-2017) as the dataset for a binary classification project focusing on prediction of the minority class (Passed Bills). The dataset consisted of 51,067 bills (resolutions and join resolutions were excluded), of which less than 12% passed the House. The data contained  metafeatures about the bill itself (ie. passage date, introduction date), the proposing congressperson (ie. state, party, name), the Congress at the time of proposal (iw. Congress number, majority), and  text features (title, bill summary). The data spanned two Democratic majority congresses, two split congresses, and ended with a Republican majority congress.

The text features were used for topic modeling using natural language processing, and those topics were included as a feature in the final classification model.

**Full dataset**:

**Webscrape summaries**: https://www.congress.gov/about/data

**API call**: http://www.congressionalbills.org

![Class Imbalance - Bill Passage](https://github.com/mellymillionz/Congressional_Bill_Passage_Analysis/blob/master/Visualizations/Bill_Split_2.png)

## Natural Language Processing:
Webscraped bill summaries were first parsed using Beautiful Soup and stored in MySQL.

Initial text exploratory analysis included word clouds for Passed and Not Passed Bills, as well as for each congress.

![Passed Bills Wordcloud](https://github.com/mellymillionz/Congressional_Bill_Passage_Analysis/blob/master/Visualizations/passed_wordcloud.png)

A custom **Spacy tokenizer** was used to process the text features (title and summary). Punctuations were removed and words were lemmatized, most parts of speech were preserved as bills contain few adjectives and proper nouns were deemed important to bill comprehension and topics. Included in the tokenizer were custom stopwords that appeared in more than 90% of the corpus (such as 'bill', or 'amend'), and limited to 10,000 words. The tokenizer was passed into a CountVectorizer before topic modeling.

## Topic Modeling: 
Processed summaries were then used for topic modeling using **Latent Dirichlet Allocation**. Optimal parameters were tested first using a wide spread in Gridsearch, particularly with n-components (the actual number of topics). Human review was used once the number of topics had been narrowed between 10-15, with 13 topcis being optimal for human topic comprehension.

Final topics were also evaluated using Log Likelihood and Perplexity, but overall these had little effect on the actual parameters chosen.

Topics were explored using pyLDAvis: file:///Users/melissamunz/src/Final_Bill_Project/Congressional_Bill_Classification/topic_model_visualization.html#topic=0&lambda=1&term=

Topics were also explored using PCA and t-sne:

![Visual Representation of Topics using t-SNE](https://github.com/mellymillionz/Congressional_Bill_Passage_Analysis/blob/master/Visualizations/t-sne_topics.png)


## Exploratory Analysis of Non-text features:
Topics were added back into the non-text metafeatures and used for further exploratory analysis. 

Several features in the original dataset were removed to prevent data leakage, and the final dataset included 17 features. Categorical features were one-hot-encoded and numeric features were scaled. All were added into a columntransformer and pipeline for model testing.

Passed bills by topic and congress:

## Visualizations:

Exploratory analysis was done on many of the metafeatures, including:
- Bills passage by Congress:
- Bills introduced by gender of congressperson.
- Bills introduced by party of congressperson.
- Who introduces the most Bills (Congressperson Name)
- Bill Passage during Majority vs Non-majority Congress
- Number of cosponsors and bill passage
- Bill topics that get vetoed
- Time passed between bill introduction and law

![Proportional State Bill Passage:](https://github.com/mellymillionz/Congressional_Bill_Passage_Analysis/blob/master/Visualizations/state_bill_passage.png)

## Modeling:

Four models were tested, including Naive Bayes for baseline comparison. Hyperparameter tuning focused on optimising for recall and balancing the major class imbalance between passed and not passed bills. All models were chosen because they allowed for weighting to counter the class imbalance.

Classification models:
- Naive Bayes
- Logistic Regression
- Stochastic Gradient Descent (with log)
- Random Forest

Evaluation Metrics: 
- AUC/ROC
- Accuracy, F1, Precision, Recall

![Comparison of Models:](https://github.com/mellymillionz/Congressional_Bill_Passage_Analysis/blob/master/Visualizations/model_compare_chart.png)

**Final Model**: Logistic Regression, which performed best for recall of the minority class.

![ROC/AUC for Final Model](https://github.com/mellymillionz/Congressional_Bill_Passage_Analysis/blob/master/Visualizations/ROC_Logreg.png)


## Why this project matters: 
Which bills pass and why is something that should be important to all Americans - it is a reflfection of how our democracy operates. Additionally, it's directly relevant to the jobs of lobbyists and congresspersons alike. Thus, the feature importances are highly important for this project. Overall, the project provides a snapshot of how our democracy functions at the federal level, across different types of majority congresses in the modern era. 

**Which types of bills pass**:
- Harmonized Tariff Schedule and desgination related bills
- Bills proposed by US territories
- Bill title length
- Higher number of cosponors
- Bills from small states that have proportionall high passage rates.
- Bills from congresspersons in high population districts in big 3 states (CA,TX,NY)

## Limitations: 

The largest limitations were the class imbalance issue, concern over data leakage, and slow webscraping which resulted in less overall data to work with.

## Next Steps:

**Information on more congresses for comparison analysis over time**: Online records go back to the 93rd Congress, in 1973. It would be interesting do EDA on all online congressional data and see how they change over time.

**Stacked Modeling**: Models for meta-features combined with text data could mean great outcomes with the inclusion of stacking techniques.

**Introducing more features**: Continue this analysis by including data regarding the number of times a bill is introduced before it passed.
