#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import pickle
sys.path.append("./tools/")


from feature_format import featureFormat
from feature_format import targetFeatureSplit

import numpy as np
import myTools

##############################################################################
### features_list is a list of strings, each of which is a feature name      #
### first feature must be "poi", as this will be singled out as the label    #
##############################################################################
features_list = []
                 
email_features_list = ['to_messages', 'from_poi_to_this_person',
                       'from_messages', 'from_this_person_to_poi',
                       'shared_receipt_with_poi']
                 
financial_features_list = ['salary', 'deferral_payments', 'total_payments',
                  'loan_advances', 'bonus', 'restricted_stock_deferred',
                  'deferred_income', 'total_stock_value', 'expenses',
                  'exercised_stock_options', 'other', 'long_term_incentive',
                  'restricted_stock', 'director_fees']
                  
target_label = ['poi']

# total features list: The first one should be 'poi' (target label)
total_features_list = target_label + email_features_list + financial_features_list

# financial features list with target label
financial_features_list = target_label + financial_features_list

# email features list with target label
email_features_list = target_label + email_features_list                 


              

### load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### we suggest removing any outliers before proceeding further

### if you are creating any new features, you might want to do that here
### store to my_dataset for easy export below
my_dataset = data_dict

# This step only selects the features which the available data > 82
selected_features_list = myTools.select_features_by_num(my_dataset, total_features_list, threshold = 82)
features_list = selected_features_list




# Remove the "TOTAL" and "THE TRAVEL AGENCY IN THE PARK" data point (outliers)
my_dataset.pop('TOTAL', 0)
my_dataset.pop('THE TRAVEL AGENCY IN THE PARK', 0)


# Import AddingFeature class to add new feature
from AddingFeature import AddingFeature
addFeature = AddingFeature(my_dataset, features_list)
addFeature.duplicate_feature("exercised_stock_options", "exercised_stock_options_1")

features_list = addFeature.get_current_features_list()
my_dataset = addFeature.get_current_data_dict()


### these two lines extract the features specified in features_list
### and extract them from data_dict, returning a numpy array
data = featureFormat(my_dataset, features_list)







### if you are creating new features, could also do that here


##############################################################################
### split into labels and features (this line assumes that the first         #
### feature in the array is the label, which is why "poi" must always        #
### be first in features_list                                                #
##############################################################################

labels, features = targetFeatureSplit(data)

# Preprocessing the data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
features = scaler.fit_transform(features)

# Using feature selection to select the feature
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
k = 6
selectKB = SelectKBest(f_classif, k = k)
features = selectKB.fit_transform(features, labels)
index = selectKB.get_support().tolist()

new_features_list = []
for i in range(len(index)):
    if index[i]:
        new_features_list.append(features_list[i+1])
        
# Insert poi to the first element
new_features_list.insert(0, "poi")


from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV

skf = StratifiedKFold( labels, n_folds=3 )
accuracies = []
precisions = []
recalls = []


from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


for train_idx, test_idx in skf: 
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
    for jj in test_idx:
        features_test.append( features[jj] )
        labels_test.append( labels[jj] )
    
    ### fit the classifier using training set, and test on test set
    

#    parameter = {'base_estimator':[None, DecisionTreeClassifier(),
#                                   RandomForestClassifier()],
#                                   'n_estimators':[20, 50]}
    
    # Here comes weird part                               
    parameter = {'base_estimator':[None],
                                   'n_estimators':[50]}

    adaBoost = AdaBoostClassifier(learning_rate = 1, random_state = 0, algorithm='SAMME.R')
    clf = GridSearchCV(adaBoost, parameter)
#    base_estimator = RandomForestClassifier()
#    clf = AdaBoostClassifier(base_estimator = None ,n_estimators = 50, learning_rate = 1, random_state = 0, algorithm='SAMME.R')
#    clf = RandomForestClassifier(n_estimators = 2, random_state = 0)    
    
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    
    accuracy = clf.score(features_test, labels_test) 
    

    ### for each fold, print some metrics
    print
    print "Accuracy: %f " %accuracy
    print "precision score: ", precision_score( labels_test, pred )
    print "recall score: ", recall_score( labels_test, pred )
    
    accuracies.append(accuracy)
    precisions.append( precision_score(labels_test, pred) )
    recalls.append( recall_score(labels_test, pred) )

### aggregate precision and recall over all folds
print "average accuracy: ", sum(accuracies)/3.
print "average precision: ", sum(precisions)/3.
print "average recall: ", sum(recalls)/3.





features_list = new_features_list
data_dict = my_dataset


####################################################################
### dump your classifier, dataset and features_list so             #
### anyone can run/check your results                              #
####################################################################

pickle.dump(clf, open("my_classifier.pkl", "w") )
pickle.dump(data_dict, open("my_dataset.pkl", "w") )
pickle.dump(features_list, open("my_feature_list.pkl", "w") )



