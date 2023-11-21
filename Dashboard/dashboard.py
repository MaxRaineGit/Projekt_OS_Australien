import dash
from dash import html

testapp = dash.Dash(__name__)

testapp.layout = html.Div(
    children=[
        html.H1(children="Dash App with Plotly Express HTML Files"),

        # Iframe for the first Plotly Express HTML file
        html.Iframe(
            srcDoc=open("../Visualisering/Cross_country_medals_per_country.html", "r", encoding="utf-8").read(),
            width="100%",
            height="500"),

        # Iframe for the second Plotly Express HTML file
        html.Iframe(
            srcDoc=open("../Visualisering/Medals_country_swimming.html", "r", encoding="utf-8").read(),
            width="100%",
            height="500"),

        # Add more Iframes as needed for additional HTML files
    ]
)

if __name__ == "__main__":
    testapp.run_server(debug=True)
