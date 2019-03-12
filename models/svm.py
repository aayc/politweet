from .learner import Learner
from sklearn import svm

class SVMLearner(Learner):
    classifier = None

    def fit(self, features, labels):
        self.classifier = svm.SVC()
        self.classifier.fit(features, labels)

    def predict(self, features):
        return self.classifier.predict(features)