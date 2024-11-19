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


### Layout da página
page = """
# ReliApp - Predictive Maintenance and Reliability Indicators
___
<|{idx}|number|min=100|max={df_orig.index.max()}|>
___

<|layout|columns=1 1|

<|part|render=True|
## lp
<|{df['lp'].values[-1]}|metric|delta={delta_series['lp']}|bar_color=gray|min={df['lp'].min()}|max={df['lp'].max()}|>
|>

<|part|render=True|
## lp time evolution
<|chart|figure={dic_figs['lp']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## v
<|{df['v'].values[-1]}|metric|delta={delta_series['v']}|bar_color=gray|min={df['v'].min()}|max={df['v'].max()}|>
|>

<|part|render=True|
## v time evolution
<|chart|figure={dic_figs['v']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## GTT
<|{df['GTT'].values[-1]}|metric|delta={delta_series['GTT']}|bar_color=gray|min={df['GTT'].min()}|max={df['GTT'].max()}|>
|>

<|part|render=True|
## GTT time evolution
<|chart|figure={dic_figs['GTT']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## GTn
<|{df['GTn'].values[-1]}|metric|delta={delta_series['GTn']}|bar_color=gray|min={df['GTn'].min()}|max={df['GTn'].max()}|>
|>

<|part|render=True|
## GTn time evolution
<|chart|figure={dic_figs['GTn']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## GGn
<|{df['GGn'].values[-1]}|metric|delta={delta_series['GGn']}|bar_color=gray|min={df['GGn'].min()}|max={df['GGn'].max()}|>
|>

<|part|render=True|
## GGn time evolution
<|chart|figure={dic_figs['GGn']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## Ts
<|{df['Ts'].values[-1]}|metric|delta={delta_series['Ts']}|bar_color=gray|min={df['Ts'].min()}|max={df['Ts'].max()}|>
|>

<|part|render=True|
## Ts time evolution
<|chart|figure={dic_figs['Ts']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## Tp
<|{df['Tp'].values[-1]}|metric|delta={delta_series['Tp']}|bar_color=gray|min={df['Tp'].min()}|max={df['Tp'].max()}|>
|>

<|part|render=True|
## Tp time evolution
<|chart|figure={dic_figs['Tp']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## T48
<|{df['T48'].values[-1]}|metric|delta={delta_series['T48']}|bar_color=gray|min={df['T48'].min()}|max={df['T48'].max()}|>
|>

<|part|render=True|
## T48 time evolution
<|chart|figure={dic_figs['T48']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## T1
<|{df['T1'].values[-1]}|metric|delta={delta_series['T1']}|bar_color=gray|min={df['T1'].min()}|max={df['T1'].max()}|>
|>

<|part|render=True|
## T1 time evolution
<|chart|figure={dic_figs['T1']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## T2
<|{df['T2'].values[-1]}|metric|delta={delta_series['T2']}|bar_color=gray|min={df['T2'].min()}|max={df['T2'].max()}|>
|>

<|part|render=True|
## T2 time evolution
<|chart|figure={dic_figs['T2']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## P48
<|{df['P48'].values[-1]}|metric|delta={delta_series['P48']}|bar_color=gray|min={df['P48'].min()}|max={df['P48'].max()}|>
|>

<|part|render=True|
## P48 time evolution
<|chart|figure={dic_figs['P48']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## P1
<|{df['P1'].values[-1]}|metric|delta={delta_series['P1']}|bar_color=gray|min={df['P1'].min()}|max={df['P1'].max()}|>
|>

<|part|render=True|
## P1 time evolution
<|chart|figure={dic_figs['P1']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## P2
<|{df['P2'].values[-1]}|metric|delta={delta_series['P2']}|bar_color=gray|min={df['P2'].min()}|max={df['P2'].max()}|>
|>

<|part|render=True|
## P2 time evolution
<|chart|figure={dic_figs['P2']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## Pexh
<|{df['Pexh'].values[-1]}|metric|delta={delta_series['Pexh']}|bar_color=gray|min={df['Pexh'].min()}|max={df['Pexh'].max()}|>
|>

<|part|render=True|
## Pexh time evolution
<|chart|figure={dic_figs['Pexh']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## TIC
<|{df['TIC'].values[-1]}|metric|delta={delta_series['TIC']}|bar_color=gray|min={df['TIC'].min()}|max={df['TIC'].max()}|>
|>

<|part|render=True|
## TIC time evolution
<|chart|figure={dic_figs['TIC']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## mf
<|{df['mf'].values[-1]}|metric|delta={delta_series['mf']}|bar_color=gray|min={df['mf'].min()}|max={df['mf'].max()}|>
|>

<|part|render=True|
## mf time evolution
<|chart|figure={dic_figs['mf']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## kMc
<|{df['kMc'].values[-1]}|metric|delta={delta_series['kMc']}|bar_color=gray|min={df['kMc'].min()}|max={df['kMc'].max()}|>
|>

<|part|render=True|
## kMc time evolution
<|chart|figure={dic_figs['kMc']}|>
|>

|>
___


<|layout|columns=1 1|

<|part|render=True|
## kMt
<|{df['kMt'].values[-1]}|metric|delta={delta_series['kMt']}|bar_color=gray|min={df['kMt'].min()}|max={df['kMt'].max()}|>
|>

<|part|render=True|
## kMt time evolution
<|chart|figure={dic_figs['kMt']}|>
|>

|>
___

        

"""

if __name__ == "__main__":

    Gui(page=page).run(port=8000, host="0.0.0.0", favicon='wrench.png', title="ReliApp", watermark='')

''''
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
'''