import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
from sklearn import datasets

from sklearn.linear_model import LinearRegression

iris = datasets.load_iris()
digits = datasets.load_digits()
boston = datasets.load_boston()
bos = pd.DataFrame(boston.data)
bos['TARGET'] = boston.target

# Get features and labels
features = bos.drop('TARGET', axis = 1)
labels = bos['TARGET']

# Split into train and test features
features_train, features_test, labels_train, labels_test = sklearn.model_selection.train_test_split(features, labels, test_size = 0.33, random_state = 5)


lm = LinearRegression()
lm.fit(features_train, labels_train)
labels_pred = lm.predict(features_test)

plt.scatter(labels_test, labels_pred)
plt.xlabel("Targets")
plt.ylabel("Predicted values:")
plt.title("Targets vs Predicted values")

mse = sklearn.metrics.mean_squared_error(labels_test, labels_pred)
print(mse)
plt.show()

# https://medium.com/@haydar_ai/learning-data-science-day-9-linear-regression-on-boston-housing-dataset-cd62a80775ef