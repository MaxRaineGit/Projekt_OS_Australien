from dash import html, dcc, callback, Output, Input
import charts  # Import charts module


def create_layout():

    # Defining dropdown options
    dropdown_options = [
        {'label': 'All Olympic Games - Male/Female Athlete Distribution', 'value': 'sex_distribution'},
        {'label': 'All Olympic Games - Amount of Medals Won (Top 10 Countries)', 'value': 'top_ten_countries'},
        {'label': 'All Olympic Games - Medals Won per Age Group/Sex', 'value': 'age_group_medals'},
        {'label': 'Australia - Medals Won per Sport', 'value': 'medals_per_sport_australia'},
        {'label': 'Australia - Medals Won per Olympic Game', 'value': 'australian_medals_per_year'},
        {'label': 'Australia - Age of Athletes', 'value': 'histogram_australia'},
        {'label': 'Swimming - Medals per Country', 'value': 'medals_country_swimming'},
        {'label': 'Swimming - Age Distribution', 'value': 'age_distribution_swimming'},
        {'label': 'Tug of War - Medals per Country', 'value': 'medal_distribution_per_year_tug_of_war'},
        {'label': 'Tug of War - Age Distribution', 'value': 'age_distribution_tug_of_war'},
        {'label': 'Cross Country Skiing - Medals per Country', 'value': 'cross_country_medals_per_country'},
        {'label': 'Cross Country Skiing - Age Distribution', 'value': 'cross_country_skiers_age'},
    ]

    return html.Div(
        style={
            "background-image": "url('/assets/Olympic_background.jpg')",
            "background-size" : "cover",
            "height" : "100vh",
            "padding" : "10px"
        },

        children=[
            html.H1(
                "Olympic Games Analysis",
                style={"textAlign" : "center",
                        "border" : "2px solid black",
                        "padding" : "10px",
                        "background-color" : "white"
                        }
        ),

        # Dropdown menu
            dcc.Dropdown(
                id="dropdown-menu",
                options=dropdown_options,
                searchable=False, # To prevent keyboard popping up on phones
                value= None,
                placeholder="Select a chart to display...",
                style={'backgroundColor': 'white', 'border': '10px solid white'}


        ),

        # Graph container
            dcc.Graph(id="selected-graph"),
        ]
    )


# Callback to update graph based on dropdown selection
@callback(
    Output("selected-graph", "figure"),
    [Input("dropdown-menu", "value")]
)
def update_graph(selected_option):
    if selected_option is None:
        return {} # Returns an empty chart instead of callback error

    chart_functions = {
        "sex_distribution": charts.create_sex_distribution_piechart,
        "top_ten_countries": charts.create_top_ten_countries_diagram,
        "age_group_medals": charts.create_age_group_medals_diagram,
        "medals_per_sport_australia": charts.create_medals_per_sport_australia,
        "australian_medals_per_year": charts.create_australian_medals_per_year_diagram,
        "histogram_australia": charts.create_histogram_australia,
        "medals_country_swimming": charts.create_medals_country_swimming,
        "age_distribution_swimming": charts.create_age_distribution_swimming,
        "medal_distribution_per_year_tug_of_war": charts.create_medal_distribution_per_year_tug_of_war,
        "age_distribution_tug_of_war": charts.create_age_distribution_tug_of_war,
        "cross_country_medals_per_country": charts.create_cross_country_medals_per_country_diagram,
        "cross_country_skiers_age": charts.create_cross_country_skiers_age_diagram,
    }

    return chart_functions[selected_option]()
