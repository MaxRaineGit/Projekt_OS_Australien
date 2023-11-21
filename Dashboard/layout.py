from dash import html, dcc
import charts  # Import charts module

def create_layout():
    # Call functions
    sex_distribution_chart = charts.create_sex_distribution_piechart()
    top_ten_countries_chart = charts.create_top_ten_countries_diagram()
    age_group_medals_chart = charts.create_age_group_medals_diagram()
    medals_per_sport_australia_chart = charts.create_medals_per_sport_australia()
    australian_medals_per_year_chart = charts.create_australian_medals_per_year_diagram()
    histogram_australia_chart = charts.create_histogram_australia()
    medals_country_swimming_chart = charts.create_medals_country_swimming()
    age_distribution_swimming_chart = charts.create_age_distribution_swimming()
    medal_distribution_per_year_tug_of_war_chart = charts.create_medal_distribution_per_year_tug_of_war()
    age_distribution_tug_of_war_chart = charts.create_age_distribution_tug_of_war()
    cross_country_medals_per_country_chart = charts.create_cross_country_medals_per_country_diagram()
    cross_country_skiers_age_chart = charts.create_cross_country_skiers_age_diagram()

    return html.Div([
        html.H1("Olympic Games Analysis"),
        dcc.Graph(figure=sex_distribution_chart),
        dcc.Graph(figure=top_ten_countries_chart),
        dcc.Graph(figure=age_group_medals_chart),
        dcc.Graph(figure=medals_per_sport_australia_chart),
        dcc.Graph(figure=australian_medals_per_year_chart),
        dcc.Graph(figure=histogram_australia_chart),
        dcc.Graph(figure=medals_country_swimming_chart),
        dcc.Graph(figure=age_distribution_swimming_chart),
        dcc.Graph(figure=medal_distribution_per_year_tug_of_war_chart),
        dcc.Graph(figure=age_distribution_tug_of_war_chart),
        dcc.Graph(figure=cross_country_medals_per_country_chart),
        dcc.Graph(figure=cross_country_skiers_age_chart),
    ])