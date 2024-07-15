import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_players_playoff =  pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/real playoff 2023-2024 NBA Player Stats - Playoffs copy.csv")
df_players_regular =  pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/nba_players_regular_season.csv")
df_regular_teams = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/regular_season_nba.csv")
df_playoff_teams = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/playoff_nba.csv")

# print(df_players_regular.head())
# print(df_players_playoff.head())

#made the columns for both the playoff and regular seasons match
playoff_columns = df_players_playoff.columns.tolist()
df_players_regular.columns = playoff_columns

print(playoff_columns)

#finding the field goal attempt average and filtering out all the players who averaged higher than the league average
regular_players_above_fga_average = df_players_regular['FGA'].mean()
playoff_players_above_fga_average = df_players_playoff['FGA'].mean()

above_FGA_regular_players = df_players_regular.loc[df_players_regular['FGA'] > regular_players_above_fga_average]
above_FGA_playoff_players = df_players_playoff.loc[df_players_playoff['FGA'] > playoff_players_above_fga_average]

regular_field_goal_percent_average = above_FGA_regular_players['FG%'].mean()
playoff_field_goal_percent_average = above_FGA_playoff_players['FG%'].mean()
print(playoff_field_goal_percent_average)


#ploting the field goal results
regular_field_goal_percent = above_FGA_regular_players['FG%'].to_list()
playoff_field_goal_percent = above_FGA_playoff_players['FG%'].to_list()

regular_x_values = range(len(regular_field_goal_percent))
playoff_x_values = range(len(playoff_field_goal_percent))


##scatter plots for data
plt.scatter(regular_x_values, regular_field_goal_percent)
plt.scatter(playoff_x_values, playoff_field_goal_percent)

##respective field goal averages are also added to the plot
plt.hlines(y = regular_field_goal_percent_average, xmin = 0, xmax = max(regular_x_values), color = 'r', linestyle = 'dashed', label = 'Regular Season Field Goal Average')
plt.hlines(y = playoff_field_goal_percent_average, xmin = 0, xmax = max(playoff_x_values), color = 'g', linestyle = 'dashed', label = 'Playoffs Field Goal Average')

##cleaning up plot
plt.legend(['Regular Season', 'Playoffs','Regular Season Field Goal Average', 'Playoffs Field Goal Average' ])
plt.xlabel('NBA Players With Above Average Field Goal Attempts')
plt.ylabel('Field Goal Shooting Percentage')
plt.title("Different in Field Goal Percentage Between the Regular Season and Playoffs")
# plt.show()
plt.clf()

#finding the variance and standard deviation for the regular season and the post season
regular_fg_variance = np.var(regular_field_goal_percent)
playoff_fg_variance = np.var(playoff_field_goal_percent)

regular_fg_std = np.std(regular_field_goal_percent)
playoff_fg_std = np.std(playoff_field_goal_percent)


####COMPARING PTS DIFFERENCE BETWEEN SEASONS

#finding players who shot above the FGA
point_diff_players = above_FGA_regular_players['Player'].tolist()

pts_diff_regular = df_players_regular.loc[df_players_regular['Player'].isin(point_diff_players)]
pts_diff_playoff = df_players_playoff.loc[df_players_playoff['Player'].isin(point_diff_players)]

pts_diff_regular = pts_diff_regular['PTS']
pts_diff_playoff = pts_diff_playoff['PTS']

pts_diff_regular_list = pts_diff_regular.tolist()
pts_diff_playoff_list = pts_diff_playoff.tolist()

x_plot_values = range(0,len(pts_diff_regular))
x_plot_values_two = range(0,len(pts_diff_playoff))

#creating dictionary to obtain specific values
regular_pts_dict = {x_plot_values[i]: pts_diff_regular_list[i] for i in  range(len(pts_diff_regular_list))} 
playoff_pts_dict = {x_plot_values[i]: pts_diff_playoff_list[i] for i in  range(len(pts_diff_playoff_list))} 


#plotting values
fig, ax = plt.subplots(figsize = (20,6))
plt.scatter(x_plot_values, pts_diff_regular)
plt.scatter(x_plot_values,pts_diff_playoff)
ax.set_xticks(x_plot_values)
ax.set_xticklabels(point_diff_players, rotation = 90)

#shows if players regressed or improved their PPG during the playoffs
for x in x_plot_values:
    if regular_pts_dict[x] > playoff_pts_dict[x]:
        ax.vlines(x, ymin= playoff_pts_dict[x],
                 ymax=regular_pts_dict[x],
                 color='red', linestyle='dotted', linewidth=2)
    else:
        ax.vlines(x, ymin=regular_pts_dict[x],
                 ymax=playoff_pts_dict[x],
                 color='green', linestyle='dotted', linewidth=2)


ax.legend(['Regular Season PTS', 'Playoff PTS'])
plt.subplots_adjust(bottom=0.3)
plt.show()


# for x in x_plot_values:
#     if regular_pts_dict[x] > playoff_pts_dict[x]:
#         ax.vlines(x, ymin=min(min(pts_diff_regular), min(pts_diff_playoff)),
#                  ymax=max(max(pts_diff_regular), max(pts_diff_playoff)),
#                  color='red', linestyle='dotted', linewidth=1)
#     else:
#         ax.vlines(x, ymin=min(min(pts_diff_regular), min(pts_diff_playoff)),
#                  ymax=max(max(pts_diff_regular), max(pts_diff_playoff)),
#                  color='green', linestyle='dotted', linewidth=1)