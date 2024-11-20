import pandas as pd
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UCL_allTime_performance_table_csv = os.path.join(
    root_dir,
    'datasets', 'champions-league-dataset', 'UCL_AllTime_Performance_Table.csv'
)

UCL_history_finals_csv = os.path.join(
    root_dir,
    'datasets', 'champions-league-dataset', 'UCL_Finals_1955-2023.csv'
)
     
def read_csv(file_path):
    """
    Reads a CSV file
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        dataframe: A pd dataframe of the CSV data
    """
    try:
        dataframe = pd.read_csv(file_path)
        return dataframe
    except FileNotFoundError:
        print(f"Error: the file at {file_path} was not found")
    except Exception as e:
        print(f"An error occured: {e}")
        
def parse_UCL_history_finals_data(dataframe):
    """
    Parses the UCL history finals dataframe to keep only the relevant columns (season, country of winner, winner, score, runners-up, country 
    of runners-up, venue) to create a dataframe that indicates the winners and runners-up and their relevant data.
    
    Args:
        dataframe: A pd dataframe.
    
    Returns:
        pd.DataFrame: A processed dataframe with columns for the listed features.
    """
    try:
        required_columns = ['Season', 'Country', 'Winners', 'Score', 'Runners-up', 'Country.1', 'Venue', 'Notes']
        missing_columns = [col for col in required_columns if col not in dataframe.columns]
        if missing_columns:
            raise KeyError(f"The dataframe is missing these columns: {missing_columns}")
        
        dataframe.rename(columns={
            'Country': 'Winner Country',
            'Country.1': 'Runner-up Country',
        }, inplace=True)
        
        dataframe['Notes'] = dataframe['Notes'].fillna("No notes")
        
        split_score = dataframe['Score'].str.split('–', expand=True)
        if split_score.shape[1] < 2:
            raise ValueError("The 'Score' column is not in the expected 'X–Y' format.")

        dataframe['Winners Goals'] = pd.to_numeric(split_score[0], errors='coerce').fillna(0).astype(int)
        dataframe['Runners-up Goals'] = pd.to_numeric(split_score[1], errors='coerce').fillna(0).astype(int)

        # Create winners DataFrame
        winners_df = dataframe[['Season', 'Winners', 'Winner Country', 'Winners Goals', 'Runners-up Goals', 'Venue', 'Notes']].copy()
        winners_df.rename(columns={
            'Winners': 'Team',
            'Winner Country': 'Country',
            'Winners Goals': 'Goals For',
            'Runners-up Goals': 'Goals Against',
            'Venue': 'Match Venue',
            'Notes': 'Match Notes'
        }, inplace=True)
        winners_df['Result'] = 'Win'
        
        # Create runners-up DataFrame
        runners_up_df = dataframe[['Season', 'Runners-up', 'Runner-up Country', 'Runners-up Goals', 'Winners Goals', 'Venue', 'Notes']].copy()
        runners_up_df.rename(columns={
            'Runners-up': 'Team',
            'Runner-up Country': 'Country',
            'Runners-up Goals': 'Goals For',
            'Winners Goals': 'Goals Against',
            'Venue': 'Match Venue',
            'Notes': 'Match Notes'
        }, inplace=True)
        runners_up_df['Result'] = 'Loss'
        
        # Combine the two DataFrames
        combined_df = pd.concat([winners_df, runners_up_df], ignore_index=True)

        # Sort by season and result
        combined_df = combined_df.sort_values(by=['Season', 'Result'], ascending=[True, False]).reset_index(drop=True)
        
        return combined_df
    
    except KeyError as e:
        print(f"Error: Missing a column in the dataframe. Details: {e}")
    except ValueError as e:
        print(f"Error: Invalid data in the dataframe. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return pd.DataFrame()
         
def parse_UCL_history_performance_data(dataframe):
    """
    Parses the UCL all-time performance dataframe to keep only the relevant columns (team name, matches played, wins, draws, loses, goals for, goals against)
    
    Args:
        dataframe: A pd dataframe.
        
    Returns:
        pd.DataFrame: A processed dataframe with columns for the listed features.
    """
    try:
        relevant_columns = ['Team', 'M.', 'W', 'D', 'L', 'goals']
        
        if not all(col in dataframe.columns for col in relevant_columns):
            raise ValueError(f"UCL performance history dataframe is missing one or more required columns: {relevant_columns}")
        
        dataframe[relevant_columns]
          
        # Handle missing values before splitting
        dataframe['goals'] = dataframe['goals'].fillna('0:0:0')
        dataframe['goals'] = dataframe['goals'].str.replace(r':\d+$', '', regex=True)  # Remove trailing `:00` if present

        # Split 'goals' into 'Goals For' and 'Goals Against'
        split_goals = dataframe['goals'].str.split(':', expand=True)
        dataframe['Goals For'] = pd.to_numeric(split_goals[0], errors='coerce').fillna(0).astype(int)
        dataframe['Goals Against'] = pd.to_numeric(split_goals[1], errors='coerce').fillna(0).astype(int)
        
        dataframe = dataframe.drop(columns=['goals'])
        
        dataframe.rename(columns={
            'M.': 'Matches Played',
            'W': 'Wins',
            'D': 'Draws',
            'L': 'Losses'
        }, inplace=True)
        
        return dataframe
    except KeyError as e:
        print(f"Error: Missing a column in the dataframe. Details: {e}")
    except ValueError as e:
        print(f"Error: Invalid data in the dataframe. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")    
    return pd.DataFrame()    