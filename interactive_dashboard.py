import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
df = pd.read_excel('500_Cities_Health.xlsx')
df = df.groupby("StateAbbr").mean()
df.reset_index(inplace=True)
dff = df.copy()
states = dff.iloc[:, 0]
data = dff.loc[:, "Population2010": "OBESITY_AdjPrev"]
#print(dff)
#print(states)
#print(data)
cM = df.loc[:, "Population2010": "OBESITY_AdjPrev"].corr()
#print(cM)
cor_fig = px.imshow(cM)
app.layout = html.Div([
    html.H1("Health Data For USA"),
    dcc.Dropdown(id="select_variable",
                 options=[
                     {"label": "Population", "value": "Population2010"},
                     {"label": "Binge Drinking", "value": "BINGE_AdjPrev"},
                     {"label": "High Blood Pressure", "value": "BPHIGH_AdjPrev"},
                     {"label": "Cancer", "value": "CANCER_AdjPrev"},
                     {"label": "Asthma", "value": "CASTHMA_AdjPrev"},
                     {"label": "Coronary Heart Disease", "value": "CHD_AdjPrev"},
                     {"label": "Chronic Obstructive Pulmonary Disease", "value": "COPD_AdjPrev"},
                     {"label": "Smoking", "value": "CSMOKING_AdjPrev"},
                     {"label": "Diabetes", "value": "DIABETES_AdjPrev"},
                     {"label": "Obesity", "value": "OBESITY_AdjPrev"}
                 ],
                 value="Population2010",
                 multi=False
                 ),
    dcc.Graph(id="choropleth_graph"),
    dcc.Graph(id="bar_graph"),
    dcc.Graph(id='cm_graph', figure=cor_fig),
    dcc.Graph(id="scatterplot_graph")
])
@app.callback(
    [Output(component_id="choropleth_graph", component_property="figure"),
     Output(component_id="bar_graph", component_property="figure")
     ],
    [Input(component_id="select_variable", component_property="value"),
     ]
)
def refresh_graph(selected):
    figbar = px.bar(
        dff, x="StateAbbr", y=selected, title=selected + " For US States",
    )
    figmap = px.choropleth(
        data_frame=dff, locationmode='USA-states', locations=states, scope="usa", color=selected,
    )
    return figbar, figmap

@app.callback(
    Output("scatterplot_graph", "figure"),
    [dash.dependencies.Input("cm_graph", "clickData")]
)
def update_scatter(clickData):
    if clickData is None:
        fig_scatter = px.scatter(
            dff, x="Population2010", y="Population2010", title="default"
        )
    else:
        x_var = clickData["points"][0]["x"]
        y_var = clickData["points"][0]["y"]
        fig_scatter = px.scatter(
            dff, x=x_var, y=y_var, title=x_var + " by " + y_var
        )
    return fig_scatter



if __name__ == '__main__':
    app.run_server(debug=True)
