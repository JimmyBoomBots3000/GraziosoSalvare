import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_table
import pandas as pd
import plotly.express as px

from dash.dependencies import Input, Output
from MongoCrud import AnimalShelter

###########################
# Data Model
###########################

username = 'testuser'
password = 'testpassword'
shelter = AnimalShelter(username, password)

# class read method supports return of cursor object and accepts projection json input
df = pd.DataFrame.from_records(shelter.read({}))

#########################
# Dashboard Layout / View
#########################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = 'Grazioso Salvare'

app.layout = html.Div([

    dbc.Row([
        dbc.Col(
            html.A(html.Img(src="https://i.ibb.co/n1X1XgS/img.png", style={'height': '150px'}),
                   href="https://www.snhu.edu/"),
            width='auto',
            align='center'),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    html.H3("Animal Finder Dashboard"), width={'size': True}, align='center'),
                dbc.Col(
                    html.A(html.Img(src="https://www.python.org/static/community_logos/python-powered-w-70x28.png"),
                           href="https://www.python.org/about/"
                           ),
                    width=1)
            ]),
            dbc.Row([
                dbc.Col([
                    # html.Hr(),
                    # Row containing radio buttons
                    html.Div(
                        className="row",
                        style={'display': 'flex'},
                        children=[
                            dbc.RadioItems(
                                id='rescue_types',
                                options=[
                                    {'label': 'Water Rescue', 'value': 'water'},
                                    {'label': 'Mountain/ Wilderness Rescue', 'value': 'mountain'},
                                    {'label': 'Disaster/ Individual Tracking', 'value': 'tracking'},
                                    {'label': 'Reset', 'value': 'reset'}
                                ],
                                value='reset',
                            )
                        ]
                    ),
                    # html.Hr()
                ],
                    width=True),
            ],
                justify='left')
        ])
    ],
        style={'backgroundColor': 'rgb(255,230,230)'}),

    dbc.Row([
        dbc.Col(
            # Data Table
            dash_table.DataTable(
                id='datatable-id',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                    # {"name": i, "id": i} for i in df.columns
                ],
                data=df.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable=False,
                row_selectable="single",
                row_deletable=False,
                page_action="native",
                selected_rows=[],
                selected_columns=[],
                page_current=0,
                page_size=10,
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                }
            ),
            width=12)
    ]),

    dbc.Row([
        dbc.Col(
            # Pie Chart
            dcc.Graph(
                id='pie'),
            width=6),
        dbc.Col(
            # Map
            dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer")],
                   id="map-id",
                   style={'width': '100%', 'height': '45vh', 'margin': "auto", "display": "block"},
                   center=[30.31880634, -97.72403767],
                   zoom=6,
                   ),
            width=6),
    ]),
],
    style={'padding': '15px'}

)


#############################################
# Interaction Between Components / Controller
#############################################
# Callback for map
# Changes map location focus and tooltips per selected row of table
@app.callback(
    [
        Output('layer', "children"),
        Output('map-id', 'center'),
        Output('map-id', 'zoom')
    ],
    [
        Input('datatable-id', "derived_viewport_data"),
        Input('datatable-id', "selected_rows")
    ]
)
# Callback inputs are passed as arguments
def update_map(viewdata, row):
    dff = pd.DataFrame.from_dict(viewdata)

    if row is not None:
        lat = float(dff.iloc[row, 14])
        long = float(dff.iloc[row, 15])

        animal_type = str(dff.iloc[row, 4].item())
        breed = str(dff.iloc[row, 5].item())

        animal_name = str(dff.iloc[row, 10].item())
        if animal_name == '':
            animal_name = '[No name]'

        children = [
            # Marker with tool tip and popup
            dl.TileLayer(id="base-layer-id"),
            dl.Marker(
                position=[
                    lat,
                    long
                ],
                children=[
                    dl.Tooltip(
                        animal_type),
                    dl.Popup([
                        html.H3(animal_name),
                        html.H4(breed)
                    ])
                ]
            )
        ]

        # Center map on selection
        center = [lat, long]
        return children, center, 10
    else:
        return None, None, 10


# Callback for radio buttons
# queries the database and returns results to data table
@app.callback(
    Output("datatable-id", "data"),
    [Input("rescue_types", "value")]
)
def filter_rescue_types(selected_type):
    if selected_type == 'water':
        dff = pd.DataFrame(
            list(shelter.read(
                {"$and": [
                    {"$or": [
                        {"breed": {"$regex": ".*Labrador.*"}},
                        {"breed": {"$regex": ".*Chesa.*"}},
                        {"breed": {"$regex": ".*Newfoundland.*"}},
                    ]},
                    {"sex_upon_outcome": "Intact Female"},
                    {"$and": [
                        {"age_upon_outcome_in_weeks": {"$gte": 26}},
                        {"age_upon_outcome_in_weeks": {"$lte": 156}},
                    ]}
                ]}
            ))
        )

    if selected_type == 'mountain':
        dff = pd.DataFrame(
            list(shelter.read(
                {"$and": [
                    {"$or": [
                        {"breed": {"$regex": ".*German Shep.*"}},
                        {"breed": {"$regex": ".*Malamute.*"}},
                        {"breed": {"$regex": ".*Old English Sheepdog.*"}},
                        {"breed": {"$regex": ".*Siberian.*"}},
                        {"breed": {"$regex": ".*Rottweiler.*"}},
                    ]},
                    {"sex_upon_outcome": "Intact Male"},
                    {"$and": [
                        {"age_upon_outcome_in_weeks": {"$gte": 26}},
                        {"age_upon_outcome_in_weeks": {"$lte": 156}},
                    ]}
                ]}
            ))
        )

    if selected_type == 'tracking':
        dff = pd.DataFrame(
            list(shelter.read(
                {"$and": [
                    {"$or": [
                        {"breed": {"$regex": ".*Doberman.*"}},
                        {"breed": {"$regex": ".*German Shep.*"}},
                        {"breed": {"$regex": ".*Golden Retriever Mix.*"}},
                        {"breed": {"$regex": ".*Bloodhound Mix.*"}},
                        {"breed": {"$regex": ".*Rottweiler.*"}},
                    ]},
                    {"sex_upon_outcome": "Intact Male"},
                    {"$and": [
                        {"age_upon_outcome_in_weeks": {"$gte": 20}},
                        {"age_upon_outcome_in_weeks": {"$lte": 300}},
                    ]}
                ]}
            ))
        )

    elif selected_type == 'reset':
        dff = pd.DataFrame(list(shelter.read({})))

    return dff.to_dict('records')


# Callback for pie chart
@app.callback(
    Output("pie", "figure"),
    [Input("datatable-id", "data")]
)
def generate_chart(data):
    dff = pd.DataFrame.from_dict(data)

    fig = px.pie(
        data_frame=dff,
        names='breed',
    )

    fig.update_traces(textposition='inside')

    return fig


# app
if __name__ == '__main__':
    app.run_server()
