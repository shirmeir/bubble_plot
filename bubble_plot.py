
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def get_point(x, digits=2):
    a, b = x.split(',')
    a = float(a.strip("("))
    b = float(b.strip("]"))
    c = (a+b)/2
    return np.round(c,digits)


def bubble_plot(df, x, y, z_boolean=None, ordered_x_values=None, ordered_y_values=None, bins_x=10,
                bins_y=10, fontsize=16, figsize=(10,5), maximal_bubble_size=4000,
                normalization_by_all = False, log=False):
    """
    :param df: dataframe
    :param x:  name of first numerical/categorical field (string) (for x-axis)
    :param y: name of second numerical/categorical field (string) (for y-axis)
    :param z_boolean: name of categorical field with two categories / boolean field (for coloring)
    :param ordered_x_values: the values we would like to map from x categorical variable 
    according to the order we would like to present them
    :param ordered_y_values: the values we would like to map from the y categorical variable 
    according to the order we would like to present them
    :param bins_x: the bins for x values if x is numberic
    :param bins_y: the bins for y values if y is numberic
    :param normalization_by_all: True - shows joint distribution p(x,y), False - shows conditional distribution p(y|x)
    :param maximal_bubble_size: if the bubbles are too big or too small this is the parameter you should change!
    :param log: whether to apply log on the count (influence the size of the bubbles)
    :return: nice bubble plot, bubble size is propotional to the frequency of the bucket :)
    """
    plt.figure(figsize=figsize)
    x_is_numeric = df[x].dtype in (float, int) and ordered_x_values is None
    y_is_numeric = df[y].dtype in (float, int) and ordered_y_values is None 
    count_table = pd.concat([pd.cut(df[x], bins=bins_x) if x_is_numeric else df[x],
                             pd.cut(df[y], bins=bins_y) if y_is_numeric else df[y]], axis=1)
    try:
        count_table = count_table.groupby(x)[y].value_counts().unstack().fillna(0)
    except:
        count_table[x] = count_table[x].astype(str)
        count_table = count_table.groupby(x)[y].value_counts().unstack().fillna(0)
    ordered_x_values = count_table.index.values if ordered_x_values is None else ordered_x_values
    ordered_y_values = count_table.columns if ordered_y_values is None else ordered_y_values
    if z_boolean is not None:
        count_table_long, xticks, yticks, xticklabels, yticklabels = plot_with_z(df, x, y, z_boolean, bins_x, bins_y, x_is_numeric, y_is_numeric, ordered_x_values, ordered_y_values, maximal_bubble_size, 
                                                                                 normalization_by_all=normalization_by_all)
    else:
        count_table_long, xticks, yticks, xticklabels, yticklabels = plot_without_z(df, x, y, z_boolean, count_table, bins_x, bins_y, x_is_numeric, y_is_numeric, ordered_x_values, ordered_y_values, 
                                                                                    normalization_by_all=normalization_by_all, log=log, maximal_bubble_size=maximal_bubble_size )
    plt.xticks(xticks, xticklabels,fontsize=fontsize)
    plt.yticks(yticks, yticklabels,fontsize=fontsize)
    plt.xlabel(x, fontsize=fontsize)
    plt.ylabel(y, fontsize=fontsize)
    if z_boolean is None:
        plt.title("{} vs {} ".format(y,x),fontsize=fontsize+4);
    else:
        plt.title("{} vs {} and {} (in colors)".format(y,x, z_boolean),fontsize=fontsize+4);

def plot_without_z(df, x, y, z, count_table, bins_x, bins_y, x_is_numeric, y_is_numeric, ordered_x_values, ordered_y_values, normalization_by_all=False, log=False, maximal_bubble_size=4000):
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
    size_factor = maximal_bubble_size/count_table.max().max()
    count_table_long = pd.melt(count_table.reset_index(), id_vars=x)
    x_values_dict = {x:i for i, x in enumerate(ordered_x_values)} \
        if not x_is_numeric else {xx:get_point(xx) for xx in ordered_x_values}
    y_values_dict = {x:i for i, x in enumerate(ordered_y_values)} \
        if not y_is_numeric else {xx: get_point(xx) for xx in ordered_y_values}
    xticks = np.arange(count_table.shape[0]) if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticks = np.arange(count_table.shape[1]) if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    xticklabels = ordered_x_values if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticklabels = ordered_y_values if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    count_table_long[x] = count_table_long[x].map(x_values_dict)
    count_table_long[y] = count_table_long[y].map(y_values_dict) 
    plt.scatter(count_table_long[x], count_table_long[y], s=size_factor*count_table_long['value'],
                c=count_table_long['value'], cmap='cool')
 
    return count_table_long, xticks, yticks, xticklabels, yticklabels
    
def plot_with_z(df, x, y, z_boolean, bins_x, bins_y, x_is_numeric, y_is_numeric, ordered_x_values, ordered_y_values, maximal_bubble_size=4000, normalization_by_all=False):
    count_table = pd.concat([pd.cut(df[x], bins=bins_x) if x_is_numeric else df[x],
                         pd.cut(df[y], bins=bins_y) if y_is_numeric else df[y], df[z_boolean]], axis=1)
    count_table = count_table.groupby([x,z_boolean])[y].value_counts().unstack().fillna(0)
    count_table = count_table.unstack()
    count_table_long = pd.melt(count_table.reset_index(), id_vars=x)
    z_boolean_values = count_table_long[z_boolean].unique()
    ratio = pd.DataFrame({'ratio':count_table_long.set_index([x,y,z_boolean]).unstack()['value'][z_boolean_values[1]] / (
    count_table_long.set_index([x,y,z_boolean]).unstack()['value'].sum(axis=1) )})
    count_table_long = count_table_long.set_index([x, y ])[['value']].merge(ratio, left_index=True, right_index=True).reset_index()
    size_factor = maximal_bubble_size/count_table_long['value'].max()
    x_values_dict = {x:i for i, x in enumerate(ordered_x_values)} \
        if not x_is_numeric else {xx:get_point(xx) for xx in ordered_x_values}
    y_values_dict = {x:i for i, x in enumerate(ordered_y_values)} \
        if not y_is_numeric else {xx: get_point(xx) for xx in ordered_y_values}
    xticks = np.arange(len(ordered_x_values)) if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticks = np.arange(len(ordered_y_values)) if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    xticklabels = ordered_x_values if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticklabels = ordered_y_values if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    count_table_long[x] = count_table_long[x].map(x_values_dict)
    count_table_long[y] = count_table_long[y].map(y_values_dict)
    plt.scatter(count_table_long[x], count_table_long[y], s=size_factor*count_table_long['value'],
                c=count_table_long['ratio'],  alpha=0.5,
                cmap='cool')
    return count_table_long, xticks, yticks, xticklabels, yticklabels
