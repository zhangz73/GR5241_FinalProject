import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import MinMaxScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier

## Load Data:
#with open("../Data/communities.data", "r") as f:
#    lines = f.readlines()
#    data = [line.strip().split(",") for line in lines]
#
#with open("../Data/Attributes.txt", "r") as f:
#    attributes = f.readlines()
#    attributes = [x.strip("\n") for x in attributes]
#
#with open("../Data/communities.csv", "w") as f:
#    f.write(",".join(attributes) + "\n")
#    for line in lines:
#        f.write(line)
data = pd.read_csv("../Data/communities.csv")

## Classifiers
#dt = DecisionTreeClassifier()
#knn = KNeighborsClassifier(n_neighbors = 3)
#svm = SVC(C = 1, gamma = 2)
#nb = GaussianNB()
#adaboost = AdaBoostClassifier(DecisionTreeClassifier(max_depth = 3),
#                                                    n_estimators = 30)
