#!/usr/bin/python

from copy import copy
import matplotlib.pyplot as plt
import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat
from feature_format import targetFeatureSplit

import enron
import poi_evaluation

# features_list is a list of strings, each of which is a feature name
# first feature must be "poi", as this will be singled out as the label
target_label = 'poi'
email_features_list = [
    # 'email_address', # remit email address; informational label
    'from_messages',
    'from_poi_to_this_person',
    'from_this_person_to_poi',
    'shared_receipt_with_poi',
    'to_messages',
    ]
financial_features_list = [
    'bonus',
    'deferral_payments',
    'deferred_income',
    'director_fees',
    'exercised_stock_options',
    'expenses',
    'loan_advances',
    'long_term_incentive',
    'other',
    'restricted_stock',
    'restricted_stock_deferred',
    'salary',
    'total_payments',
    'total_stock_value',
]
features_list = [target_label] + financial_features_list + email_features_list

# load the dictionary containing the dataset
data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

# remove outliers
outlier_keys = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
enron.remove_keys(data_dict, outlier_keys)

# instantiate copies of dataset and features for grading purposes
my_dataset = copy(data_dict)
my_feature_list = copy(features_list)

# add two new features
enron.add_financial_aggregate(my_dataset, my_feature_list)
enron.add_poi_interaction(my_dataset, my_feature_list)

# get K-best features
num_features = 9
best_features = enron.get_k_best(my_dataset, my_feature_list, num_features)
my_feature_list = [target_label] + best_features.keys()



# print features
print "{0} selected features: {1}\n".format(len(my_feature_list) - 1, my_feature_list[1:])

# extract the features specified in features_list
data = featureFormat(my_dataset, my_feature_list)

# split into labels and features (this line assumes that the first
# feature in the array is the label, which is why "poi" must always
# be first in the features list
labels, features = targetFeatureSplit(data)

# scale features via min-max
from sklearn import preprocessing
scaler = preprocessing.MinMaxScaler()
features = scaler.fit_transform(features)

# parameter optimization (not currently used)
from sklearn.grid_search import GridSearchCV

### Logistic Regression Classifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import f_classif
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA

# prepare a pipeline for the cross-validated grid search for the Logistic Regression Model
# features are scaled between 0 - 1
# selects the KBest features using the ANOVA F-value for the classification
# uses the KBest features to reduce dimensionality further through PCA
# used the PCA components in the Logistic Regression
def get_LogReg_pipeline():
    pipeline = Pipeline(steps=[('minmaxer', MinMaxScaler()),
                               ('selection', SelectKBest(score_func=f_classif)),
                               ('reducer', PCA()),
                               ('classifier', LogisticRegression())
                               ])

    return pipeline


# prepares a parameters dictionary for cross-validated grid search
# makes a parameter dictionary to search over
# default parameters include only the final parameters found through searching
def get_LogReg_params(full_search_params=False):
    params = {'reducer__n_components': [.5],
              'reducer__whiten': [False],
              'classifier__class_weight': ['auto'],
              'classifier__tol': [1e-64],
              'classifier__C': [1e-3],
              'selection__k': [17]
              }

    if full_search_params:
        params = {'selection__k': [7, 9, 12, 17, 'all'],
                  'classifier__C': [1e-07, 1e-05, 1e-2, 1e-1, 1, 10],
                  'classifier__class_weight': [{True: 12, False: 1},
                                               {True: 10, False: 1},
                                               {True: 8, False: 1}],
                  'classifier__tol': [1e-1, 1e-4, 1e-16,
                                      1e-64, 1e-256],
                  'reducer__n_components': [1, 2, 3],
                  'reducer__whiten': [True, False]
                  }

    return params


l_clf = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(tol=0.001, C=10 ** -8, penalty='l2', random_state=42))])


### K-means Clustering

from sklearn.cluster import KMeans

k_clf = KMeans(n_clusters=2, tol=0.001)

### Adaboost Classifier
from sklearn.ensemble import AdaBoostClassifier
a_clf = AdaBoostClassifier(algorithm='SAMME')

### Support Vector Machine Classifier
from sklearn.svm import SVC


def get_SVC_pipeline():
    pipeline = Pipeline(steps = [('minmaxer', MinMaxScaler()),
                                 ('selection', SelectKBest(score_func=f_classif)),
                                 ('reducer', PCA()),
                                 ('classifier', SVC())
                                 ])
    return pipeline

def get_SVC_params(full_search_params=False):
    params = {'reducer__n_components': [.5],
              'reducer__whiten': [True],
              'selection__k': [17],
              'classifier__C': [1],
              'classifier__gamma': [0.0],
              'classifier__kernel': ['rbf'],
              'classifier__tol': [1e-3],
              'classifier__class_weight': ['auto'],
              'classifier__random_state': [42],
              }

    if full_search_params:
        params = {'selection__k': [9, 15, 17, 21],
                  'classifier__C': [1e-5, 1e-2, 1e-1, 1, 10, 100],
                  'classifier__class_weight': [{True: 12, False: 1},
                                               {True: 10, False: 1},
                                               {True: 8, False: 1},
                                               {True: 15, False: 1},
                                               {True: 4, False: 1},
                                               'auto', None],
                  'classifier__tol': [1e-1, 1e-2, 1e-4, 1e-8, 1e-16,
                                      1e-32, 1e-64, 1e-128, 1e-256],
                  'reducer__n_components': [1, 2, 3, 4, 5, .25, .4, .5, .6,
                                            .75, .9, 'mle'],
                  'reducer__whiten': [True, False]
                  }

    return params

s_clf = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('classifier', SVC(kernel='rbf', C=1000))])

### Random Forest
from sklearn.ensemble import RandomForestClassifier
rf_clf = RandomForestClassifier()

### Stochastic Gradient Descent - Logistic Regression
from sklearn.linear_model import SGDClassifier
g_clf = SGDClassifier(loss='log')

### Selected Classifiers Evaluation
poi_evaluation.evaluate_clf(l_clf, features, labels)
poi_evaluation.evaluate_clf(k_clf, features, labels)

poi_evaluation.evaluate_clf(a_clf, features, labels)
poi_evaluation.evaluate_clf(s_clf, features, labels)
poi_evaluation.evaluate_clf(rf_clf, features, labels)
poi_evaluation.evaluate_clf(g_clf, features, labels)

### Final Machine Algorithm Selection
clf = l_clf

# dump your classifier, dataset and features_list so
# anyone can run/check your results
pickle.dump(clf, open("../final_project/my_classifier.pkl", "w"))
pickle.dump(my_dataset, open("../final_project/my_dataset.pkl", "w"))
pickle.dump(my_feature_list, open("../final_project/my_feature_list.pkl", "w"))