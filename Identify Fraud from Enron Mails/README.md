### Enron dataset analysis: detect People-of-Interest (POI)


## Introduction

In 2000, Enron was one of the biggest companies in USA. By 2002, it went into bankruptcy due to a companywide corporate fraud. In the Federal investigation that followed a good amount of typically confidential information went open into the public. That included detailed financial record of executive as well as a good amount of email. 

With the help of machine learning and scikit-learn library, I built a POI identifier in order to detect potential people using features from the provided email & financial data, as well as labeled data - POIs who either reached a settlement, pleaded a deal, indicted or testified in exchange of immunity. 


## Short questions 

1) Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  

The goal of this project is to use the financial & email data from to build a predictive, analytic model that could identify whether an individual could be considered POI. The data set is comprised by email and financial data of 146 records (people), mostly senior management of Enron. Since our dataset already contains labeled data - people already listed as POs - the value on the existing dataset is quite questionable. The potential value of a such model is application to other datasets in similar cases in other companies as well as possibly identifying potential suspects worth investigating further. The data itself contains 146 records in total, 1 labeled feature (POI), 6 email features & 14 financial features. Within the data only 18 individuals were labeled as POI. 

On the other hand if we review how many of the features contain people with missing data: 

POI : 18, notPOI: 128 (12.328767% POI)
features (21 total): 
 - salary : 35% empty
 - to_messages : 41% empty
 - deferral_payments : 73% empty
 - total_payments : 14% empty
 - exercised_stock_options : 30% empty
 - bonus : 44% empty
 - restricted_stock : 25% empty
 - shared_receipt_with_poi : 41% empty
 - restricted_stock_deferred : 88% empty
 - total_stock_value : 14% empty
 - expenses : 35% empty
 - loan_advances : 97% empty
 - from_messages : 41% empty
 - other : 36% empty
 - from_this_person_to_poi : 41% empty
 - poi : 0% empty
 - director_fees : 88% empty
 - deferred_income : 66% empty
 - long_term_incentive : 55% empty
 - email_address : 24% empty
 - from_poi_to_this_person : 41% empty

With the help of EDA, I was able to identify 4 records that needs to be changed or removed:

1) TOTAL: Through visualizing the data, I found out that it is an extreme outlier since it comprises all financial data in it & thus needs to be removed.
2) LOCKHART EUGENE E: is an empty record containing NaN for all values.
3) THE TRAVEL AGENCY IN THE PARK: This must be a data-entry error as it does not represent an individual.
4) BELFER ROBERT and BHATNAGAR SANJAY were updated with the correct data to correspond to PDF.

After the data-clearning, we have 143 records remaining. 

2) What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: “create new features”, “properly scale features”, “intelligently select feature”]

In order to select the most relevant features, I leveraged from the SelectKBest in order to pick up the most influential features. I have tried various number of features & selected the number of features that produced the best scores in terms of accuracy, recall & precision. In our case the highest metrics were displayed with 9 features. The features along with their associated scores can be found in the table below:

| Feature                 | Score  | Valid |
| :---------------------- | -----: | ----: |
| exercised_stock_options | 24.815 |   102 |
| total_stock_value       | 24.183 |   126 |
| bonus                   | 20.792 |    82 |
| salary                  | 18.290 |    95 |
| financial_aggregate     | 15.971 |    71 |
| deferred_income         | 11.458 |    49 |
| long_term_incentive     |  9.922 |    66 |
| restricted_stock        |  9.213 |   102 |
| total_payments		  |  8.772 |   125 |

A table of the different number of features tried along with the performance metrics is below:

| Number of Feature       | Accuracy  | Precision | Recall |
| :---------------------- | --------: | --------: | -----: |
| 5 features Log.Reg.     | 0.825     |   0.390   | 0.248  |
| 5 features KMeans       | 0.816     |   0.326   | 0.186  |
| 8 features              | 0.847     |   0.464   | 0.472  |
| 9 features              | 0.856     |   0.462   | 0.493  |
| 10 features             | 0.831     |   0.385   | 0.435  |
| 11 features             | 0.828     |   0.367   | 0.397  |
| 12 features             | 0.820     |   0.352   | 0.422  |
| 15 features             | 0.782     |   0.272   | 0.381  |


The K-best is a classic approach of automated univariate feature selection algorithm, but I was hesitant when using it, due to the lack of email features in the resulting dataset. In order to overcome this, I created a feature poi_interaction - ratio of the total number of emails to & from POI to the total number of emails. I also created financial aggregate feature containing the sum of exercised_stock_options, salary & total_stock_value in order to understand what is the wealth of an individual. Both features were included in the final analysis as they slightly increased the precision & accuracy of most of the machine learning algorithms tested. 

Next I scaled all features with the min-max scaler. This step is of vital importance due to the magnitude of differences between features. With the feature scaling I ensured that for the applicable classifiers, features would be weighted evenly. 



3) What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?

I ended up using the logistic regression. The primary reason to choose it is because the prediction outcome is expected to be a binary classification. A classical use of this algorithm is for tumor benign/malignancy prediction based on medical test results. I sought to emulate this behaviour in predicting whether or not someone is a person of interest based on their email & financial behaviour. 

Initially I tried a couple of algorithms, with KMeans performing quite sufficient, which is not suprising since its objective was to separate the dataset into POI/non-POI groups. With less sucess were tested as well Adabooster, SVM, random forest classifier & stochastic gradient descent (with logistic regression)



4) What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).

Parameter tuning refers to the adjustment of the algorithm during training, in order to improve the fit on the test set. Parameters can influence heavily the outcome of the learning process, the more tuned the parameters, the more biased the algorithm will be. The strategy can be effective but as well lead to more fragile models & overfit in case not performed well in reality.

I tuned the parameters using exhaustive seraches with the following parameters:

Loigistic regression - inversive regularization (C), tollerance (tol) and over/undersampling (class_weight)
KMeans clustering - tol

KMeans was initialized with K of 2 in order to represent POI & non-POI clusters. Additionally, it performed better with only 8 best features & 2 additional. 

Suprisingly if we include the auto-weight in the logistic regression (selection of feature weights inversely proportional to class frequencies) improved the recall but lowered precision. The remaining algorithms were tuned experimentally with unremarkable improvement. 

5) What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?  [relevant rubric item: “validation strategy”]

Validation comprises a set of techniques to make sure our model generalizes well with the remaining part of the dataset. A classic mistakes, which I made as well as a start, is over-fitting where the model performed well on training set but had a substantially low result on the test set. In order to validate my analysis, I took the avg precision & recall over 1000 randomized trials with a sub-sectioned data 3:1 training-test ratio (done in poi_evaluation.py)

The main metrics utilized for evaluation are recall & precision. Recall stands for the ratio of true positives flagged as POIs, which basically means the sensitivity. Precision captures the ratio of true positives to the records that are POIs, describing how often a 'false alarm' are (not) raised. It is fairly obvious that due to the unbalanced nature of the dataset (very few POIs), accuracy is not a good metric. For the logistic regression & K-means clustering algorithms, I saw contradicting results between both validation methods described. Results are following:

Randomized, partitioned trials with n = 1000

| Classifier              | Precision | Recall    | Features  |
| ----------------------- | --------: | --------: | --------: |
| Logistic Regression     |     0.348 |     0.388 |        12 |
| K-means Clustering, K=2 |     0.232 |     0.355 |        10 |


Both algorithms performed quite well, given that the dataset is both sparse (few POI) and noisy.  In the context of helping fraud investigators, I would argue that recall is more important than precision.  In other words, as the objective is raising the alarm on individuals for further investigation, it seems to be important that suspects are included rather than innocent individuals be excluded.  A higher recall value would ensure that truly guilty individuals are flagged as POIs and would be investigated more thoroughly. 

In an attempt to optimize for a higher recall value, we can include balanced-weighting in logistic regression, which substaintially increased the recall:

Logistic Regression with Auto-weighting

|              | Precision | Recall    |
| ------------ | --------: | --------: |
| Validation   |     0.269 |     0.728 |




## Conclusion
The most challenging aspect of this project was the dataset itself & how sparse it was.  Most of the algorithms naturally perform much better on balanced datasets. Maybe an interesting topic for further investigation would be to apply anomaly detection algorithms on the dataset (usually used for credit card checking) in order to identify the POIs. In addition including temporal features may improve the study. Many of the features in the dataset are cumulative by nature and normalizing them over a predefined period might have increased the fidelity of the algorithms used. 


References:

1) http://fch808.github.io/Identifying_Fraud_at_Enron.html
2) https://jaycode.github.io/enron/identifying-fraud-from-enron-email.html
3) https://github.com/j-bennet/udacity-nano-da/tree/master/p5
4) https://github.com/lyvinhhung/Udacity-Data-Analyst-Nanodegree/tree/master/p5%20-%20Identify%20Fraud%20from%20Enron%20Email

Files:

1) final_project/emails_by_address/: email message data (not used)
2) tools/: helper tools and functions
3) final_project/tester.py: Udacity-provided file, produces relevant submission files
4) final_project/poi_evaluation.py: custom validation 
5) final_project/poi_email_addresses.py: prints dataset email addresses (not used)
6) final_project/poi_id.py: POI identifier
7) final_project/enron.py: containes helper functions and exploratory data analysis
