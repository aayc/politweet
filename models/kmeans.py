from .learner import Learner
from sklearn.cluster import KMeans

class kMeansLearner(Learner):
    classifier = None

    def __init__ (self):
        self.K = 4

    def fit(self, features, labels):
        self.classifier = KMeans(n_clusters=2, random_state=0)
        self.classifier = self.classifier.fit(features, labels)

    def set_params (self, params):
        self.K = params.get("k", self.K)

    def predict(self, features):
        return self.classifier.predict(features)