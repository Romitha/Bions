from sklearn import datasets


class GenerateData:

    @classmethod
    def generate_sample(cls, logger=None, number_of_records=None):
        """ Generate a numpy array with the number of sample row for Xs and Y """

        X, y = datasets.make_classification(n_samples=number_of_records, n_features=10, n_informative=6, n_redundant=2,
                                            scale=1.0, shift=0.0)
        # X_scaled = MinMaxScaler().fit_transform(X);
        # Fitting a minmaxscalar so that the X values are distributed between 0 and 1;

        return X, y
