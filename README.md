# bubble_plot
Hi everyone!

I love data visualizations! And if you love them too, I think you will find this bubble plot very nice and useful.

The goal for the bubble plot is to help us visualize linear and non-linear connections between numerical/categorical features in our data in an easy and simple way.
The bubble plot is a kind of a 2 dimensional histogram using bubbles.
It suits every combination of categorical and numerical features.

The bubble size is proportional to the frequency of the data points in this point.

For numerical features the values will be presented in buckets (10 equally spaced bins will be used as default, you can provide the specific bins / bins number through bin_x and bins_y).

df, x, y, ordered_x_values=None, ordered_y_values=None, bins_x=10, bins_y=10, fontsize=16, figsize=(15,10), maximal_bubble_size=5000, normalization_by_all = False, log=False):

For categorical features the features will be presented according to their categories.
If you would like a specific order for the categories presentation please supply a list of the values by order in ordered_x_values/ ordered_y_values.

You can plot a numerical features vs. another numerical feature or a categorical feature vs another categorical features.
Normalization by all means joint distribution p(x,y), if it is false we see the conditional distribution of y vs. x p(y/x).

log would apply log on the counts which will make the differences between the largest bubble to the smallest bubble much smaller, so if you have large differences between the frequencies of different values you might want to use that.

Example of usage:

import pandas as pd                             
from sklearn.datasets import load_boston                            
data=load_boston()                            
df = pd.DataFrame(columns=data['feature_names'], data=data['data'])                            
df['target'] = data['target']                            
bubble_plot(df,x = 'RM', y = 'target')                            

The resulting bubble plot will look like this:
![](https://github.com/shirmeir/bubble_plot/blob/master/bubble_plot.png)
                                          
dependencies - pandas, numpy, matplotlib                                          


Please let me know if you have any questions. My email is meir.shir86@gmail.com.

Enjoy,

Shir

