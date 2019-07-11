from sklearn.metrics import roc_auc_score, classification_report, roc_curve, confusion_matrix
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
import numpy as np
import pandas as pd


def get_most_correlated_variables(corr, num_pairs=10):
    correlation_melted = pd.melt(corr.reset_index().rename(columns={"index": "var_1"}), id_vars=("var_1"),var_name='var_2')
    correlation_melted = correlation_melted[correlation_melted.var_1!=correlation_melted.var_2]
    correlation_melted['var_couple'] = correlation_melted[['var_1','var_2']].apply(lambda x:tuple(sorted([x[0],x[1]])), axis=1)
    correlation_melted = correlation_melted.drop_duplicates(subset='var_couple').drop(['var_couple'],axis=1)
    correlation_melted['abs_value'] = correlation_melted['value'].abs().round(3)
    return correlation_melted.sort_values(by='abs_value').tail(num_pairs).drop('abs_value', axis=1).reset_index(drop=True)


def plot_correlation_matrix(X, features2):
    corr = X[features2].corr()
     # return the most correlated variables
    most_correlated_variables = get_most_correlated_variables(corr, num_pairs=10)
    max_correlation = 1.25*most_correlated_variables['value'].abs().max()
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    ax.set_yticklabels(features2, fontsize=18)
    ax.set_xticklabels(features2, rotation='vertical', fontsize=18)
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=max_correlation, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .8})
    return most_correlated_variables


def find_best_threshold(thresholds, fpr, tpr):
    """
    find the best threshold from the roc curve. by finding the threshold for the point which is closest to (fpr=0,tpr=1)
    """
    fpr_tpr = pd.DataFrame({'thresholds': thresholds, 'fpr': fpr, 'tpr': tpr})
    fpr_tpr['dist'] = (fpr_tpr['fpr'])**2 + (fpr_tpr['tpr']-1)**2
    return fpr_tpr.ix[fpr_tpr.dist.idxmin(), 'thresholds']


def get_model_results(model, train, test, y_train, y_test):
    probabilities = model.predict_proba(test)[:,1]
    fpr, tpr, thresholds = roc_curve(y_test, probabilities)
    threshold = find_best_threshold(thresholds, fpr, tpr)
    predictions = probabilities>threshold
    plt.figure()
    plt.plot(fpr, tpr, label='test')
    roc_auc = roc_auc_score(y_test, probabilities)
    probabilities = model.predict_proba(train)[:,1]
    fpr, tpr, thresholds = roc_curve(y_train, probabilities)
    plt.plot(fpr, tpr, label='train')
    plt.plot([0, 1], [0, 1], 'r--', label='random guess')
    plt.title("area under the ROC curve = {:.3f}".format(roc_auc), fontsize=18);
    print(classification_report(y_test, predictions))
    plt.legend()

    
def describe_categorical_values(df, non_interesting_columns=[], num_categories=5):
    """
    Returns:
         (chart):  the relative frequency of the top num_categories in each column
    By Shir Meir Lador
    """

    values_df = pd.DataFrame()
    for i, column in enumerate(df.columns):
        if column in non_interesting_columns:
            continue
        top_values0 = ["{}: {}%".format(x,int(round(100*y/len(df))))
                       for x, y in zip(df[column].value_counts(dropna=False).head(num_categories).index,
                                       df[column].value_counts(dropna=False).head(num_categories).values)]
        if len(top_values0) < num_categories:
            top_values = [None]*num_categories
            top_values[:len(top_values0)] = top_values0
        else:
            top_values = top_values0
        values_df[column] = top_values
    return values_df.transpose()


def remove_infrequent_values(df, categorical_columns, frequency_threshold=20):
    infrequent_cols_to_remove = []
    for cat_col in categorical_columns:
        col_count = df[cat_col].value_counts()
        infrequent_values = col_count[col_count<frequency_threshold].index.values
        if not col_count[col_count<frequency_threshold].empty:
            print("removing columns: \n{} \n".format(col_count[col_count<frequency_threshold]))
        infrequent_cols_to_remove += ["{}_{}".format(cat_col, x) for x in infrequent_values]
    return df
