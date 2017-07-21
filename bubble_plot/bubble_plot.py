import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def get_point(x, digits=2):
    a, b = x.split(',')
    a = float(a.strip("("))
    b = float(b.strip("]"))
    c = (a+b)/2
    return np.round(c,digits)


def bubble_plot(df, x, y, ordered_x_values=None, ordered_y_values=None, bins_x=10,
                bins_y=10, fontsize=16, figsize=(15,10), maximal_bubble_size=5000,
                normalization_by_all = False, log=False):
    plt.figure(figsize=figsize)
    x_is_numeric = df[x].dtype in (float, int)
    y_is_numeric = df[y].dtype in (float, int)
    count_table = pd.concat([pd.cut(df[x], bins=bins_x) if x_is_numeric else df[x],
                             pd.cut(df[y], bins=bins_y) if y_is_numeric else df[y]], axis=1)
    count_table = count_table.groupby(x)[y].value_counts().unstack().fillna(0)
    ordered_x_values = count_table.index.values if ordered_x_values is None else ordered_x_values
    ordered_y_values = count_table.columns if ordered_y_values is None else ordered_y_values
    if normalization_by_all:
        count_table /= count_table.sum().sum()
    else:
        for col in count_table.columns:
            count_table[col] /= count_table[col].sum()
    if log:
        count_table = np.log(count_table)
        maximal_bubble_size /= 2
    size_factor = maximal_bubble_size/count_table.max().max()
    count_table_long = pd.melt(count_table.reset_index(), id_vars=x)
    x_values_dict = {x:i for i, x in enumerate(count_table.index.values)} \
        if not x_is_numeric else {xx:get_point(xx) for xx in ordered_x_values}
    y_values_dict = {x:i for i, x in enumerate(count_table.columns)} \
        if not y_is_numeric else {xx: get_point(xx) for xx in ordered_y_values}
    count_table_long[x] = count_table_long[x].map(x_values_dict)
    count_table_long[y] = count_table_long[y].map(y_values_dict)
    xticks = np.arange(count_table.shape[0]) if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticks = np.arange(count_table.shape[1]) if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    xticklabels = count_table.index.values if not x_is_numeric else [get_point(xx) for xx in ordered_x_values]
    yticklabels = count_table.columns if not y_is_numeric else [get_point(xx) for xx in ordered_y_values]
    plt.scatter(count_table_long[x], count_table_long[y], s=size_factor*count_table_long['value'],
                c=count_table_long['value'], cmap='cool')
    plt.xticks(xticks, xticklabels,fontsize=fontsize)
    plt.yticks(yticks, yticklabels,fontsize=fontsize)
