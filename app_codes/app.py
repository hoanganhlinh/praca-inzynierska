from pathlib import Path
import pandas as pd
from shiny import ui, render, App

# Part 1: ui ----
# app_ui = ui.page_fluid(
#     "Hello, world!",
# )

df = pd.read_csv(Path(__file__).parent / "data\\2022-03-29-rt.gtfs\stop_times.txt")

app_ui = ui.page_fluid(
    ui.output_table("real_stop_times"),
)

def server(input, output, session):
    # ...
    @output
    @render.table
    def real_stop_times():
        return df

app = App(app_ui, server)
