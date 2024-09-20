import pandas as pd
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import mplcursors
import joblib

# Load the existing DataFrame
df = pd.read_csv(os.path.join("archive", "testdata.csv"))
df.dropna(inplace=True)


# Create variables for the data
countryNames = df["Country"]
x = df[['Population', 'GDP', 'Total']].values
y = df["Current Total"].values

# Load the new CSV file
#if os.path.exists("results.csv"):
  #  newxcount = pd.read_csv("results.csv")
   # if len(newxcount) == len(df):
   #     print("Put in 2020 dataset here")
  #      twentytwentydata = newxcount[["2020MedalCounts"]]
  #  else:
  #      print("Error: Length of new data does not match the existing DataFrame.")



Population = df.Population.values
GDP = df.GDP.values

# Load or create the model
if os.path.exists("trained_model.joblib"):
    model = joblib.load("trained_model.joblib")
else:

    model = RandomForestRegressor(n_estimators=100, random_state=42)


# Fit the model
model.fit(x, y)

# Make predictions
yPred = model.predict(x)
new_data = pd.DataFrame(yPred, columns=['Data'])

# tried to create 2024 predictions didnt work
#df.insert(2, "2020MedalCounts", twentytwentydata.values)
#model.apply(df[["Population", "GDP", "2020MedalCounts"]])
#olympics2024predictions = model.predict(df[["Population", "GDP", "2020MedalCounts"]])
#print(olympics2024predictions)
#

# Save predictions to CSV
new_data.to_csv('results.csv', header=["2020MedalCounts"], index=False)

predicted_values = np.array(yPred)

# Print errors
print("Mean Squared Error:", mean_squared_error(y, predicted_values))
print("Mean Absolute Error:", mean_absolute_error(y, predicted_values))

# Plotting
colorPalette = plt.colormaps.get_cmap('tab10').colors
indices = range(0, len(predicted_values) * 2, 2)

prediction = plt.scatter(indices, predicted_values)
actualVals = plt.scatter(indices, y, color=colorPalette[8])
values2016 = plt.scatter(indices, df["Total"], color=colorPalette[3])

cursor = mplcursors.cursor(hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(f"{countryNames[sel.index]}\nPredicted Val: {round(predicted_values[sel.index])}\nActual Val: {y[sel.index]}\n2016 Val: {df['Total'][sel.index]}\nGDP (in mil): {GDP[sel.index]}\nPopulation: {Population[sel.index]}"))

plt.legend(["Predicted Values", "Actual Values", "2016 Values"], loc="upper left")
joblib.dump(model, "trained_model.joblib")
plt.show()
