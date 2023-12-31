# imports all the modules
import pandas as pd
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import mplcursors
import joblib

# Lots of gaps in my data set....
# Its hard to fill in data for over 200 countries
# but I tried to find data on most of the well known countries :(

# CSV loading and data refining
# we call the variable df for data frame
df = pd.read_csv(os.path.join("archive", "testdata.csv"))
df.dropna(inplace=True)

# creates variables for all the data we're using
countryNames = df["Country"]
x = df[['Population', 'GDP', 'Total']].values
y = df["Current Total"].values

Population = df.Population.values
GDP = df.GDP.values

# if we already have a model file, load that
if os.path.exists("trained_model.joblib"):
    model = joblib.load("trained_model.joblib")

# otherwise we create a new model to use
else:
    # initializes our random forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)

# fits our model to our data
model.fit(x, y)

# Formats a prediction
yPred = model.predict(x)

predicted_values = np.array(yPred)

# Gets rid of scientific notation in print statements
np.set_printoptions(suppress=True)

# Print the mean squared error
print("Mean Squared Error:", mean_squared_error(y, predicted_values))
print("Mean Absolute Error:", mean_absolute_error(y, predicted_values))

# Creates a color palette for variety
colorPalette = plt.colormaps.get_cmap('tab10').colors

# Creates a common x value for spacing and because
# we dont have a x value that would make sense to correlate the countries
indices = range(0, len(predicted_values) * 2, 2)

# Plots our points on a graph
prediction = plt.scatter(indices, predicted_values)
actualVals = plt.scatter(indices, y, color=colorPalette[8])
values2016 = plt.scatter(indices, df["Total"], color=colorPalette[3])

# Creates a cursor object to hover over data points
cursor = mplcursors.cursor(hover=True)

# Adds text for when the cursor is hovering over a point
cursor.connect("add", lambda sel: sel.annotation.set_text(f"{countryNames[sel.index]}\nPredicted Val: {round(predicted_values[sel.index])}\nActual Val: {y[sel.index]}\n2016 Val: {df['Total'][sel.index]}\nGDP (in mil): {GDP[sel.index]}\nPopulation: {Population[sel.index]}"))

# creates a legend for better visualization
plt.legend(["Predicted Values", "Actual Values", "2016 Values"], loc="upper left")

# saves our model so that it can be trained on more data for more accurate results
joblib.dump(model, "trained_model.joblib")

# Show the plot
plt.show()
