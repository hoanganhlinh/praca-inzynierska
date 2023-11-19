from shiny import ui, render, App
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import os
from datetime import datetime
# from shinywidgets import output_widget, render_widget
# import plotly.express as px
# import plotly.graph_objs as go


######################### DATA TRANSFORMATION #########################

directory = "../app_codes/data/" # set your path
day = "2022-03-29"
filepath = directory +  day
stop_times_df = pd.read_csv(filepath + '.gtfs/stop_times.txt')
filepath += "-rt.gtfs"
rt_stop_times_df = pd.read_csv(filepath + "/stop_times.txt")
merged_df = stop_times_df.merge(rt_stop_times_df, on=['trip_id', 'stop_id'])

merged_df['arrival_time_x'] = merged_df['arrival_time_x'].str.strip()
merged_df['arrival_time_y'] = merged_df['arrival_time_y'].str.strip()
merged_df['diff'] = pd.to_timedelta(merged_df['arrival_time_y'], errors='coerce') - pd.to_timedelta(merged_df['arrival_time_x'], errors='coerce')
merged_df['diff'] = merged_df['diff'].apply(lambda x: pd.Timedelta.total_seconds(x))
# print(merged_df.head(5))

# Calculate the 2.5% and 97.5% quantiles of the 'diff' column
lower_quantile = merged_df['diff'].quantile(0.025)
upper_quantile = merged_df['diff'].quantile(0.975)
# Filter the dataframe to keep values within the 2.5% - 97.5% range
filtered_df = merged_df[(merged_df['diff'] >= lower_quantile) & (merged_df['diff'] <= upper_quantile)]
# print(filtered_df.head(5))


######################### APP CODE #########################

app_ui = ui.page_fluid(
    ui.output_table("time_diff"),
    ui.output_plot("a_scatter_plot"),
)

def server(input, output, session):
    @output

    @render.table
    def time_diff():
        return merged_df.head(5)
    
    @render.plot
    def a_scatter_plot():

        fig, ax = plt.subplots(1,1)
        fig.set_size_inches(10,5)
        
        return filtered_df['diff'].hist(ax=ax, bins = 50)
    

app = App(app_ui, server)
