import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Leer el archivo CSV
df = pd.read_csv('datos.csv')

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
server = app.server

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Dashboard de Vinos de Tenerife"),
    
    # Filtros
    html.Div([
        html.Label('Selecciona la denominación:'),
        dcc.Dropdown(
            id='denominacion-dropdown',
            options=[{'label': denom, 'value': denom} for denom in df['denominacion'].unique()],
            value=df['denominacion'].unique()[0]
        )
    ]),
    
    html.Div([
        html.Label('Selecciona el periodo:'),
        dcc.Slider(
            id='periodo-slider',
            min=df['periodo'].min(),
            max=df['periodo'].max(),
            step=1,
            marks={i: str(i) for i in range(df['periodo'].min(), df['periodo'].max() + 1)},
            value=df['periodo'].max()
        )
    ]),
    
    # Gráficos
    dcc.Graph(id='grafico-tinto-blanco'),
    dcc.Graph(id='grafico-total'),
])

# Callback para actualizar los gráficos basados en los filtros
@app.callback(
    [Output('grafico-tinto-blanco', 'figure'),
     Output('grafico-total', 'figure')],
    [Input('denominacion-dropdown', 'value'),
     Input('periodo-slider', 'value')]
)
def actualizar_graficos(denominacion, periodo):
    # Filtrar datos
    df_filtrado = df[(df['denominacion'] == denominacion) & (df['periodo'] <= periodo)]
    
    # Crear gráficos
    fig_tinto_blanco = px.line(df_filtrado, x='periodo', y=['Tinto', 'Blanco'],
                              labels={'value': 'Cantidad', 'periodo': 'Año'},
                              title=f'Producción de Vino Tinto y Blanco para {denominacion}')
    
    fig_total = px.line(df_filtrado, x='periodo', y='Total',
                        labels={'Total': 'Cantidad Total', 'periodo': 'Año'},
                        title=f'Producción Total de Vino para {denominacion}')
    
    return fig_tinto_blanco, fig_total

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)