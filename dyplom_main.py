import pandas as pd
import matplotlib.pyplot as plt

potwierdzone = pd.read_csv('confirmed.csv')
smierci = pd.read_csv('deaths.csv')
wyleczeni = pd.read_csv('recovered.csv')

potwierdzone = potwierdzone.drop(['Province/State', 'Lat', 'Long'], axis=1)
smierci = smierci.drop(['Province/State', 'Lat', 'Long'], axis=1)
wyleczeni = wyleczeni.drop(['Province/State', 'Lat', 'Long'], axis=1)

potwierdzone = potwierdzone.groupby(potwierdzone['Country/Region']).aggregate('sum')
smierci = smierci.groupby(smierci['Country/Region']).aggregate('sum')
wyleczeni = wyleczeni.groupby(wyleczeni['Country/Region']).aggregate('sum')

potwierdzone = potwierdzone.T
smierci = smierci.T
wyleczeni = wyleczeni.T

new_cases = potwierdzone.copy()

for day in range(1, len(potwierdzone),30):
    new_cases.iloc[day] = potwierdzone.iloc[day] - potwierdzone.iloc[day-1]

growth_rate = potwierdzone.copy()

for day in range(1, len(potwierdzone),30):
    growth_rate.iloc[day] = new_cases.iloc[day] / potwierdzone.iloc[day-1]

active_cases = potwierdzone.copy()

for day in range (0, len(potwierdzone),30):
    active_cases.iloc[day] = potwierdzone.iloc[day] - smierci.iloc[day] - wyleczeni.iloc[day]

overall_growth_rate = potwierdzone.copy()

for day in range(1, len(potwierdzone),30):
    overall_growth_rate.iloc[day] = ((active_cases.iloc[day] - active_cases.iloc[day-1]) / active_cases.iloc[day - 1]) * 100

death_rate = potwierdzone.copy()

for day in range(0, len(potwierdzone),30):
    death_rate.iloc[day] = (smierci.iloc[day] / potwierdzone.iloc[day]) * 100

hospitalization_rate_estimate = 0.05

hospitalization_needed = potwierdzone.copy()

for day in range(0, len(potwierdzone)):
    hospitalization_needed.iloc[day] = active_cases.iloc[day] * hospitalization_rate_estimate


# WIZUALIZACJA

countries = ['Italy', 'China', 'Poland', 'Germany']

#Potwierdzone przypadki
# ax = plt.subplot()
# ax.set_facecolor('black')
# ax.figure.set_facecolor('#121212')
# ax.tick_params(axis='x', colors = 'white')
# ax.tick_params(axis='y', colors = 'white')
# ax.set_title('Covid-19 - Wszystkie potwierdzone przypadki wg. kraju', color = 'white')

# for country in countries:
#     potwierdzone[country].plot.bar(label=country)

# plt.legend(loc = 'upper left')
# plt.show()


# Wzrost zakażeń
# for country in countries: 
#     ax = plt.subplot()
#     ax.set_facecolor('black')
#     ax.figure.set_facecolor('#121212')
#     ax.tick_params(axis='x', colors = 'white')
#     ax.tick_params(axis='y', colors = 'white')
#     ax.set_title(f'Covid-19 - Wszystkie wzrosty potwierdzonych przypadków wg. {country}', color = 'white')
#     potwierdzone[country].plot.bar(label=country)
#     plt.show()

# Wszystkie truposze
for country in countries: 
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors = 'white')
    ax.tick_params(axis='y', colors = 'white')
    ax.set_title(f'Covid-19 - Wszystkie śmierci wg. {country}', color = 'white')

    for country in countries:
        smierci[country].plot.bar(label=country)

plt.legend(loc = 'upper left')
plt.show()