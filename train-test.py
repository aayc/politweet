import numpy as np
import pandas as pd
import time
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection
from sklearn.preprocessing import StandardScaler
from sklearn import datasets

# Models
from models.mlp import MLPLearner
from models.svm import SVMLearner

models = [
    {
        'name': 'Support Vector Machine',
        'instance': SVMLearner()
    },
    {
        'name': 'Multilayer Perceptron',
        'instance': MLPLearner()
    }
]

iris = datasets.load_iris()
features, labels = StandardScaler().fit_transform(iris.data), iris.target

# Split into train and test features
features_train, features_test, labels_train, labels_test = sklearn.model_selection.train_test_split(features, labels, test_size = 0.33, random_state = 5)

for model in models:
    print('------------------------------------------------')
    name = model['name']
    print('Model: %s' % (name))
    print('Training...')

    start_time = time.clock()
    model['instance'].fit(features_train, labels_train)
    train_time = time.clock() - start_time

    print('Finished training in {0:.6f} seconds'.format(train_time))

    labels_pred = model['instance'].predict(features_test)
    mse = sklearn.metrics.mean_squared_error(labels_test, labels_pred)
    print('MSE: %s' % (mse))
    model['mse'] = mse

plt.bar(
    np.arange(len(models)),
    [model['mse'] for model in models],
    tick_label=[model['name'] for model in models])
plt.ylabel('MSE')
plt.xlabel('Model Name')
plt.show()

# https://medium.com/@haydar_ai/learning-data-science-day-9-linear-regression-on-boston-housing-dataset-cd62a80775ef
