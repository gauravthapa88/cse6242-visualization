import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the data
df = pd.read_csv('df_merged_model_final_imputed.csv', dtype={'ZIP Code': str})
df['ZIP Code'] = df['ZIP Code'].astype(str).str.zfill(5)

app = dash.Dash(__name__)

# Calculate min and max job density for the slider
min_job_density = df['job_density_2013'].min()
max_job_density = df['job_density_2013'].max()

app.layout = html.Div([
    dcc.Store(id='initial-load', data=True),
    html.H1('Influence of Socioeconomic Variables on Violent Crime Rates in Chicago',
            style={
                "textAlign": "center",
                "color": "#333",
                "fontFamily": "Arial, sans-serif",
                "fontWeight": "bold",
                "fontSize": "2.5rem",
                "marginBottom": "20px",
                "borderBottom": "2px solid #666",
                "paddingBottom": "10px"
            }),

    html.Div([
        html.H3("Key Insights", style={"textAlign": "center"}),
        html.P(
            "After feature engineering and regression analysis, four variables were identified as significant predictors of violent crime rate:"),
        html.Ul([
            html.Li(
                "Number of Households with Income between $25,000-$34,999: Significant (p < 0.01) positive relationship to violent crime rate."),
            html.Li(
                "Number of Households with Income at $150,000+: Significant (p < 0.001) negative relationship to violent crime rate."),
            html.Li("Job Density: Significant (p < 0.05) negative relationship to violent crime rate."),
            html.Li(
                "Fraction In Top 20% of Individual Income: Significant (p < 0.01) negative relationship to violent crime rate.")
        ]),
        html.P(
            "This insight suggests that policymakers should focus their resources on income and employment programs to potentially reduce violent crime rates.")
    ], style={'width': '80%', 'margin': '20px auto', 'backgroundColor': '#ffffff', 'padding': '20px',
              'borderRadius': '10px'}),

    html.Div([
        html.H3("Adjust values of each predictor to visualize changes in crime rate", style={"textAlign": "center"}),
        html.Label('Household Income $25,000-$34,999'),
        html.P("Change in the number of households in this income bracket",
               style={"fontSize": "0.7em", "fontStyle": "italic"}),
        dcc.Slider(id='hi-25000-34999-slider', min=-100, max=100, step=1, value=0,
                   marks={-100: '-100%', 0: '0%(present)', 100: '100%'}),

        html.Label('Household Income $150,000+'),
        html.P("Change in the number of households in this income bracket",
               style={"fontSize": "0.7em", "fontStyle": "italic"}),
        dcc.Slider(id='hi-150000-slider', min=-100, max=100, step=1, value=0,
                   marks={-100: '-100%', 0: '0%(present)', 100: '100%'}),

        html.Label('Job Density:'),
        html.P("Number of jobs per square mile (log scale)", style={"fontSize": "0.7em", "fontStyle": "italic"}),
        dcc.Slider(id='job-density-slider', min=0, max=5, step=0.1, value=3,
                   marks={0: f'{min_job_density:.0f}(present min)', 5: f'{max_job_density:.0f}(present max)'}),

        html.Label('Fraction in Top 20% of Individual Income:'),
        html.P("Proportion of individuals in the top 20% income bracket",
               style={"fontSize": "0.7em", "fontStyle": "italic"}),
        dcc.Slider(id='fraction-top20-slider', min=0, max=1, step=0.01, value=0.2, marks={0: '0', 0.5: '0.5', 1: '1'}),
    ], style={'width': '80%', 'margin': '20px auto'}),

    html.Div([
        html.Button('Reset to Average', id='reset-button', n_clicks=0, style={'marginRight': '10px'}),
        html.Button('Apply Changes', id='apply-button', n_clicks=0)
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    dcc.Graph(id='chicago-map')
], style={
    "fontFamily": "Arial, sans-serif",
    "maxWidth": "1200px",
    "margin": "0 auto",
    "padding": "20px",
    "backgroundColor": "#f0f0f0"
})


@app.callback(
    Output('chicago-map', 'figure'),
    [Input('initial-load', 'data'),
     Input('hi-25000-34999-slider', 'value'),
     Input('hi-150000-slider', 'value'),
     Input('job-density-slider', 'value'),
     Input('fraction-top20-slider', 'value')]
)
def update_map(initial_load, hi_25000_34999_change, hi_150000_change, job_density_slider_value, fraction_top20):
    actual_job_density = 10 ** job_density_slider_value
    df['predicted_crime_rate'] = (36.02 +
                                  0.002 * (df['HI_25000_34999'] * (1 + hi_25000_34999_change / 100)) +
                                  -0.00077 * (df['HI_150000_more'] * (1 + hi_150000_change / 100)) +
                                  -0.00004 * actual_job_density +
                                  -17.97 * fraction_top20)

    df['predicted_crime_rate'] = df['predicted_crime_rate'].clip(lower=0)


    fig = px.choropleth(
        df,
        geojson='https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json',
        locations='ZIP Code',
        featureidkey="properties.ZCTA5CE10",
        color='predicted_crime_rate',
        color_continuous_scale="Reds",
        range_color=[df['predicted_crime_rate'].min(), df['predicted_crime_rate'].max() * 1.25],
        hover_data=['predicted_crime_rate'],
        labels={'predicted_crime_rate': 'Predicted Crime Rate'},
        scope="usa"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="Predicted Crime Rate",
            tickformat=".2f"
        ),
        title="Predicted Crime Rate Based on Key Predictors",
        title_font=dict(
            size=20,
            family='Arial, sans-serif',
            color='#333'
        )
    )

    return fig


@app.callback(
    [Output('hi-25000-34999-slider', 'value'),
     Output('hi-150000-slider', 'value'),
     Output('job-density-slider', 'value'),
     Output('fraction-top20-slider', 'value')],
    [Input('reset-button', 'n_clicks')]
)
def reset_sliders(n_clicks):
    if n_clicks > 0:
        return [0, 0, 3, df['Frac._in_Top_20%_Based_on_Indiv_Income_rP_gP_pall'].mean()]
    raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)