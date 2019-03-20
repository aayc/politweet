import numpy as np
import sys
import pandas as pd
import time
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection
from sklearn.preprocessing import StandardScaler
from sklearn import datasets
from sklearn.utils import shuffle

DATA_FILE = sys.argv[1] if len(sys.argv) > 1 else "data/tmp/test.csv"
DATA_SAMPLE_PERC = float(sys.argv[2]) if len(sys.argv) > 2 else 1
print(DATA_SAMPLE_PERC)

print("USING DATA FILE", DATA_FILE, "with", DATA_SAMPLE_PERC*100, "% OF THE DATA")
print("(to change this, usage: <data-file> <percentage e.g. 0.3, 0.5, or 1>")


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
data = pd.DataFrame.from_csv(DATA_FILE)
data = data.sample(frac=DATA_SAMPLE_PERC)
targets = data["ideology"].values
targets = np.rint(targets) # round to nearest integer, so we can classify
# unique, counts = np.unique(targets, return_counts=True)
# counters = dict(zip(unique, counts))
# print(counters)

inputs = data[["x" + str(i) for i in range(300)]].values
features, labels = StandardScaler().fit_transform(inputs), targets

# Split into train and test features
features_train, features_test, labels_train, labels_test = sklearn.model_selection.train_test_split(features, labels, test_size = 0.33, random_state = 5)

for model in models:
    print('------------------------------------------------')
    name = model['name']
    print('Model: %s' % (name))
    print('Model Information: %s' % str(model["instance"]))
    print('Training...')

    start_time = time.clock()
    model['instance'].fit(features_train, labels_train)
    train_time = time.clock() - start_time

    print('Finished training in {0:.6f} seconds'.format(train_time))

    labels_pred = model['instance'].predict(features_test)
    mse = sklearn.metrics.mean_squared_error(labels_test, labels_pred)
    print('MSE: %s' % (mse))
    model['mse'] = mse
    accuracy = sklearn.metrics.accuracy_score(labels_test, labels_pred)
    print('Accuracy: %s' % (accuracy))


'''
plt.bar(
    np.arange(len(models)),
    [model['mse'] for model in models],
    tick_label=[model['name'] for model in models])
plt.ylabel('MSE')
plt.xlabel('Model Name')
plt.show()
'''

# https://medium.com/@haydar_ai/learning-data-science-day-9-linear-regression-on-boston-housing-dataset-cd62a80775ef
