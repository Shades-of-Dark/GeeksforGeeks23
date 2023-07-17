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
df = pd.read_csv(os.path.join("archive", "testdata.csv"))
df.dropna(inplace=True)

countryNames = df["Country"]
x = df[['Population', 'GDP', 'Total']].values
y = df["Current Total"].values
Population = df.Population.values
GDP = df.GDP.values

# Creates our model trains it and predicts medal counts

if os.path.exists("trained_model.joblib"):
    model = joblib.load("trained_model.joblib")
else:
    model = RandomForestRegressor(n_estimators=100, random_state=42)

model.fit(x, y)

# Formats a prediction
y_pred = model.predict(x)

predicted_values = np.array(y_pred)

# Gets rid of scientific notation in print statements
np.set_printoptions(suppress=True)

# Print the mean squared error
print("Mean Squared Error:", mean_squared_error(y, predicted_values))
print("Mean Absolute Error:", mean_absolute_error(y, predicted_values))

# Creates a color palette for variety
color_palette = plt.colormaps.get_cmap('tab10').colors

# Creates a common x value for spacing
indices = range(0, len(predicted_values) * 2, 2)

# Plots our points on a graph
prediction = plt.scatter(indices, predicted_values)
actualVals = plt.scatter(indices, y, color=color_palette[8])
values2016 = plt.scatter(indices, df["Total"], color=color_palette[3])

cursor = mplcursors.cursor(hover=True)

cursor.connect("add", lambda sel: sel.annotation.set_text(f"{countryNames[sel.index]}\nPredicted Val: {round(predicted_values[sel.index])}\nActual Val: {y[sel.index]}\n2016 Val: {df['Total'][sel.index]}\nGDP (in mil): {GDP[sel.index]}\nPopulation: {Population[sel.index]}"))


plt.legend(["Predicted Values", "Actual Values", "2016 Values"], loc="upper left")

# saves our model so that it can be trained on more data for more accurate results
joblib.dump(model, "trained_model.joblib")

# Show the plot
plt.show()
