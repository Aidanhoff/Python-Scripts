# Following tutorial available at https://towardsdatascience.com/random-forest-in-python-24d0893d51c0

import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestRegressor
# This bit is basically just some data prepping.


features = pd.read_csv('temps.csv')
print(features.head(5))

# Probably a good idea to look up how this works. Basically, converts categorical data into boolean columns where data has attribute or not. 
features = pd.get_dummies(features)

# labels = values we want to predict (?)
labels = np.array(features['actual'])

# Removes labels from features by dropping 'actual' and removing axis 1 of the data (the columns)
features = features.drop('actual', axis = 1)

# Just saving the column headers for later.
feature_list = list(features.columns)

features = np.array(features)

# Onto the data split (using skicit-learn, rather than doing it ourselves.)

# Setting random_state = 42 is essentially a seeded RNG for reproducibility; can leave blank. See http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html. 
# test_size is the proportion (btwn 0-1) of the dataset to keep for training. By default the train_size is the complement. 
# Important to note that this is basically skipping the whole bootstrapping element where you use some preliminary trees to optimize your split variable. 
#Note that for a classification project you will want the Gini index
train_features, test_features, train_labels, test_labels, = train_test_split(features, labels, test_size = 0.25, random_state = 42)

# Onto making baseline predictions (the "supervision" part of the ML)
# Baseline predictions == historical averages in this case.
baseline_preds = test_features[:, feature_list.index('average')] #some NP syntaxs I assume

# Baseline errors/avg error
baseline_errors = abs(baseline_preds - test_labels)

print('Average baseline error: ', round(np.mean(baseline_errors), 2))

# Result = ~ 5 degrees -> element to beat. Think, do we have a current predictive model for soils similar to the average daily temp? -> Discussed in paper to some extent.

#This is the actual random forest model. Note here that we use the Regressor as we're dealing with some interval data; for soil we want the classifier.
# There are bootstrapping vars in this equation that need some inspection later. Apparently bootstrapping is true by default though, so...?
rf = RandomForestRegressor(n_estimators= 1000, random_state=42)

rf.fit(train_features, train_labels)

# Onto the fun stuff, making predictions.

predictions = rf.predict(test_features)

# Basically taking predicted values minus the values from our test dataset.
errors = abs(predictions - test_labels)
print('Mean Absolute Error: ', round(np.mean(errors), 2), 'degrees.')

# MAE (Mean Absolute Error) == 3.87 deg.

# Defining our performance metrics

# Mean Absolute Percentage Error (MAPE)
mape = 100 * (errors/ test_labels)

accuracy = 100 - np.mean(mape)
print('Accuracy: ', round(accuracy, 2), '%.')


# At this point we have a fully operational tree. How does it work? Who knows. Let's find out.

'''from sklearn.tree import export_graphviz
import pydot 

tree = rf.estimators_[5]

export_graphviz(tree, out_file='tree.dot', feature_names= feature_list, rounded=True, precision=1)

(graph, ) = pydot.graph_from_dot_file('tree.dot')
# This doesn't work at the moment. Probably easy to fix, just cba. 
try:
    graph.write_png('tree.png')
except AttributeError:
    print("Weird pydot error")'''

# Read the source blog, but basically the tree tells us which vars it uses, and therefore what vars turned out to be strong predictors so we can eliminate data for future models. Spoiler alert, it was temp 1 day prior and historic temp averages.

# Now to actually test to find variable importance. 

# Note: this code has some fun list comprehensions, lambas, zip, etc. Good to study.
importances = list(rf.feature_importances_)

feature_importances = [ (feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]

feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

# Note that we're getting some different values than expected. Publishing date of the article was 10 months ago so it's possible that scikitlearn has changed their rf algorithms slightly.