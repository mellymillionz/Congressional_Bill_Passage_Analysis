# Congressional_Bill_Analysis
Analysis and predictions on Congressional bill passage

# Sittin’ Here on Capital Hill: Investigation of Congressional Bill Data

## Question: Predicting what bills will pass
- What makes a passable bill?
- Are there particular types of bills that are more likely to pass (topics)? Ones that never pass?

## Dependent Variable: Pass or not pass

- Second Dependent Variable: Law or not law

Features:

- Text analysis on bill summary content using topic modeling: https://www.congress.gov/bill/93rd-congress/house-bill/1?s=3&r=1

Increase domain knowledge on bill types:
https://govtracknews.wordpress.com/2009/11/11/what-are-the-different-types-of-bills/

## Further investigations: 

- When were the most bills passed? The least?
- How actually important is house majority?
- Predict Republican or Democrat proposed based on content

## Why this matters: 

- Which types of bills pass and why: text analysis is a big part of it!
- Provides a snapshot of how our democracy is working 
- Investigates how bill passage has changed over time.

## Dataset:

Full dataset:
https://www.congress.gov/about/data
http://www.congressionalbills.org/download.html

Documentation: https://github.com/usgpo/bill-status/blob/master/BILLSTATUS-XML_User_User-Guide.md

## Modeling:

- Topic modeling on summaries and titles
- Tokenize
- IFIDF or Countvectorizer
- LDA 
- Word Clouds for each Congress
Classification algorithm:
- Naive Bayes
- Logistic Regression
- Random Forest

Evaluations: 
- AUC/ROC
- Accuracy, F1, Precision, Recall
- Focus on Recall because only care about correct classification of PASS

Modeling resource: https://www.analyticsvidhya.com/blog/2018/04/a-comprehensive-guide-to-understand-and-implement-text-classification-in-python/

## Visualizations:
- What state reps intro/pass the most bills heat map us states
- Bills passed over the years (or at least by each Congress) stacked bar graph
- Bills introduced by men vs women
- Bills introduced by Dem vs Rep
- Who introduces the mos Bills (names)
- Passes during Majority vs non-majority
- Number of cosponsors/bill type or bill passage
- Bill topics that get vetoed!
- Time passed between bill introduction and law

## Questions:
- How best to deal with class imbalance (this is a dataset similar to disease detection and fraud detection - small amount of 1’s in a sea of 0’s)
- Run on all bills in all congresses? Just the last 3? Last 1?
- If I do both from question above is there a a good way to compare them?

## Other Resources:

Using Neural Networks to understand Congress
https://medium.com/fiscalnote-in-depth/how-we-used-neural-networks-to-understand-congress-c6aec3069594
Specific Bill info
https://www.congress.gov/bill/116th-congress/house-resolution/739/related-bills
