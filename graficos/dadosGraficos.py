# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import numpy as np

# Incorporate data
df = pd.read_csv('../eshop.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Ofertas Nintendo Eshop'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.bar(df, x='Desconto', y='Título')),
    dcc.Graph(figure=px.pie(df, values='Desconto', names='Título'))
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
