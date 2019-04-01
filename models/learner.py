from pandas import DataFrame

class Learner:

    def fit(self, features, labels):
        """
        :type features: DataFrame
        :type labels: DataFrame
        """
        raise NotImplementedError()

    def set_params (params):
        """
        Sets hyperparameters for the learner, very dynamic.

        :type params: dict
        """
        raise NotImplementedError()

    def predict(self, features):
        """
        A feature vector goes in. A label vector comes out.
        :type features: DataFrame
        :type labels: [float]
        """
        raise NotImplementedError()
