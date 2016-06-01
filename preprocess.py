#!/usr/bin/env python
# coding=utf-8
#Author: Perfe
#E-mail: ieqinglinzhang@gmail.com

import xml.etree.ElementTree as ET
import jieba

def loaddata(): 
    label_dict = {}
    with open("label.txt","r") as f:
        text = f.readline().strip()
        while text:
            if text[-2] == "-":
                label_dict[text[11:-3]] = int(text[-2:])
            else:
                label_dict[text[11:-2]] = int(text[-1])
            text = f.readline().strip()        
    tree = ET.parse("COAE_weibo2015.xml")
    root = tree.getroot()
    corpus = []
    label = []
    for child in root.getchildren():
        for grandchild in child.getchildren():
            corpus.append(grandchild.text)
            if grandchild.tag in label_dict:
                if label_dict[grandchild.tag] == -1:
                    label.append((0,0))
                if label_dict[grandchild.tag] == 0:
                    label.append((0,1))
                if label_dict[grandchild.tag] == 1:
                    label.append((1,0))
            else:
                label.append((1,1))
    corpus = list(map(jieba.lcut,corpus))
    print(corpus[6:11],label[6:11])
    freq_dictionary = {}
    for sent in corpus:
        for word in sent:
            freq_dictionary[word] = freq_dictionary.setdefault(word,0)+1
#if want to change the size of dictionary, you can filter which freq is less 
    id_dictionary = {}
    sorted_list = sorted(freq_dictionary.items(),key=lambda word:word[1])
#排序，词频较高的id越小，略过id为0的，用以最后归化所有的低频词
    for i,c in enumerate(sorted_list):
        id_dictionary[c[0]] = i+1

    def char2id(char,dict=id_dictionary):
        return dict[char]

#change char in corpus to id in dict
    for i,sent in enumerate(corpus):
        corpus[i] = list(map(char2id,sent))
    #X_data是语料，为列表，元素还是列表（一句话），最内层的元素是ID
    X_data = corpus
    y_data = label
    return X_data,y_data


if __name__ == "__main__":
    x,y=loaddata()
    print(x[6:11],y[6:11])
