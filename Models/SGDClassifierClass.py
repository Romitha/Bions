from sklearn.linear_model import SGDClassifier


class SGDClassifierClass:
    @classmethod
    def initial_model(cls, logger=None):
        """ Simulation of the iniital model setup in a traditional ML training """
        print('Simulation of the iniital model setup in a traditional ML training')

        clf = SGDClassifier(
            # loss='hinge', # hinge as a loss gives the linear SVM;
            loss='log',  # log as a loss gives the logistic regression
            # loss='perceptron', # perceptron as a loss gives perceptron
            # penalty='elasticnet', # l2 as a default for the linear SVM;
            penalty='none',  # l2 as a default for the linear SVM;
            # penalty='l2', # l2 as a default for the linear SVM;
            fit_intercept=True,  # defaults to True;
            shuffle=True,
            # shuffle after each epoch; might not have multiple epoch as the parital fit does not have max_iter
            # alpha=0.00008,
            # eta0=0.00001,
            eta0=0.001,
            # learning_rate='optimal',
            learning_rate='constant',
            average=False,  # computes the averaged SGD weights and stores the result in the coef_
            random_state=2011,
            verbose=0,
            max_iter=1000,
            warm_start=False
            # better to set the warm_start false since the multiple fit can result in diff models
            # True as an option improves the classification metrics; where False does not;
        )
        return clf
