import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import dash_table
import pandas as pd
import plotly.express as px

from dash.dependencies import Input, Output

# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from MongoCrud import AnimalShelter

###########################
# Data Model
###########################

username = 'testuser'
password = 'testpassword'
shelter = AnimalShelter(username, password)

# class read method must support return of cursor object and accept projection json input
df = pd.DataFrame.from_records(shelter.read({}))

#########################
# Dashboard Layout / View
#########################
# app = Dash app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    # Top section of interface
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Center([
        html.Table(
            html.Tr([
                html.Td(
                    html.A(
                        html.Img(src="https://i.ibb.co/CPsh27v/Grazioso-Salvare-Logo.png",
                                 style={'height': '25%', 'width': '25%'}
                                 ),
                        href="https://www.snhu.edu/"
                    )
                ),
                html.Td(html.B('Developed by James Richmond'))]
            )
        )]
    ),
    html.Hr(),
    html.Div(
        # Row containing radio buttons
        className="row",
        style={'display': 'flex'},
        children=[
            dcc.RadioItems(
                id='rescue_types',
                options=[
                    {'label': 'Water Rescue', 'value': 'water'},
                    {'label': 'Mountain/ Wilderness Rescue', 'value': 'mountain'},
                    {'label': 'Disaster/ Individual Tracking', 'value': 'tracking'},
                    {'label': 'Reset', 'value': 'reset'}
                ],
                value='reset',
                labelStyle={'display': 'inline-block'}
            )]
    ),
    html.Hr(),
    # Data Table
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
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
        page_size=10
    ),
    html.Br(),
    html.Hr(),
    html.Div(
        html.Tr([
            # Pie chart
            html.Td(
                dcc.Graph(
                    id='pie'
                )
            ),
            # Map
            html.Td(
                id='map-id',
                className='col s12 m6'
            )
        ])
    )
])


#############################################
# Interaction Between Components / Controller
#############################################
# Callback for map
# Changes map location focus and tooltips per selected row of table
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data"),
     Input('datatable-id', "selected_rows")])
# Calback inputs are passed as arguments
def update_map(viewData, row):
    dff = pd.DataFrame.from_dict(viewData)
    lat = float(dff.iloc[row, 14])
    long = float(dff.iloc[row, 15])
    return [
        dl.Map(
            style={
                'width': '750px',
                'height': '500px'
            },
            # Sets the center of the map
            center=[
                lat,
                long
            ],
            zoom=10,
            children=[
                dl.TileLayer(id="base-layer-id"),
                # Marker with tool tip and popup
                dl.Marker(
                    position=[
                        lat,
                        long
                    ],
                    children=[
                        dl.Tooltip(
                            dff.iloc[row, 4]),  # animal type
                        dl.Popup([
                            html.H2(dff.iloc[row, 10]),  # animal name
                            html.H3(dff.iloc[row, 5])  # animal breed
                        ])
                    ]
                )
            ]
        )
    ]


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
        dff,
        names='breed',
        title='Animals by Breed (Selection)'
    )

    return fig


# app
if __name__ == '__main__':
    app.run_server()
