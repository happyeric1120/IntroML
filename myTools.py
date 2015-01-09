# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 10:11:58 2015

@author: ericwu
"""

def calculate_available_num_features(data_dict, features_name):
    ctr = 0
    for i in data_dict.keys():
        if data_dict[i][features_name] != 'NaN':
            ctr += 1
    return ctr
    
    
def calculate_available_num_features_list(data_dict, features_list):
    num_list = []    
    for feature in features_list:
        num_list.append(calculate_available_num_features(data_dict, feature))
    return num_list
    
def select_features_by_num(data_dict, features_list, threshold = 0):
    num_list = calculate_available_num_features_list(data_dict, features_list)
    selected_features = []
    
    for i in range(len(num_list)):
        if num_list[i] > threshold:
            selected_features.append(features_list[i])
            
    return selected_features