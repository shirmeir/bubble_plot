

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def bubble_plot(df, x, y, z_boolean=None, ordered_x_values=None, ordered_y_values=None, bins_x=10,
                bins_y=10, fontsize=16, figsize=(10, 5), maximal_bubble_size=3500,
                normalization_by_all=False, log=False):
    """
    The goal for the bubble plot is to help us visualize linear and non-linear connections between numerical/categorical
    features in our data in an easy and simple way. The bubble plot is a kind of a 2-dimensional histogram using bubbles.
    The bubble size is proportional to the frequency of the data points in this point.
    Arguments:
        df (~pandas.DataFrame): the data frame to use.
        x (str): name of first numerical/categorical field (string) (for x-axis)
        y: name of second numerical/categorical field (string) (for y-axis)
        z_boolean: name of categorical field with two categories / boolean field (for coloring)
        ordered_x_values: the values we would like to map from x categorical variable according to the order we would like to present them
        ordered_y_values: the values we would like to map from the y categorical variable according to the order we would like to present them
        bins_x: the bins for x values if x is numberic
        bins_y: the bins for y values if y is numberic
        normalization_by_all: True - shows joint distribution p(x,y), False - shows conditional distribution p(y|x)
        maximal_bubble_size: if the bubbles are too big or too small this is the parameter you should change.
        log: whether to apply log on the count (influence the size of the bubbles)
    Returns:
         (plot): nice bubble plot, bubble size is proportional to the frequency of the bucket :)
    By Shir Meir Lador
    :Example:
        *Custom Message*
        .. code-block:: python
            import pandas as pd
            from sklearn.datasets import load_boston
            data = load_boston()
            df = pd.DataFrame(columns=data['feature_names'], data=data['data'])
            df['target'] = data['target']
            bubble_plot(df, x='RM', y='target')
        .. note::
            For numerical features the values will be presented in buckets (ten equally spaced bins will be used as default,
            you can provide the specific bins / bins number through the `bin_x` and `bins_y` parameters).
            For categorical features the features will be presented according to their categories.
            If you would like a specific order for the categories presentation please supply a list of the values by order using the `ordered_x_values` / `ordered_y_values` parameters.
            You can plot a numerical feature vs. another numerical feature or vs. a categorical feature or a categorical feature vs another categorical feature or numerical feature. All options are possible.
            Setting the `log` parameter to `True` would apply the natural log function - element wise - on the counts which will make the differences between the largest bubble to the smallest bubble much smaller, so if you have large differences between the frequencies of different values you might want to use that.
            Setting the `z_boolean` parameter to a name of categorical field with two categories / boolean field would make the color of the bucket  be proportional to the ratio ( (boolean_z==value_1).sum()/(boolean_z==value_1).sum() + (boolean_z==value_2).sum()) of the z values for this bucket.
    """

    plt.figure(figsize=figsize)
    x_is_numeric = df[x].dtype in (float, int) and ordered_x_values is None
    y_is_numeric = df[y].dtype in (float, int) and ordered_y_values is None
    count_table = pd.concat([pd.cut(df[x], bins=bins_x) if x_is_numeric else df[x],
                             pd.cut(df[y], bins=bins_y) if y_is_numeric else df[y]], axis=1)

    count_table[x] = count_table[x].astype(str)
    count_table = count_table.groupby(x)[y].value_counts().unstack().fillna(0)
    count_table = count_table.rename({x:str(x) for x in count_table.columns},axis=1)
    ordered_x_values = sorted(count_table.index.values) if ordered_x_values is None else ordered_x_values
    ordered_y_values = sorted(count_table.columns) if ordered_y_values is None else ordered_y_values
    if z_boolean is not None:
        count_table_long, xticks, yticks, xticklabels, yticklabels = plot_with_z(df, x, y, z_boolean, bins_x, bins_y,
                                                                                 x_is_numeric, y_is_numeric,
                                                                                 ordered_x_values, ordered_y_values,
                                                                                 maximal_bubble_size,
                                                                                 normalization_by_all=normalization_by_all)
    else:
        count_table_long, xticks, yticks, xticklabels, yticklabels = plot_without_z(df, x, y, z_boolean, count_table,
                                                                                    bins_x, bins_y, x_is_numeric,
                                                                                    y_is_numeric, ordered_x_values,
                                                                                    ordered_y_values,
                                                                                    normalization_by_all=normalization_by_all,
                                                                                    log=log,
                                                                                    maximal_bubble_size=maximal_bubble_size)
    plt.xticks(xticks, xticklabels, fontsize=fontsize)
    plt.yticks(yticks, yticklabels, fontsize=fontsize)
    plt.xlabel(x, fontsize=fontsize)
    plt.ylabel(y, fontsize=fontsize)
    if z_boolean is None:
        plt.title("{} vs {} ".format(y, x), fontsize=fontsize + 4);
    else:
        plt.title("{} vs {} and {} (in colors)".format(y, x, z_boolean), fontsize=fontsize + 4);


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

def plot_without_z(df, x, y, z, count_table, bins_x, bins_y, x_is_numeric, y_is_numeric, ordered_x_values,
                   ordered_y_values, normalization_by_all=False, log=False, maximal_bubble_size=4000):
    if normalization_by_all:
        count_table /= count_table.sum().sum()
    else:
        count_table = count_table.transpose()
        for col in count_table.columns:
            count_table[col] /= count_table[col].sum()
        count_table = count_table.transpose()
    if log:
        count_table = np.log(count_table)
        maximal_bubble_size /= 2
    size_factor = maximal_bubble_size / count_table.max().max()
    count_table = count_table.rename({x:str(x) for x in count_table.columns},axis=1)

    count_table_long = pd.melt(count_table.reset_index(), id_vars=x)
    ordered_x_values = [str(x) for x in ordered_x_values]
    x_values_dict = {x: i for i, x in enumerate(ordered_x_values)} if not x_is_numeric else {xx: get_point(xx) for xx in
                                                                                             ordered_x_values}
    y_values_dict = {x: i for i, x in enumerate(ordered_y_values)} if not y_is_numeric else {xx: get_point(xx) for xx in
                                                                                             ordered_y_values}
    xticks = np.arange(count_table.shape[0]) if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticks = np.arange(count_table.shape[1]) if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    xticklabels = ordered_x_values if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticklabels = ordered_y_values if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    count_table_long[x] = count_table_long[x].map(x_values_dict)
    count_table_long[y] = count_table_long[y].map(y_values_dict)
    plt.scatter(count_table_long[x], count_table_long[y], s=size_factor * count_table_long['value'],
                c=count_table_long['value'], cmap='cool')

    return count_table_long, xticks, yticks, xticklabels, yticklabels


def get_point(x, digits=2):
    if not isinstance(x, pd.Interval):
        a, b = x.split(',')
        a = float(a.strip("("))
        b = float(b.strip("]"))
    else:
        a, b = x.left, x.right
    c = (a + b) / 2
    return np.round(c, digits)


def plot_with_z(df, x, y, z_boolean, bins_x, bins_y, x_is_numeric, y_is_numeric, ordered_x_values,
                ordered_y_values, maximal_bubble_size=4000, normalization_by_all=False):
    count_table = pd.concat([pd.cut(df[x], bins=bins_x) if x_is_numeric else df[x],
                             pd.cut(df[y], bins=bins_y) if y_is_numeric else df[y], df[z_boolean]], axis=1)
    count_table = count_table.groupby([x, z_boolean])[y].value_counts().unstack().fillna(0)
    count_table = count_table.unstack().unstack()
    count_table_long = count_table.reset_index().rename(
        columns={0: 'value'})  # pd.melt(count_table.reset_index(), id_vars=x)
    z_boolean_values = count_table_long[z_boolean].unique()
    ratio = pd.DataFrame(
        {'ratio': count_table_long.set_index([x, y, z_boolean]).unstack()['value'][z_boolean_values[1]] / (
            count_table_long.set_index([x, y, z_boolean]).unstack()['value'].sum(axis=1))})
    count_table_long = count_table_long.set_index([x, y])[['value']].merge(ratio, left_index=True,
                                                                           right_index=True).reset_index()
    size_factor = maximal_bubble_size / count_table_long['value'].max()
    x_values_dict = {x: i for i, x in enumerate(ordered_x_values)} if not x_is_numeric else {xx: get_point(xx) for xx in
                                                                                             ordered_x_values}
    y_values_dict = {x: i for i, x in enumerate(ordered_y_values)} if not y_is_numeric else {xx: get_point(xx) for xx in
                                                                                             ordered_y_values}
    xticks = np.arange(len(ordered_x_values)) if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticks = np.arange(len(ordered_y_values)) if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    xticklabels = ordered_x_values if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticklabels = ordered_y_values if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    count_table_long[x] = count_table_long[x].astype(str).map(x_values_dict)
    count_table_long[y] = count_table_long[y].astype(str).map(y_values_dict)
    plt.scatter(count_table_long[x], count_table_long[y], s=size_factor * count_table_long['value'],
                c=count_table_long['ratio'], alpha=0.5,
                cmap='cool')
    return count_table_long, xticks, yticks, xticklabels, yticklabels
