import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tabulate as tabulate

df_players_playoff =  pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/real playoff 2023-2024 NBA Player Stats - Playoffs copy.csv")
df_players_regular =  pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/nba_players_regular_season.csv")
df_regular_teams = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/regular_season_nba.csv")
df_playoff_teams = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/playoff_nba.csv")
df_players_height = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/all_seasons.csv")

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
point_diff_players = above_FGA_regular_players['Player'].tolist() #getting a list fo players that shot above the FGA

pts_diff_regular_df = df_players_regular.loc[df_players_regular['Player'].isin(point_diff_players)] #filtering the columns of players that shot above the FGA
pts_diff_playoff_df = df_players_playoff.loc[df_players_playoff['Player'].isin(point_diff_players)]

pts_diff_regular = pts_diff_regular_df['PTS'] #only selecting the PTS column
pts_diff_playoff = pts_diff_playoff_df['PTS']

pts_diff_regular_list = pts_diff_regular.tolist() #creating a list of the PTS column
pts_diff_playoff_list = pts_diff_playoff.tolist()

x_plot_values = range(0,len(pts_diff_regular)) #x plot values to plot PTS list
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

regressed_count = 0 #counting how many players regressed and improved in the playoffs
progress_count = 0
regressed_player_list = [] #obtaining the index value for all the players based of if they regressed or improved
progress_player_list = []

#shows if players regressed or improved their PPG during the playoffs (this is how they show the green or red dotted lines)
for x in x_plot_values:
    if regular_pts_dict[x] > playoff_pts_dict[x]:
        regressed_count +=1
        regressed_player_list.append(x)
        ax.vlines(x, ymin= playoff_pts_dict[x],
                 ymax=regular_pts_dict[x],
                 color='red', linestyle='dotted', linewidth=2)
    else:
        progress_count +=1
        progress_player_list.append(x)
        ax.vlines(x, ymin=regular_pts_dict[x],
                 ymax=playoff_pts_dict[x],
                 color='green', linestyle='dotted', linewidth=2)


ax.legend(['Regular Season PTS', 'Playoff PTS'])
plt.title("PPG Differential Between Regular and Playoff Season")
plt.ylabel("PPG")
plt.subplots_adjust(bottom=0.3)
# plt.show()
plt.clf()


#setting up to perform analysis
# print(regressed_count, progress_count)
# print(regressed_player_list, progress_player_list)
# print(point_diff_players)

regressed_names = [] #going thorugh regressed and improved lists (the ones with index values) and obtaining the players names
progress_names = []
for num in regressed_player_list:
    regressed_names.append(point_diff_players[num])
for num in progress_player_list:
    progress_names.append(point_diff_players[num])


regressed_avg_numerator = 0
progress_avg_numerator = 0
regressed_name_ppg_differential_dict = {}
progress_name_ppg_differential_dict = {}

# print(progress_names)
#merged playoff and regular season tables to create another table comparing the PPG values
regular_playoff_ppg_diff_merged_df = pd.merge(pts_diff_regular_df, pts_diff_playoff_df, on = 'Player', suffixes=('_regular', '_playoffs'))
regular_playoff_ppg_diff_merged_df['Point Difference'] = regular_playoff_ppg_diff_merged_df['PTS_playoffs'] - regular_playoff_ppg_diff_merged_df['PTS_regular']
specific_columns = regular_playoff_ppg_diff_merged_df[['Player', 'PTS_regular', 'PTS_playoffs','Point Difference']]

point_difference_mean = specific_columns['Point Difference'].mean()


for player in specific_columns['Player']:
    value = specific_columns.loc[specific_columns['Player'] == player, 'Point Difference']
    value = float(value.iloc[0])
    if  value > 0:
        progress_avg_numerator += value
    else:
        regressed_avg_numerator += value

regressed_avg = regressed_avg_numerator/len(regressed_names)
progress_avg = progress_avg_numerator/len(progress_names)


largest_point_difference = specific_columns.nlargest(5, 'Point Difference')
smallest_point_difference = specific_columns.nsmallest(5, 'Point Difference')


# specific_columns.to_csv('PPG_differential.csv')


#three-point percentage analysis

regular_players_above_threePA_average = df_players_regular['3PA'].mean()
playoff_players_above_threePA_average = df_players_playoff['3PA'].mean()
above_threePA_regular_players = df_players_regular.loc[df_players_regular['3PA'] > regular_players_above_threePA_average]
above_threePA_playoff_players = df_players_playoff.loc[df_players_playoff['3PA'] > playoff_players_above_threePA_average]
# print(above_threePA_playoff_players)
# print(above_threePA_regular_players)
# print(np.max(above_threePA_regular_players['3P%']))
# print(np.min(above_threePA_regular_players['3P%']))

above_threePA_regular_players_list = above_threePA_regular_players['Player'].tolist()
above_threePA_playoff_players_list = above_threePA_playoff_players['Player'].tolist()
print(above_threePA_regular_players_list)



df_players_height_no_duplicates = df_players_height.drop_duplicates(subset= ['player_name', 'player_height']) #getting the players height through another dataset. needed to removed the duplicates


above_threePA_regular_players['players_height'] = None
height_list = df_players_height_no_duplicates['player_name'].tolist()

#adding data from height df to above 3P% dataframe
for player in above_threePA_regular_players_list:
    if player in height_list:
        above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, 'players_height']= df_players_height_no_duplicates.loc[df_players_height_no_duplicates['player_name'] == player, 'player_height'].values[0]
    else:
        above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, 'players_height']= None

print(above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == 'Paul George', 'players_height'].values[0] )


#checking for any players that did not have the same spelling in height df or had not been drafted yet. (Note that the height dataset only goes up to 2022)
missing_player_height = []
for player in above_threePA_regular_players_list:
    if above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, 'players_height'].values[0]== None:
        missing_player_height.append(player)
        
#adding values for missing data
above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == 'Bojan Bogdanovi?', 'players_height'] = 201
above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == 'Luka Don?i?', 'players_height'] = 201
above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == 'Jordan Hawkins', 'players_height'] = 196
above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == 'Chet Holmgren', 'players_height'] = 216
above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == 'Nikola Jovi?', 'players_height'] = 208
above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == 'Kristaps Porzi??is', 'players_height'] = 218







# above_threePA_regular_players['3P_percent for bin'] = None

# for player in above_threePA_regular_players_list:
#     if above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.25:
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] =0.25
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.25 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.27 :
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.27
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.27 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.29 :
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.29
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.29 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.31 :
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.31
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.31 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.33 :
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.33
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.33 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.35:
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.35
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.35 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.37:
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.37
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.37 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.39:
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.39
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.39 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.41:
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.41
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.41 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.43:
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.43
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.43 and above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] < 0.45:
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.45
#     elif above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P%'].values[0] > 0.45:
#         above_threePA_regular_players.loc[above_threePA_regular_players['Player'] == player, '3P_percent for bin'] = 0.47

# print(above_threePA_regular_players[['Player', '3P_percent for bin']])

print(np.mean(above_threePA_regular_players['3P%']))
fig, ax = plt.subplots(figsize = (6,6))
plt.hist(above_threePA_regular_players['3P%'], bins = 12, alpha = 0.5, density = True)
plt.hist(above_threePA_playoff_players['3P%'], bins = 12, alpha = 0.5, density = True)
ax.vlines(x = np.mean(above_threePA_regular_players['3P%']), ymin = 0, ymax = 18, colors = 'r', linestyle = 'dashed')
ax.vlines(x = np.mean(above_threePA_playoff_players['3P%']), ymin = 0, ymax = 18, colors = 'g', linestyle = 'dashed')
plt.show()

