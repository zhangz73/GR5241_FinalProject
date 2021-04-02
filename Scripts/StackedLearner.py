import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import statsmodels.api as sm

from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostRegressor
from sklearn.cluster import KMeans
from sklearn.ensemble import StackingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import BayesianRidge

## Load Data:
data = pd.read_csv("../Data/communities_rmMissing.csv")
X = data[[x for x in data.columns if x not in ["state", "communityname", "ViolentCrimesPerPop", "fold"]]]
Y = data["ViolentCrimesPerPop"]
N = data.shape[0]

N_FOLDS = 5
#shuffle_idx = np.random.permutation(Y.size)
#X = X.iloc[shuffle_idx]
#Y = Y[shuffle_idx]
X = np.array(X)
Y = np.array(Y)

## hold out 20 percent of data for testing accuracy
train_prct = 0.8
n_train = int(round(X.shape[0]*train_prct))

## Models
knn = KNeighborsRegressor(n_neighbors=5)
svm = SVR()
rf = RandomForestRegressor(n_estimators=100, criterion='mse', random_state=0)
decision_tree = DecisionTreeRegressor(max_depth=3, max_features=2)
bayesian_ridge = BayesianRidge()

base_models = [("KNN", knn), ("SVM", svm), ("DecisionTree", decision_tree), ("RandomForest", rf)]

## Fit
stacked_learner = StackingRegressor(base_models, cv=N_FOLDS)
stacked_learner = stacked_learner.fit(X[:n_train], Y[:n_train])
y_pred_test = stacked_learner.predict(X[n_train:])
residuals_stacked = Y[n_train:] - y_pred_test

adaboost = AdaBoostRegressor(n_estimators=100, loss="square", random_state=0)
adaboost = adaboost.fit(X[:n_train], Y[:n_train])
y_pred_test = adaboost.predict(X[n_train:])
residuals_adaboost = Y[n_train:] - y_pred_test

## Plot
plt.plot(residuals_stacked, '.')
plt.axhline(y=0, color="red")
plt.title("Stacked Learners\nMSE = " + str(np.mean(residuals_stacked ** 2)))
plt.savefig("../Plots/StackedLearner_residuals_scatter.png")
plt.close()
plt.plot(residuals_adaboost, '.')
plt.axhline(y=0, color="red")
plt.title("Adaboost\nMSE = " + str(np.mean(residuals_adaboost ** 2)))
plt.savefig("../Plots/Adaboost_residuals_scatter.png")
plt.close()

fig = sm.qqplot(residuals_stacked)
plt.savefig("../Plots/StackedLearner_residuals_qqplot.png")
plt.close()
fig = sm.qqplot(residuals_adaboost)
plt.savefig("../Plots/Adaboost_residuals_qqplot.png")
plt.close()
