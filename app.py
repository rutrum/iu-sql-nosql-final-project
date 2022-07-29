from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import requests
import json

app = Dash(__name__,
           #external_stylesheets=["https://cdn.jsdelivr.net/npm/water.css@2/out/light.css"]
           )

api_url = "http://localhost:5000"

hosts = pd.read_json(f"{api_url}/host")
locations = pd.read_json(f"{api_url}/location")

def into_long_form(data):
    df = {}
    for row in data:
        for key,val in row.items():
            if key in df:
                df[key] = df[key] + [val]
            else:
                df[key] = [val]
    return df

# fig = px.bar(into_long_form(hosts), x="name", y="listings_count")
fig = px.scatter_mapbox(locations.sample(1000), lat="latitude", lon="longitude", hover_name="name",
                        hover_data=["price", "number_of_reviews"],
    color_discrete_sequence=["fuchsia"], zoom=10, height=1200)
fig.update_layout(mapbox_style="open-street-map")

print(locations.head())

app.layout = html.Div(children=[
    html.H1(children='Airbnb Host Explorer'),

    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Locational Data', children=[
            dcc.Graph(
                id='geo',
                figure=fig
            )
        ]),
        dcc.Tab(label='Host Data', children=[
            dash_table.DataTable(
                id="hosts",
                data=hosts.to_dict('records'),
                columns=[{"name": i, "id": i} for i in sorted(hosts.columns)],
                filter_action='native',
                sort_action='native',
                hidden_columns=["id", "host_id", "location_id"],
            )
        ]),
    ]),

    #dash_table.DataTable(data=hosts),
])

if __name__ == '__main__':
    app.run_server(debug=True)
