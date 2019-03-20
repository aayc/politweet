from .learner import Learner
from sklearn import tree

class DecisionTree(Learner):
    classifier = None

    def fit(self, features, labels):
        self.classifier = tree.DecisionTreeClassifier()
        self.classifier = self.classifier.fit(features, labels)

    def predict(self, features):
        return self.classifier.predict(features)