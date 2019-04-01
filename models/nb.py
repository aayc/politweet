from .learner import Learner
from sklearn.naive_bayes import GaussianNB

class NaiveBayes(Learner):
    classifier = None

    def fit(self, features, labels):
        self.classifier = GaussianNB()
        self.classifier.fit(features, labels)

    def set_params (self, params):
        pass

    def predict(self, features):
        return self.classifier.predict(features)
