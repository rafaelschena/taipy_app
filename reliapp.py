from taipy import Gui
import taipy.gui.builder as tgb
from math import cos
import plotly.graph_objects as go
import plotly.express as px
from utils import *
import pandas as pd


def plot_line(df, col):
    fig = px.line(
                    df,
                    x=df.index,
                    y=df[col],
                    # labels={"value": "Valor", "variable": "Features"},
                    # title=f"{col} temporal evolution"
                    )
    return fig


def on_change(state, var_name, var_value):
    if var_name == "value_gauge":
        state.delta = var_value - state.threshold
        return
    elif var_name == "value_linear":
        state.delta_linear = var_value - state.threshold
        return
    elif var_name == "phase_chart_1":
        state.data_chart_1 = senoidal_data(phase=state.phase_chart_1)
        return
    elif var_name == "freq_chart_2":
        state.data_chart_2 = senoidal_data(freq=state.freq_chart_2)
        return
    elif var_name == "idx":
        state.df = state.df_orig[:int(state.idx)]
        state.delta_series = state.df.iloc[-1] - state.df.iloc[-2]
        state.dic_figs = {col: plot_line(state.df, col) for col in state.df.columns}
        return

def senoidal_data(freq=1, ampl=1, phase=0):
    return [cos(i*freq/6 + phase) * ampl for i in range(100)]


## Plotly charts
df_orig = load_data_naval_pdm()
idx=100
df = df_orig[:idx]
delta_series = df.iloc[-1] - df.iloc[-2]
dic_figs = {col: plot_line(df, col) for col in df.columns}

show_pane = True

### Layout da página
page = """
<|toggle|theme|>

<|layout|columns=300px 1fr|

<|padding=10px|
### Change the number to simulate time elapsing:
<|{idx}|number|min=100|max={df_orig.index.max()}|>
|>

<|padding=50px|
# ReliApp - Predictive Maintenance and Reliability Indicators
<|layout|columns=1 1|
<|part|render=True|
### lp - Lever position
<|{df['lp'].values[-1]}|metric|delta={delta_series['lp']}|bar_color=darkgoldenrod|min={df['lp'].min()}|max={df['lp'].max()}|>
|>

<|part|render=True|
### lp history
<|chart|figure={dic_figs['lp']}|>
|>

|>
|>

|>
"""

if __name__ == "__main__":

    Gui(page=page).run(port=8000, host="0.0.0.0", favicon='wrench.png', title="ReliApp", watermark='')

'''
<|{show_pane}|pane|anchor=left|width=220|active=False|>
Change the number to simulate the time elapsing:
<|{idx}|number|min=100|max={df_orig.index.max()}|>
|>

## Slider
value_slider = 9

## Color maps
color_map = {
    0: "red",
    30: "orange",
    60: "yellow",
    80: "green"
}


## Gauge
value_gauge = 72
threshold = 60
delta = value_gauge - threshold

<|{value_gauge}|slider|min=0|max=100|step=1|>
<|{show_pane}|pane|anchor=left|width=200|active=True|
|>

<|part|render=True|
### P48 - HP exit pressure
<|{df['P48'].values[-1]}|metric|delta={delta_series['P48']}|bar_color=darkgoldenrod|min={df['P48'].min()}|max={df['P48'].max()}|>
|>

<|part|render=True|
### T48 - HP exit temperature
<|{df['T48'].values[-1]}|metric|delta={delta_series['T48']}|bar_color=darkgoldenrod|min={df['T48'].min()}|max={df['T48'].max()}|>
|>

<|part|render=True|
### P48 history
<|chart|figure={dic_figs['P48']}|>
|>
<|part|render=True|
### T48 history
<|chart|figure={dic_figs['T48']}|>
|>

<|layout|columns=1 1|

<|part|render=True|
### v - Ship speed
<|{df['v'].values[-1]}|metric|delta={delta_series['v']}|bar_color=darkgoldenrod|min={df['v'].min()}|max={df['v'].max()}|>
|>

<|part|render=True|
### v history
<|chart|figure={dic_figs['v']}|>
|>

'''