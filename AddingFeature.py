# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 13:58:48 2015

@author: ericwu
"""
from __future__ import division


class AddingFeature:
    def __init__(self, data_dict, features_list):
        self.data_dict = data_dict
        self.features_list = features_list
        
    def duplicate_feature(self, duplicate_feature_name, new_feature_name):
        self.features_list.append(new_feature_name)
        
        for key in self.data_dict:
            self.data_dict[key][new_feature_name] = self.data_dict[key][duplicate_feature_name]
            
    def delete_feature(self, delete_feature_name):
        self.features_list.remove(delete_feature_name)
        
        for key in self.data_dict:
            self.data_dict[key].pop(delete_feature_name)
        
    def calculate_feature(self, feature_one, feature_two, new_name, function = 'add'):
        if function == 'add':
            for key in self.data_dict:
                if self.data_dict[key][feature_one] == 'NaN':
                    self.data_dict[key][feature_one] = 0
                if self.data_dict[key][feature_two] == 'NaN':
                    self.data_dict[key][feature_two] = 0
                    
                self.data_dict[key][new_name] = self.data_dict[key][feature_one] + self.data_dict[key][feature_two]
                
        elif function == 'substract':
            for key in self.data_dict:
                if self.data_dict[key][feature_one] == 'NaN':
                    self.data_dict[key][feature_one] = 0
                if self.data_dict[key][feature_two] == 'NaN':
                    self.data_dict[key][feature_two] = 0
                    
                self.data_dict[key][new_name] = self.data_dict[key][feature_one] - self.data_dict[key][feature_two]
                
        elif function == 'multiply':
            for key in self.data_dict:
                if self.data_dict[key][feature_one] == 'NaN':
                    self.data_dict[key][feature_one] = 0
                if self.data_dict[key][feature_two] == 'NaN':
                    self.data_dict[key][feature_two] = 0
                    
                self.data_dict[key][new_name] = self.data_dict[key][feature_one] * self.data_dict[key][feature_two]
           
        elif function == 'divide':
            for key in self.data_dict:
                if self.data_dict[key][feature_one] == 'NaN':
                    self.data_dict[key][feature_one] = 0
                if self.data_dict[key][feature_two] == 'NaN':
                    self.data_dict[key][feature_two] = 0
                    
                if self.data_dict[key][feature_two] == 0:
                    self.data_dict[key][new_name] = 0
                else:
                    self.data_dict[key][new_name] = self.data_dict[key][feature_one]/self.data_dict[key][feature_two]
                
    def get_current_features_list(self):
        return self.features_list
        
    def get_current_data_dict(self):
        return self.data_dict