from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

class Trainer():
    def __init__(self):
        pass
    
    def cross_validation(self, x_train, y_train):
        log_reg_alg = LogisticRegression(random_state=1)
        loss = -cross_val_score(log_reg_alg, x_train, y_train, cv=10, scoring='mean_squared_error')
        return loss