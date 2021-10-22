import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
### Make 'overweight' column, fill with "empty" 0 (needs to be an int to preserve type)
df['overweight'] = 0

### Use BMI calculations (weight/height^2) to assign 1 or 0 to each row in 'overweight'
df.loc[(df['weight']/((df['height']/100)**2)) > 25, 'overweight'] = 1
df.loc[(df['weight']/((df['height']/100)**2)) <= 25, 'overweight'] = 0

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[(df['cholesterol'] == 1), 'cholesterol'] = 0
df.loc[(df['cholesterol'] > 1), 'cholesterol'] = 1
df.loc[(df['gluc'] == 1), 'gluc'] = 0
df.loc[(df['gluc'] > 1), 'gluc'] = 1


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars = ['cardio'], value_vars = [ 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'], ignore_index = False)


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. 
    ### groupby and then count the total for each grouping by using agg
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).agg(
    total = pd.NamedAgg(column = 'value', aggfunc = 'count')).reset_index()

    # Draw the catplot with 'sns.catplot()'
    graph = sns.catplot(x = "variable", y = "total", col = "cardio", hue = 'value', data = df_cat, kind = "bar", height = 6)
    fig = graph.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


#Draw Heat Map
def draw_heat_map():
    #Clean the data
    df_clean = df[(df['ap_lo'] <= df['ap_hi']) &  
      (df['height'] >= df['height'].quantile(0.025)) &
      (df['height'] <= df['height'].quantile(0.975)) &
      (df['weight'] >= df['weight'].quantile(0.025)) &
      (df['weight'] <= df['weight'].quantile(0.975))]
 
   #Calculate the correlation matrix
    corr = df_clean.corr()

    #Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    #Set up the matplotlib figure
    fig, ax = plt.subplots()

    #Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask = mask, fmt = '.1f', annot = True, linecolor = 'white', linewidth = 0.2, square = True)

    #Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
