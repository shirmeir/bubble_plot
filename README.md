# bubble_plot
Hi everyone!

I love data visualizations! And if you love them too, I think you will find this bubble plot very nice and useful.

- [How to install](#how_to_install)
- [Motivation & Usage](#motivation)
- [Usage Example](#usage)
- [Usage Example 2](#usage2)
- [Utils](#utils)
- [Dependencies](#dependencies)
- [Contact](#contact)

## <a name="how_to_install"></a>How to install

Very simple - just write in your command line:
```python
pip install bubble_plot
```

## <a name="motivation"></a>Motivation & Usage

The goal for the bubble plot is to help us visualize linear and non-linear connections between numerical/categorical features in our data in an easy and simple way. The bubble plot is a kind of a 2-dimensional histogram using bubbles. It suits every combination of categorical and numerical features.

The bubble size is proportional to the frequency of the data points in this point.

*Function signature:*
```python
bubble_plot(df, x, y, z_boolean=None, ordered_x_values=None, ordered_y_values=None, bins_x=10, bins_y=10, fontsize=16, 
            figsize=(15,10), maximal_bubble_size=5000, normalization_by_all = False, log=False)
```

For numerical features the values will be presented in buckets (ten equally spaced bins will be used as default, you can provide the specific bins / bins number through the `bin_x` and `bins_y` parameters).

For categorical features the features will be presented according to their categories. If you would like a specific order for the categories presentation please supply a list of the values by order using the `ordered_x_values` / `ordered_y_values` parameters.

You can plot a numerical feature vs. another numerical feature or vs. a categorical feature or a categorical feature vs another categorical feature or numerical feature. All options are possible.

Setting the parameter normalization_by_all to False defines that we would like to plot P(y/x), meaning, plot the distribution of y given x. Each column in this plot is an independent (1D) histogram of the values of the y given x. Setting the parameter normalization_by_all to True would plot the joint distribution of x and y, P(x,y), this is in fact a 2D histogram with bubbles. 

Setting the `log` parameter to `True` would apply the natural log function - element wise - on the counts which will make the differences between the largest bubble to the smallest bubble much smaller, so if you have large differences between the frequencies of different values you might want to use that.

Setting the `z_boolean` parameter to a name of categorical field with two categories / boolean field would make the color of the bucket  be proportional to the ratio ( (boolean_z==value_1).sum()/(boolean_z==value_1).sum() + (boolean_z==value_2).sum()) of the z values for this bucket. 

## <a name="usage"></a>Usage Example

```python
import pandas as pd  
from bubble_plot.bubble_plot import bubble_plot
from sklearn.datasets import load_boston
import seaborn as sns
sns.set_style("darkgrid")
data = load_boston()                            
df = pd.DataFrame(columns=data['feature_names'], data=data['data'])                            
df['target'] = data['target']                            
bubble_plot(df, x='RM', y='target')
```                        

The resulting bubble plot will look like this:
![](https://github.com/shirmeir/bubble_plot/blob/master/boston.png)

## <a name="usage2 "></a>Usage Example 2
Census income dataset - plot the age vs. hours per week vs. the income level.
How is that even possible? Can we visualize three dimensions of information in a two dimensional plot?

```python
import pandas as pd
import seaborn as sns
from bubble_plot.bubble_plot import bubble_plot
sns.set_style("darkgrid")
df = pd.read_csv("adult.csv")
bubble_plot(df, x='age', y='hours-per-week', z_boolean='target')
```                        

The resulting bubble plot will look like this:
![](https://github.com/shirmeir/bubble_plot/blob/master/3d_plotv.png)

P(x,y), x: age, y: working hours, color — proportional to the rate of high income people within each bucket

In this bubble plot, we see  the joint distribution of the hours-per-week vs. the age (p(x,y)), but here the color is proportional to the rate of high income people — (#>50K/((#>50K)+(#≤50K)) - within all the people in this bucket . By supplying the z_boolean variable, we added additional dimension to the plot using the color of the bubble.

The pinker the color, the higher the ratio for the given boolean feature/target Z. See colormap in the image.
![](https://github.com/shirmeir/bubble_plot/blob/master/cool.png)

Cool colormap — Pink would stand for the higher ratios in our case, cyan would stand for the lower ratios

This plot shows us clearly that the higher income is much more common within people of age higher than 30 which work more than 40 hours a week.

## <a name="Utils "></a>Utils

Some additional utils for modeling and data exploration were added to this package.
Examples of how to use them can be found here:
https://github.com/shirmeir/notebooks/blob/master/predicting_income_from_census_income_data.ipynb


## <a name="dependencies"></a>Dependencies
for bubble_plot:
  * pandas
  * numpy
  * matplotlib      

for utils:
  * sklearn
  * seaborn


## <a name="contact"></a>Contact
More usage examples and explanations can be found at:
https://medium.com/@DataLady/exploring-the-census-income-dataset-using-bubble-plot-cfa1b366313b

Please let me know if you have any questions. My email is meir.shir86@gmail.com.

Enjoy,
Shir
