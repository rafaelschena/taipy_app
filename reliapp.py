from taipy import Gui
import taipy.gui.builder as tgb

## Slider
value_slider = 9

## Gauge
value_gauge = 72
threshold = 60
delta = value_gauge - threshold

## Linear
value_linear = 50
delta_linear = value_linear - threshold

def on_change(state, var_name, var_value):
    if var_name == "value_gauge":
        state.delta = var_value - state.threshold
        return
    elif var_name == "value_linear":
        state.delta_linear = var_value - state.threshold
        return

### Layout da página
page = """
# ReliApp - Predictive Maintenance and Reliability Indicators
___
## Gauge metric
<|{value_gauge}|metric|delta={delta}|threshold={threshold}|>
<|{value_gauge}|slider|min=0|max=100|step=1|>

## Linear metric
<|{value_linear}|metric|delta={delta_linear}|threshold={threshold}|type=linear|>
<|{value_linear}|number|min=0|max=100|step=1|>
"""

if __name__ == "__main__":

    Gui(page=page).run(debug=True, port=8000, host="0.0.0.0", favicon='wrench.png', title="ReliApp")