#!/usr/bin/python
import csv
import matplotlib.pyplot as plt
import pickle
import sys
import pandas as pd
sys.path.append("../tools/")

from feature_format import featureFormat
from feature_format import targetFeatureSplit

from sklearn.feature_selection import SelectKBest

def remove_keys(dict_object, keys):
    """ removes a list of keys from a dict object """
    for key in keys:
        dict_object.pop(key, 0)

def make_csv(data_dict):
    """ generates a csv file from a data set """
    fieldnames = ['name'] + data_dict.itervalues().next().keys()
    with open('data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in data_dict:
            person = data_dict[record]
            person['name'] = record
            assert set(person.keys()) == set(fieldnames)
            writer.writerow(person)

def visualize(data_dict, feature_x, feature_y):
    """ generates a plot of feature y vs feature x, colors poi """

    data = featureFormat(data_dict, [feature_x, feature_y, 'poi'])

    for point in data:
        x = point[0]
        y = point[1]
        poi = point[2]
        color = 'red' if poi else 'blue'
        plt.scatter(x, y, color=color)
    plt.xlabel(feature_x)
    plt.ylabel(feature_y)
    plt.show()


def add_poi_interaction(data_dict, features_list):
    """ mutates data dict to add proportion of email interaction with pois """
    fields = ['to_messages', 'from_messages',
              'from_poi_to_this_person', 'from_this_person_to_poi']
    for record in data_dict:
        person = data_dict[record]
        is_valid = True
        for field in fields:
            if person[field] == 'NaN':
                is_valid = False
        if is_valid:
            total_messages = person['to_messages'] +\
                             person['from_messages']
            poi_messages = person['from_poi_to_this_person'] +\
                           person['from_this_person_to_poi']
            person['poi_interaction'] = float(poi_messages) / total_messages
        else:
            person['poi_interaction'] = 'NaN'
    features_list += ['poi_interaction']

def add_financial_aggregate(data_dict, features_list):
    """ mutates data dict to add aggregate values from stocks and salary """
    fields = ['total_stock_value', 'exercised_stock_options', 'salary']
    for record in data_dict:
        person = data_dict[record]
        is_valid = True
        for field in fields:
            if person[field] == 'NaN':
                is_valid = False
        if is_valid:
            person['financial_aggregate'] = sum([person[field] for field in fields])
        else:
            person['financial_aggregate'] = 'NaN'
    features_list += ['financial_aggregate']

def count_valid_values(data_dict):
    """ counts the number of non-NaN values for each feature """
    counts = dict.fromkeys(data_dict.itervalues().next().keys(), 0)
    for record in data_dict:
        person = data_dict[record]
        for field in person:
            if person[field] != 'NaN':
                counts[field] += 1
    return counts


def get_k_best(data_dict, features_list, k):
    """ runs scikit-learn's SelectKBest feature selection
        returns dict where keys=features, values=scores
    """
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)

    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_
    unsorted_pairs = zip(features_list[1:], scores)
    sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
    k_best_features = dict(sorted_pairs[:k])
    print "{0} best features:\n {1}\n ".format(k, k_best_features)
    return k_best_features

# Data overview

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))


# Fixes the 2 records found with values not matching the PDF file
def fix_records(data_dict):
    data_dict['BELFER ROBERT'] = {'bonus': 'NaN',
                                  'deferral_payments': 'NaN',
                                  'deferred_income': -102500,
                                  'director_fees': 102500,
                                  'email_address': 'NaN',
                                  'exercised_stock_options': 'NaN',
                                  'expenses': 3285,
                                  'from_messages': 'NaN',
                                  'from_poi_to_this_person': 'NaN',
                                  'from_this_person_to_poi': 'NaN',
                                  'loan_advances': 'NaN',
                                  'long_term_incentive': 'NaN',
                                  'other': 'NaN',
                                  'poi': False,
                                  'restricted_stock': -44093,
                                  'restricted_stock_deferred': 44093,
                                  'salary': 'NaN',
                                  'shared_receipt_with_poi': 'NaN',
                                  'to_messages': 'NaN',
                                  'total_payments': 3285,
                                  'total_stock_value': 'NaN'}

    data_dict['BHATNAGAR SANJAY'] = {'bonus': 'NaN',
                                     'deferral_payments': 'NaN',
                                     'deferred_income': 'NaN',
                                     'director_fees': 'NaN',
                                     'email_address': 'sanjay.bhatnagar@enron.com',
                                     'exercised_stock_options': 15456290,
                                     'expenses': 137864,
                                     'from_messages': 29,
                                     'from_poi_to_this_person': 0,
                                     'from_this_person_to_poi': 1,
                                     'loan_advances': 'NaN',
                                     'long_term_incentive': 'NaN',
                                     'other': 'NaN',
                                     'poi': False,
                                     'restricted_stock': 2604490,
                                     'restricted_stock_deferred': -2604490,
                                     'salary': 'NaN',
                                     'shared_receipt_with_poi': 463,
                                     'to_messages': 523,
                                     'total_payments': 137864,
                                     'total_stock_value': 15456290}
    return data_dict

if __name__ == '__main__':
    outliers = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
    remove_keys(data_dict, outliers)
    make_csv(data_dict)
    visualize(data_dict, 'salary', 'bonus')
    visualize(data_dict, 'from_poi_to_this_person', 'from_this_person_to_poi')

    features_list = ['poi',
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
                     'from_messages',
                     'from_poi_to_this_person',
                     'from_this_person_to_poi',
                     'shared_receipt_with_poi',
                     'to_messages']

    add_poi_interaction(data_dict, features_list)
    visualize(data_dict, 'total_stock_value', 'poi_interaction')

    add_financial_aggregate(data_dict, features_list)
    visualize(data_dict, 'poi_interaction', 'financial_aggregate')

    total = len(data_dict)
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    poi_count = df[df.poi == 1].shape[0]
    other = total - poi_count

    print "total number of data points", len(data_dict)
    print "POI : {}, notPOI: {} ({:0%} POI)".format(poi_count, other, float(poi_count) / total)
    print "features ({} total): ".format(df.dtypes.count())
    for c in list(df):
        nans = df[c][df[c] == 'NaN'].count() if df[c].dtype == object else 0
        print ' - {} : {:.0%} empty, {} valid'.format(c, float(nans) / total, int(total - nans))

    k_best = get_k_best(data_dict, features_list, 9)
