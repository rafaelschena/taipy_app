from taipy import Gui
import taipy.gui.builder as tgb
from math import cos
import plotly.graph_objects as go
import plotly.express as px
from utils import *
import pandas as pd
from sklearn.preprocessing import MinMaxScaler



def plot_line(df, col):
    fig = px.line(
                    df,
                    x=df.index,
                    y=col,
                    # labels={"value": "Valor", "variable": "Features"},
                    # title=f"{col} temporal evolution"
                    )
    return fig

def create_gauge(serie):
    min = serie.min()
    max = serie.max()
    fig = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = serie.values[-1],
    delta = {'reference': serie.values[-2]},
    gauge={
        "axis": {"range": [min, max]},
        "bar": {"color": "blue"},
        "steps": [
            {"range": [min, 0.5*max], "color": "lightgreen"},
            {"range": [0.5*max, 0.8*max], "color": "yellow"},
            {"range": [0.8*max, max], "color": "red"}
        ],
        # "threshold": {
        #     "line": {"color": "black", "width": 4},
        #     "value": 90
        # }
    }
    # title = {'text': text},
    # domain = {'x': [0, 1], 'y': [0, 1]}
    ))

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
        state.df = state.df_scaled[:int(state.idx)]
        # state.delta_series = state.df.iloc[-1] - state.df.iloc[-2]
        # state.dic_figs = {col: plot_line(state.df, col) for col in state.df.columns}
        state.dic_gauges = {col: create_gauge(state.df[col]) for col in state.df.columns}
        state.plot_page_1 = plot_line(state.df, ['lp', 'v', 'P48', 'T48'])
        return

def senoidal_data(freq=1, ampl=1, phase=0):
    return [cos(i*freq/6 + phase) * ampl for i in range(100)]


## Plotly charts
df_orig = load_data_naval_pdm()
idx=100
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df_orig)
df_scaled = pd.DataFrame(scaled_data, columns=df_orig.columns)
df = df_scaled[:idx]
# delta_series = df.iloc[-1] - df.iloc[-2]
# dic_figs = {col: plot_line(df, col) for col in df.columns}
dic_gauges = {col: create_gauge(df[col]) for col in df.columns}
plot_page_1 = plot_line(df, ['lp', 'v', 'P48', 'T48'])

show_pane = True

### Layout da página
page = """
<|toggle|theme|>
<|layout|columns=300px 1fr|
<|padding=10px|
### Change the number to simulate time elapsing:
<|{idx}|number|min=100|max={df_orig.index.max()}|>
|>
<|layout|columns=1fr|
# ReliApp - Predictive Maintenance and Reliability Indicators
<|layout|columns=1 1 1 1|
<|part|render=True|
### lp - Lever position
<|chart|figure={dic_gauges['lp']}|height=300px|>
|>
<|part|render=True|
### v - ship speed
<|chart|figure={dic_gauges['v']}|height=300px|>
|>
<|part|render=True|
### P48 - HP exit pressure
<|chart|figure={dic_gauges['P48']}|height=300px|>
|>
<|part|render=True|
### T48 - HP exit temp
<|chart|figure={dic_gauges['T48']}|height=300px|>
|>
|>
  \
  \
<|part|render=True|
<|chart|figure={plot_page_1}|height=300px|>
|>
|>
|>
"""

if __name__ == "__main__":

    Gui(page=page).run(port=8000, host="0.0.0.0", favicon='wrench.png', title="ReliApp", watermark='')
