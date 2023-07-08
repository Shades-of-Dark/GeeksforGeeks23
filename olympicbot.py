import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import googlesearch


athleteStats = pd.read_csv(os.path.join("archive/", "athlete_events.csv"))

'''ID - Unique number for each athlete
Name - Athlete's name
Sex - M or F
Age - Integer
Height - In centimeters
Weight - In kilograms
Team - Team name
NOC - National Olympic Committee 3-letter code
Games - Year and season
Year - Integer
Season - Summer or Winter
City - Host city
Sport - Sport
Event - Event
Medal - Gold, Silver, Bronze, or NA'''

errormsg = "That name is not in our registers! Make sure you're typing the name correctly, or if the athlete competed in 2016 olympics and prior.\n" \
           "Example: Christine Jacoba Aaftink"

athleteName = input("Type the name of an athlete: \n")

matchedRows = [i for i, d in enumerate(athleteStats.values) if athleteName in d]

while len(matchedRows) == 0:
    print(errormsg)
    athleteName = input("Type the name of an athlete: \n")
    matchedRows = [i for i, d in enumerate(athleteStats.values) if athleteName in d]

womanBMI = {(7.5, 16.5): "severe underweight",
            (16.5, 18.5): "underweight",
            (18.5, 24.9): "normal weight",
            (25.0, 29.9): "overweight",
            (30.0, 34.9): "obesity class I",
            (35.0, 39.9): "obesity class II",
            (40, 140): "obesity class III"}

manBMI = {(7.5, 18.5): "severe underweight",
          (18.5, 24.9): "normal weight",
          (25.0, 29.9): "overweight",
          (30.0, 140): "obese"}


def bmi_calc(cm, kg):
    return kg / cm / cm * 10000


def obesity(gender, manbmi, womanbmi, bmiCalc):
    if gender == "F":
        for entry in womanbmi.keys():
            if entry[0] < bmiCalc < entry[1]:
                print(womanbmi[entry])
    else:
        for entry in manbmi.keys():
            if entry[0] < bmiCalc < entry[1]:
                print(manbmi[entry])


query = athleteName + " personal bests"

url = googlesearch.search(query, start=1, stop=1, pause=1, tld="co.in")

r = requests.get(list(url)[0])

soup = BeautifulSoup(r.content, "html.parser")
text = soup.text.lower()

foundText = text.find("personal")
print(text[foundText:foundText + 100] + " \n")
# Christine Jacoba Aaftink


for num in matchedRows:
    height = athleteStats["Height"][num]
    weight = athleteStats["Weight"][num]
    age = athleteStats["Age"][num]
    sex = athleteStats["Sex"][num]
    medal = athleteStats["Medal"][num]
    bmi = round(bmi_calc(height, weight), 2)
    sport = athleteStats["Sport"][num]
    event = athleteStats["Event"][num]
    year = athleteStats["Year"][num]

    print(f"Weight: {weight}")
    print(f"Height: {height}")
    print(f"Age: {age}")
    print(f"Sex: {sex}")
    print(f"BMI: {bmi}")
    print(f"Medal: {medal}")
    print(f"Sport: {sport}")
    print(f"Event: {event}")
    print(f"Year: {year}")
    obesity(sex, manBMI, womanBMI, bmi)

    print("\n")
