# -*- coding: utf-8 -*-
"""
Created on Sat Jan  3 13:30:05 2015

@author: ericwu
"""
from sklearn.cross_validation import KFold
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from numpy import *

class PCAApproach:
    def __init__(self, n_components = 5, n_folds = 10):
        self.n_components = n_components
        self.n_folds = n_folds

        
    def setPCAComponents(self, n_components):
        self.n_components = n_components
        
    def getPCAComponents(self):
        return self.n_components
        
    def setFoldNumber(self, n_folds):
        self.n_folds = n_folds
        
    def getFoldNumber(self):
        return self.n_folds
        
    def fit(self, features, labels):
        kf = KFold(len(features), n_folds = self.n_folds)
        self.accuracy_list = []
        self.pca_list = []
        self.clf_list = []

        for train_index, test_index in kf:
            features_train, features_test = features[train_index], features[test_index]
            labels_train, labels_test = labels[train_index], labels[test_index]
            
        
            ### machine learning goes here!
            ### please name your classifier clf for easy export below
            
            # Using the pca to transform the training set
            pca = PCA(n_components=self.n_components, whiten=True).fit(features_train)
            
            features_train_pca = pca.transform(features_train)
            features_test_pca = pca.transform(features_test)
            
            
            #clf = None    ### get rid of this line!  just here to keep code from crashing out-of-box
            #from sklearn.tree import DecisionTreeClassifier
            #clf = DecisionTreeClassifier()
            #clf.fit(features_train_pca, labels_train)
            #print clf.score(features_test_pca, labels_test)
            
            
            clf = SVC(C=1, gamma=0)
            clf.fit(features_train_pca, labels_train)
            accuracy = clf.score(features_test_pca, labels_test)
            self.accuracy_list.append(accuracy)
            self.pca_list.append(pca)
            self.clf_list.append(clf)
        
    def getAccuracyList(self):
        if not self.accuracy_list:
            return None
        else:
            return self.accuracy_list
                
    def getAverageAccuracy(self):
        if not self.accuracy_list:
            return None
        else:
            return mean(self.accuracy_list)
                
    def getBestPCA(self):
            bestArgument = argmax(self.accuracy_list)
            return self.pca_list[bestArgument]
            
    def getBestSVMClassifier(self):
            bestArgument = argmax(self.accuracy_list)
            return self.clf_list[bestArgument]
        
        
if __name__ == '__main__':
    pcaA = PCAApproach()
    pcaA.setFoldNumber(20)
    print pcaA.getFoldNumber()