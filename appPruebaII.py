import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Leer el archivo CSV
df = pd.read_csv('datos.csv')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1("Dashboard de Vinos de Tenerife", className="title"),
        
        # Filtros
        html.Div([
            html.Label('Selecciona la denominación:', className="filter-label"),
            dcc.Dropdown(
                id='denominacion-dropdown',
                options=[{'label': denom, 'value': denom} for denom in df['denominacion'].unique()],
                value=df['denominacion'].unique()[0]
            )
        ]),
        
        html.Div([
            html.Label('Selecciona el periodo:', className="filter-label"),
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
    ], className="container")
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
                              title=f'Producción de Vino Tinto y Blanco para {denominacion}',
                              color_discrete_map={'Tinto': '#800000', 'Blanco': '#FFD700'},
                              template='plotly_white')
    fig_tinto_blanco.update_layout(
        plot_bgcolor='#f5f5f5',
        paper_bgcolor='#f5f5f5',
        title_font=dict(size=20, color='#003366'),
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#e5e5e5')
    )
    
    fig_total = px.line(df_filtrado, x='periodo', y='Total',
                        labels={'Total': 'Cantidad Total', 'periodo': 'Año'},
                        title=f'Producción Total de Vino para {denominacion}',
                        line_shape='spline',
                        template='plotly_white')
    fig_total.update_traces(line=dict(color='#003366'))
    fig_total.update_layout(
        plot_bgcolor='#f5f5f5',
        paper_bgcolor='#f5f5f5',
        title_font=dict(size=20, color='#003366'),
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#e5e5e5')
    )
    
    return fig_tinto_blanco, fig_total


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)