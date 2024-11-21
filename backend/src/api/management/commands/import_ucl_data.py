from django.core.management.base import BaseCommand
from api.models import UCL_history_finals, UCL_history_performance
from api.util.csv.csv_parsers import parse_UCL_history_finals_data, parse_UCL_history_performance_data
import os
import pandas as pd

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UCL_allTime_performance_table_csv = os.path.join(
    root_dir,
    'datasets', 'champions-league-dataset', 'UCL_AllTime_Performance_Table.csv'
)

UCL_history_finals_csv = os.path.join(
    root_dir,
    'datasets', 'champions-league-dataset', 'UCL_Finals_1955-2023.csv'
)

class Command(BaseCommand):
    
    def handle(sef, *args, **options):
        
        # Implementation to import UCL history finals CSV data
        ucl_finals_dataframe = pd.read_csv(UCL_history_finals_csv)
        ucl_finals_parsed_dataframe = parse_UCL_history_finals_data(ucl_finals_dataframe)
        
        if not ucl_finals_parsed_dataframe.empty:
            for index, row in ucl_finals_parsed_dataframe.iterrows():
                UCL_history_finals.objects.create(
                    season=row['Season'],
                    team=row['Team'],
                    goals_for=row['Goals For'],
                    goals_against=row['Goals Against'],
                    match_venue=row['Match Venue'],
                    match_notes=row['Match Notes'],
                    result=row['Result']
                )
            print("Successfully imported UCL finals CSV data")
        else:
            print("Failed to import UCL finals data as its data is empty")
            
        # Implementation to import UCL all time performance CSV data
        ucl_performance_dataframe = pd.read_csv(UCL_allTime_performance_table_csv)
        ucl_performance_parsed_dataframe = parse_UCL_history_performance_data(ucl_performance_dataframe)
        
        if not ucl_performance_parsed_dataframe.empty:
            for index, row in ucl_performance_parsed_dataframe.iterrows():
                UCL_history_performance.objects.create(
                    rank=row['Rank'],
                    team=row['Team'],
                    matches_played=row['Matches Played'],
                    wins=row['Wins'],
                    draws=row['Draws'],
                    losses=row['Losses'],
                    goals_for=row['Goals For'],
                    goals_against=row['Goals Against']
                )
            print("Successfully imported UCL all time performance data")
        else:
            print("Failed to import UCL performance data as its data is empty")
                
        