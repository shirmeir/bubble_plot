# bubble_plot
Hi everyone!

I love data visualizations! And if you love them too, I think you will find this bubble plot very nice and useful.

- [How to install](#how_to_install)
- [Motivation & Usage](#motivation)
- [Usage Example](#usage)
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

Setting the `log` parameter to `True` would apply the natural log function - element wise - on the counts which will make the differences between the largest bubble to the smallest bubble much smaller, so if you have large differences between the frequencies of different values you might want to use that.

Setting the `z_boolean` parameter to a name of categorical field with two categories / boolean field would make the color of the bucket  be proportional to the ratio ( (boolean_z==value_1).sum()/(boolean_z==value_1).sum() + (boolean_z==value_2).sum()) of the z values for this bucket. 

## <a name="usage"></a>Usage Example

```python
import pandas as pd  
from bubble_plot.bubble_plot import bubble_plot
from sklearn.datasets import load_boston                            
data = load_boston()                            
df = pd.DataFrame(columns=data['feature_names'], data=data['data'])                            
df['target'] = data['target']                            
bubble_plot(df, x='RM', y='target')    
```                        

The resulting bubble plot will look like this:
![](https://github.com/shirmeir/bubble_plot/blob/master/bubble_plot.png)
   
   
## <a name="dependencies"></a>Dependencies
  * pandas
  * numpy
  * matplotlib                                   


## <a name="contact"></a>Contact
More usage examples and explanations can be found at:
https://medium.com/@DataLady/exploring-the-census-income-dataset-using-bubble-plot-cfa1b366313b

Please let me know if you have any questions. My email is meir.shir86@gmail.com.

Enjoy,
Shir
