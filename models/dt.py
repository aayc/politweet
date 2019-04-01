from .learner import Learner
from sklearn import tree

class DecisionTree(Learner):
    classifier = None

    def __init__ (self):
        pass

    def fit(self, features, labels):
        self.classifier = tree.DecisionTreeClassifier()
        self.classifier = self.classifier.fit(features, labels)

    def set_params (self, params):
        pass

    def predict(self, features):
        return self.classifier.predict(features)
