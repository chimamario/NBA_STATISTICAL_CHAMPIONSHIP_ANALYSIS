import pandas as pd

df_players_playoff =  pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/real playoff 2023-2024 NBA Player Stats - Playoffs copy.csv")
df_players_regular =  pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/nba_players_regular_season.csv")
df_regular_teams = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/regular_season_nba.csv")
df_playoff_teams = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/nba_project_2024/cleaned_up_data and_code/playoff_nba.csv")

print(df_players_regular.head())
print(df_players_playoff.head())

regular_players_above_fga_average = df_players_regular['fg'].mean()
# playoff_players_above_fga_average = df_players_playoff['fg'].mean()
print(regular_players_above_fga_average)
# print(playoff_players_above_fga_average)

#next task - change column in regular players to make with playoff players