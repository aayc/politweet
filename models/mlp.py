from .learner import Learner
from sklearn.neural_network import MLPClassifier

class MLPLearner(Learner):
    classifier = None

    def fit(self, features, labels):
        self.classifier = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(20, 2), max_iter=8000)
        self.classifier.fit(features, labels)

    def predict(self, features):
        return self.classifier.predict(features)
