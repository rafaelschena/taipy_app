from taipy import Gui
import taipy.gui.builder as tgb
from math import cos
import plotly.graph_objects as go
import plotly.express as px


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

def senoidal_data(freq=1, ampl=1, phase=0):
    return [cos(i*freq/6 + phase) * ampl for i in range(100)]

## Slider
value_slider = 9

## Gauge
value_gauge = 72
threshold = 60
delta = value_gauge - threshold

## Linear
value_linear = 50
delta_linear = value_linear - threshold

## Chart-1
phase_chart_1 = 1
data_chart_1 = senoidal_data(phase=phase_chart_1)

## Chart-2
freq_chart_2 = 1
data_chart_2 = senoidal_data(freq=freq_chart_2)

## Color maps
color_map = {
    0: "red",
    30: "orange",
    60: "yellow",
    80: "green"
}


## Plotly charts
list_to_display = [100/x for x in range(1, 100)]
fig1 = go.Figure(data=go.Scatter(y=list_to_display))

df = px.data.tips()
fig2 = px.histogram(df, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=df.columns)

### Layout da página
page = """
# ReliApp - Predictive Maintenance and Reliability Indicators
___

<|layout|columns=1 1|

<|part|render=True|
## Gauge metric
<|{value_gauge}|slider|min=0|max=100|step=1|>
<|{value_gauge}|metric|delta={delta}|threshold={threshold}|color_map={color_map}|bar_color=gray|>
|>

<|part|render=True|
## Linear metric
<|{value_linear}|slider|min=0|max=100|step=1|>
<|{value_linear}|metric|delta={delta_linear}|threshold={threshold}|type=linear|color_map={color_map}|bar_color=gray|>
|>

|>

<|layout|columns=1 1|

<|part|render=True|
## Scatterplot 1
<|{phase_chart_1}|slider|min=0|max=100|step=1|>
<|{data_chart_1}|chart|>
|>

<|part|render=True|
## Scatterplot 2
<|{freq_chart_2}|slider|min=0|max=100|step=1|>
<|{data_chart_2}|chart|>
|>

|>


<|layout|columns=1 1|

<|part|render=True|
## Plotly Figure 1
<|chart|figure={fig1}|>
|>

<|part|render=True|
## Plotly Figure 2
<|chart|figure={fig2}|>
|>

|>

"""

if __name__ == "__main__":

    Gui(page=page).run(debug=True, port=8000, host="0.0.0.0", favicon='wrench.png', title="ReliApp")

''''

'''