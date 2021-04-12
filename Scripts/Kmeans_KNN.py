import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import statsmodels.api as sm

from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cluster import KMeans

## Load Data:
data = pd.read_csv("../Data/communities_rmMissing.csv")
X = data[[x for x in data.columns if x not in ["state", "communityname", "ViolentCrimesPerPop", "fold"]]]
Y = data["ViolentCrimesPerPop"]
train_prct = 0.8
n_train = int(round(X.shape[0]*train_prct))

## Models
knn = KNeighborsRegressor(n_neighbors = 5)
kmeans = KMeans(n_clusters=2, random_state=0)

## Fit
model_kmeans = kmeans.fit(X)
data["KmeansLabel"] = model_kmeans.labels_
data.to_csv("../Data/communities_kmeans.csv", index=False)

model_knn = knn.fit(X.iloc[:n_train], Y[:n_train])
residuals = Y[n_train:] - model_knn.predict(X.iloc[n_train:])

## Plot
hist_x = []
for label in set(model_kmeans.labels_):
    hist_x.append([Y[i] for i in range(len(Y)) if model_kmeans.labels_[i] == label])

plt.hist(hist_x, label=["Cluster_" + str(x) for x in set(model_kmeans.labels_)])
plt.legend()
plt.savefig("../Plots/Kmeans_hist.png")
plt.close()

plt.plot(residuals, '.')
plt.axhline(y=0, color="red")
plt.title("MSE = " + str(np.mean(residuals ** 2)))
plt.savefig("../Plots/KNN_residuals_scatter.png")
plt.close()

fig = sm.qqplot(residuals)
plt.savefig("../Plots/KNN_residuals_qqplot.png")
plt.close()
