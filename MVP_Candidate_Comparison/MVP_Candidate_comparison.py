#Comparing the NBA MVP and NBA MVP runner up


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import requests

#These are the json url files that contian Steph Curry's and James Harden's 2014-2015 game logs..
url_James = 'http://stats.nba.com/stats/playergamelog?LeagueID=00&'+\
            'PlayerID=201935&Season=2014-15&SeasonType=Regular+Season'

url_Steph = 'http://stats.nba.com/stats/playergamelog?LeagueID=00&'+\
            'PlayerID=201939&Season=2014-15&SeasonType=Regular+Season'

#Request the content of the url and parse the JSON file using the loads method.
James_response = requests.get(url_James)
James_response.raise_for_status() #Raise an error if something goes wrong with the request.

Steph_response = requests.get(url_Steph)
Steph_response.raise_for_status()

#Grab the list of statistic categories (columns), "headers", and save them into the James_stat_names variable.
James_stat_names = James_response.json()["resultSets"][0]["headers"]
Steph_stat_names = Steph_response.json()['resultSets'][0]['headers']

#Grab an entire season worth of game logs of the each player (rows).
James_stats = James_response.json()['resultSets'][0]['rowSet']
Steph_stats = Steph_response.json()['resultSets'][0]['rowSet']


"""Create a matrix dataframe that will store all this data using the pandas module.
We will set the rows of the dataframe to be equal to the "rowSet" of each player
and obviously we will use the categories "headers" to index the columns of our matrix."""
James_df = pd.DataFrame(James_stats,columns=James_stat_names)
Steph_df = pd.DataFrame(Steph_stats,columns=Steph_stat_names)




#These are all the statistics that I'm going to use to compare the players.
contributing_stats = ["MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT",
                      "FTM", "FTA", "OREB", "DREB", "REB", "AST", "STL",
                      "BLK", "TOV", "PF", "PTS", "PLUS_MINUS"]

#Subset the original dataframes to only return the columns of data that we want to analyze in the comparison.
James_numerical_stats = James_df[contributing_stats]
Steph_numerical_stats = Steph_df[contributing_stats]



MVP_candidates = ["James", "Steph"]

"""For each player, I want the average percentage for all of the percentage stats and
the sum of the data in each of the other category areas. I.e. sum of made field goals,
steals, assist, etc."""
for player in MVP_candidates:
    if player == "James":
        James_tot_avg = [James_numerical_stats[stat].mean(axis=0)
                        if "PCT" in stat else James_numerical_stats[stat].sum(axis=0)
                        for stat in contributing_stats]
    else:
        Steph_tot_avg = [Steph_numerical_stats[stat].mean(axis=0)
                         if "PCT" in stat else Steph_numerical_stats[stat].sum(axis=0)
                         for stat in contributing_stats]


row_set = [Steph_tot_avg, James_tot_avg]
Comparison_df = pd.DataFrame(row_set, columns=contributing_stats)

Comparison_df.insert(9,column='FT_PCT', value=Comparison_df['FTM']/Comparison_df['FTA'])
Comparison_df.insert(0, column='Name', value = ['Stephen_Curry', 'James Harden'])

print(Comparison_df)

#Now let's analyze the data side by side using a bar graph.
steph_stats = Comparison_df.irow(slice(0,1))
#This is another way to retrieve a specific row of data from the matrix dataframe
james_stats = Comparison_df.iloc[[1]]



scoring_stats = ['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'PTS']
team_contribution_stats = ['AST', 'TOV', 'PF', 'PLUS_MINUS', 'MIN']
defensive_and_hustle_stats = ['STL', 'BLK', 'DREB', 'OREB', 'REB']
percentage_stats = ['FG_PCT', 'FG3_PCT', 'FT_PCT']

#First we will check out and compare the scoring stats
x_axis_scoring = [category for category in scoring_stats]
steph_totals_scoring = [steph_stats[category].item() for category in scoring_stats]
james_totals_scoring = [james_stats[category].item() for category in scoring_stats]

#The defensive/hustle stats.
x_axis_defense = [category for category in defensive_and_hustle_stats]
steph_totals_defense = [steph_stats[category].item() for category in
                        defensive_and_hustle_stats]
james_totals_defense = [james_stats[category].item() for category in
                        defensive_and_hustle_stats]

#The stats that contribute to the success of the team.
x_axis_team = [category for category in team_contribution_stats]
steph_totals_team = [steph_stats[category].item() for category in team_contribution_stats]
james_totals_team = [james_stats[category].item() for category in team_contribution_stats]

#Finally, the average shooting percentages of the season.
x_axis_percentages = [category for category in percentage_stats]
steph_percentages = [steph_stats[category].item() for category in percentage_stats]
james_percentages = [james_stats[category].item() for category in percentage_stats]

#Function that will construct a bar graph comparing the two candidates for each statistic category.
def bar_graph(x_axis, steph_totals, james_totals, title, xlabel, ylabel):

    index = np.arange(0, len(x_axis), 1)
    bar_width = 0.25
    bar1 = plt.bar(index, steph_totals, bar_width, color='b', label='Steph')
    bar2 = plt.bar(index+bar_width, james_totals, bar_width, color='r', label='James')
    plt.xticks(index+bar_width, x_axis)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

#Create four bar graphs comparing the selected statistics.
fig = plt.figure(1)
plt.style.use('ggplot')
ax = plt.subplot(221)
bar_graph(x_axis_scoring, steph_totals_scoring, james_totals_scoring,
          'Scoring Stats', 'Scoring Categories', 'Season_Total')
leg = plt.legend(loc = 'center left')
bb = leg.legendPatch.get_bbox().inverse_transformed(ax.transAxes)
xOffset = 1.25
yOffset = 1.24
newX0 = bb.x0 + xOffset
newX1 = bb.x1 + xOffset
newY0 = bb.y0 + yOffset
newY1 = bb.y1 + yOffset
bb.set_points([[newX0, newY0], [newX1, newY1]])
leg.set_bbox_to_anchor(bb)

plt.subplot(222)
bar_graph(x_axis_defense, steph_totals_defense, james_totals_defense,
          'Defensive/Hustle Stats', 'Defensive Categories', 'Season_Total')

plt.subplot(223)
bar_graph(x_axis_team, steph_totals_team, james_totals_team,
          'Team Contributing Stats', 'Team Categories', 'Season_Total')

plt.subplot(224)
bar_graph(x_axis_percentages, steph_percentages, james_percentages,
          'Scoring Percentages', 'Percentage Categories', 'Average_Percentage')

fig.tight_layout()
plt.show()
