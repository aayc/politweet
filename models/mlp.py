from .learner import Learner
from sklearn.neural_network import MLPClassifier

class MLPLearner(Learner):
    classifier = None

    def __init__ (self):
        self.HIDDEN_LAYERS = (100, 100, 100)
        self.ALPHA = 1e-5
        self.MAX_ITERS = 8000

    def fit(self, features, labels):
        self.classifier = MLPClassifier(solver='sgd', alpha=self.ALPHA, hidden_layer_sizes=self.HIDDEN_LAYERS, max_iter=self.MAX_ITERS)
        self.classifier.fit(features, labels)

    def set_params (self, params):
        self.HIDDEN_LAYERS = params.get("hidden_layers", self.HIDDEN_LAYERS)
        self.ALPHA = params.get("alpha", self.ALPHA)
        self.MAX_ITERS = params.get("max_iters", self.MAX_ITERS)

    def predict(self, features):
        return self.classifier.predict(features)

    def __str__ (self):
        return "MLP " + str(len(self.HIDDEN_LAYERS)) + " layers, " + str(self.HIDDEN_LAYERS)

