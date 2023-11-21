import dash
from layout import create_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.layout = create_layout()

if __name__ == '__main__':
    app.run_server(debug=True)