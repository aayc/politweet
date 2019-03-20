from .learner import Learner
from sklearn.neural_network import MLPClassifier

class MLPLearner(Learner):
    classifier = None

    def __init__ (self):
        self.HIDDEN_LAYERS = (100, 100, 100)

    def fit(self, features, labels):
        self.classifier = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=self.HIDDEN_LAYERS, max_iter=8000)
        self.classifier.fit(features, labels)

    def predict(self, features):
        return self.classifier.predict(features)

    def __str__ (self):
        return "MLP " + str(len(self.HIDDEN_LAYERS)) + " layers, " + str(self.HIDDEN_LAYERS)

