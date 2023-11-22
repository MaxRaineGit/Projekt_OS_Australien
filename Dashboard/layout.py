from dash import html, dcc, callback, Output, Input
import charts  # Import charts module


def create_layout():

    # Defining dropdown options
    dropdown_options = [
        {'label': 'Sex Distribution', 'value': 'sex_distribution'},
        {'label': 'Top Ten Countries', 'value': 'top_ten_countries'},
        {'label': 'Age Group Medals', 'value': 'age_group_medals'},
        {'label': 'Medals per Sport Australia', 'value': 'medals_per_sport_australia'},
        {'label': 'Australian Medals per Year', 'value': 'australian_medals_per_year'},
        {'label': 'Histogram Australia', 'value': 'histogram_australia'},
        {'label': 'Medals Country Swimming', 'value': 'medals_country_swimming'},
        {'label': 'Age Distribution Swimming', 'value': 'age_distribution_swimming'},
        {'label': 'Medal Distribution per Year Tug of War', 'value': 'medal_distribution_per_year_tug_of_war'},
        {'label': 'Age Distribution Tug of War', 'value': 'age_distribution_tug_of_war'},
        {'label': 'Cross Country Medals per Country', 'value': 'cross_country_medals_per_country'},
        {'label': 'Cross Country Skiers Age', 'value': 'cross_country_skiers_age'},
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
                value="sex_distribution",  # Default selected value
                searchable=False # To prevent keyboard popping up on phones
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
