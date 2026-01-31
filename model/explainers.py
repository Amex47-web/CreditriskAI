import shap
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict

class Explainer:
    def __init__(self, model_wrapper):
        """
        Initialize SHAP explainer.
        :param model_wrapper: Instance of RiskModel containing the trained XGBoost model.
        """
        self.model = model_wrapper.model
        self.feature_names = model_wrapper.features
        # Create explainer (TreeExplainer is optimized for Trees)
        self.explainer = shap.TreeExplainer(self.model)

    def explain_prediction(self, X_row: pd.DataFrame) -> Dict[str, float]:
        """
        Generate SHAP values for a single prediction.
        :return: Dictionary of {feature: shap_value}
        """
        X_row = X_row[self.feature_names]
        shap_values = self.explainer.shap_values(X_row)
        
        # For GradientBoostingClassifier (binary), shap_values is an array of shape (n_samples, n_features)
        # It does NOT return a list of arrays like XGBoost sometimes does
        if isinstance(shap_values, list): 
             vals = shap_values[1][0] # Should not happen for Sklearn GBC usually
        elif len(shap_values.shape) > 1 and shap_values.shape[0] == 1:
             vals = shap_values[0]
        else:
             vals = shap_values
                
        explanation = dict(zip(self.feature_names, vals))
        return explanation

    def plot_summary(self, X_sample: pd.DataFrame):
        """
        Save a summary plot for a batch of data.
        """
        X_sample = X_sample[self.feature_names]
        shap_values = self.explainer.shap_values(X_sample)
        shap.summary_plot(shap_values, X_sample, show=False)
        plt.savefig("shap_summary.png")
        plt.close()

if __name__ == "__main__":
    from train import RiskModel
    rm = RiskModel()
    # Ensure model is trained/loaded
    if not hasattr(rm.model, 'feature_importances_'):
         X, y = rm.create_synthetic_data(100)
         rm.train(X, y)
    
    exp = Explainer(rm)
    X_single = rm.create_synthetic_data(1)[0].iloc[[0]]
    print(exp.explain_prediction(X_single))
