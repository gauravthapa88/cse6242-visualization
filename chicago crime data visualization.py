import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.io as pio
import time

start_time = time.time()

# Renaming variables
variable_mapping = {
    'ZIP Code': 'ZIP Code',
    'Household_Income_at_Age_35_rP_gP_pall': 'Household Income at 35',
    'Incarceration_Rate_rP_gP_pall': 'Incarceration Rate',
    'Individual_Income_Excluding_Spouse_at_Age_35_rP_gP_pall': 'Individual Income at 35',
    'Fraction_Married_at_Age_35_rP_gP_pall': 'Fraction Married at 35',
    'Spouse\'s_Income_at_Age_35_rP_gP_pall': 'Spouse Income at 35',
    'Employment_Rate_at_Age_35_rP_gP_pall': 'Employment Rate at 35',
    'Frac._in_Top_20%_Based_on_Household_Income_rP_gP_pall': 'Top 20% Household Income',
    'Frac._in_Top_20%_Based_on_Indiv_Income_rP_gP_pall': 'Top 20% Individual Income',
    '%_Staying_in_Same_Commuting_Zone_as_Adults_rP_gP_pall': 'Same Commuting Zone as Adults',
    '%_Staying_in_Same_Tract_as_Adults_rP_gP_pall': 'Same Tract as Adults',
    'Household_Income_Stayed_in_Commuting_Zone_rP_gP_pall': 'Household Income (Same Commuting Zone)',
    'Individual_Income_Stayed_in_Commuting_Zone_rP_gP_pall': 'Individual Income (Same Commuting Zone)',
    'Number_of_Children_rP_gP_pall': 'Number of Children',
    'kfr_rP_gP_pall': 'Income Rank',
    'two_par_rP_gP_pall': 'Two Parents',
    'married_26_rP_gP_pall': 'Married at 26',
    'married_24_rP_gP_pall': 'Married at 24',
    'married_29_rP_gP_pall': 'Married at 29',
    'kir_24_rP_gP_pall': 'Income Rank at 24',
    'kir_26_rP_gP_pall': 'Income Rank at 26',
    'working_rP_gP_pall': 'Working',
    'frac_years_xw_rP_gP_pall': 'Fraction Years Worked',
    'kir_29_rP_gP_pall': 'Income Rank at 29',
    'working_32_rP_gP_pall': 'Working at 32',
    'staytract_rP_gP_pall': 'Stayed in Same Tract',
    'kfr_26_rP_gP_pall': 'Income Rank at 26',
    'kfr_24_rP_gP_pall': 'Income Rank at 24',
    'kir_rP_gP_pall': 'Income Rank',
    'spouse_rank_rP_gP_pall': 'Spouse Income Rank',
    'staycz_rP_gP_pall': 'Stayed in Commuting Zone',
    'kfr_29_rP_gP_pall': 'Income Rank at 29',
    'stayhome_rP_gP_pall': 'Stayed at Home',
    'kfr_staycz_rP_gP_pall': 'Income Rank (Stayed in Commuting Zone)',
    'has_dad_rP_gP_pall': 'Has Father',
    'par_rank_rP_gP_pall': 'Parent Income Rank',
    'kfr_top20_rP_gP_pall': 'Top 20% Income Rank',
    'lowpov_nbhd_rP_gP_pall': 'Low Poverty Neighborhood',
    'kir_top20_rP_gP_pall': 'Top 20% Individual Income Rank',
    'kir_staycz_rP_gP_pall': 'Individual Income Rank (Stayed in Commuting Zone)',
    'married_32_rP_gP_pall': 'Married at 32',
    'count_rP_gP_pall': 'Count',
    'working_29_rP_gP_pall': 'Working at 29',
    'frac_below_med_rP_gP_pall': 'Fraction Below Median Income',
    'married_rP_gP_pall': 'Married',
    'working_24_rP_gP_pall': 'Working at 24',
    'working_26_rP_gP_pall': 'Working at 26',
    'jail_rP_gP_pall': 'Incarcerated',
    'has_mom_rP_gP_pall': 'Has Mother',
    'median_rent2016': 'Median Rent 2016',
    'nonwhite_share2010': 'Non-white Share 2010',
    'mail_return_rate2010': 'Mail Return Rate 2010',
    'med_hhinc1990_real': 'Median Household Income 1990 (Real)',
    'lfp2010': 'Labor Force Participation 2010',
    'job_density_2013': 'Job Density 2013',
    'foreign_share2016': 'Foreign Share 2016',
    'popdensity2010': 'Population Density 2010',
    'traveltime15_2016': 'Travel Time < 15 min 2016',
    'poor_share2016': 'Poverty Share 2016',
    'ann_avg_job_growth_2004_2013': 'Annual Avg Job Growth 2004-2013',
    'pop2010': 'Population 2010',
    'singleparent_share2016': 'Single Parent Share 2016',
    'unemp2015': 'Unemployment 2015',
    'hhinc_mean2010': 'Mean Household Income 2010',
    'med_hhinc2010': 'Median Household Income 2010',
    'frac_coll_plus2016': 'Fraction College+ 2016',
    'med_hhinc2016_real': 'Median Household Income 2016 (Real)',
    'violent_crime_rate': 'Violent Crime Rate',
    'wtd_avg_mean_income': 'Weighted Avg Mean Income',
    'HI_0_5000': 'Household Income $0-$5000',
    'HI_100000_149999': 'Household Income $100000-$149999',
    'HI_10000_14999': 'Household Income $10000-$14999',
    'HI_150000_more': 'Household Income $150000+',
    'HI_15000_19999': 'Household Income $15000-$19999',
    'HI_20000_24999': 'Household Income $20000-$24999',
    'HI_25000_34999': 'Household Income $25000-$34999',
    'HI_35000_49999': 'Household Income $35000-$49999',
    'HI_50000_74999': 'Household Income $50000-$74999',
    'HI_5000_9999': 'Household Income $5000-$9999',
    'HI_75000_99999': 'Household Income $75000-$99999',
    'MHCP_20_29': 'Monthly Housing Cost 20-29% of Income',
    'MHCP_30_more': 'Monthly Housing Cost 30%+ of Income',
    'MHCP_less_20': 'Monthly Housing Cost <20% of Income',
    'MHC_0_300': 'Monthly Housing Cost $0-$300',
    'MHC_1000_1499': 'Monthly Housing Cost $1000-$1499',
    'MHC_1500_1999': 'Monthly Housing Cost $1500-$1999',
    'MHC_2000_2499': 'Monthly Housing Cost $2000-$2499',
    'MHC_2500_2999': 'Monthly Housing Cost $2500-$2999',
    'MHC_3000_more': 'Monthly Housing Cost $3000+',
    'MHC_300_499': 'Monthly Housing Cost $300-$499',
    'MHC_500_799': 'Monthly Housing Cost $500-$799',
    'MHC_800_999': 'Monthly Housing Cost $800-$999',
    'Violent Crime Level': 'Violent Crime Level'
}

# Load the data
df = pd.read_csv('df_merged_model_final_imputed.csv', dtype={'ZIP Code': str})

# Ensure ZIP codes are properly formatted
df['ZIP Code'] = df['ZIP Code'].astype(str).str.zfill(5)

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
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
        html.P("After feature engineering and regression analysis, four variables were identified as significant predictors of violent crime rate:"),
        html.Ul([
            html.Li("Household Income $25,000-$34,999: Slight increase in crime rate"),
            html.Li("Household Income $150,000+: Slight decrease in crime rate"),
            html.Li("Job Density: Slight decrease in crime rate"),
            html.Li("Fraction in Top 20% (Household Income): Significant decrease in crime rate")
        ]),
        html.P(
            "This insight suggests that policymakers should focus their resources on income and employment programs, as other factors may not significantly affect crime rates based on this analysis.")
    ], style={'width': '80%', 'margin': '20px auto', 'backgroundColor': '#ffffff', 'padding': '20px',
              'borderRadius': '10px'}),

    html.Div([
        html.Label('Select Variable to Visualize',
                   style={
                       "fontFamily": "Arial, sans-serif",
                       "fontWeight": "bold",
                       "color": "#555",
                       "marginBottom": "10px"
                   }),
        dcc.Dropdown(
            id='variable-selector',
            options=[{'label': v, 'value': k} for k, v in variable_mapping.items() if
                     k not in ['ZIP Code', 'violent_crime_rate']],
            value='HI_25000_34999',
            style={
                "fontFamily": "Arial, sans-serif",
                "fontSize": "1rem"
            }
        )
    ], style={
        "width": "80%",
        "margin": "0 auto",
        "marginBottom": "20px"
    }),

    html.Div([
        html.H3("Adjust Key Predictors", style={"textAlign": "center"}),

        # Sliders for key predictors with current values displayed
        html.Label('Household Income $25,000-$34,999 (%):'),
        dcc.Slider(id='hi-25000-34999-slider', min=0, max=100, step=1,
                   value=df['HI_25000_34999'].mean(), marks={0: '0%', 50: '50%', 100: '100%(default value)'}),

        html.Label('Household Income $150,000+ (%):'),
        dcc.Slider(id='hi-150000-slider', min=0, max=100, step=1,
                   value=df['HI_150000_more'].mean(), marks={0: '0%', 50: '50%', 100: '100%(default value)'},
                   tooltip={"placement": "bottom", "always_visible": True}),

        html.Label('Job Density:'),
        dcc.Slider(id='job-density-slider', min=0, max=df['job_density_2013'].max(), step=100,
                   value=df['job_density_2013'].mean(),tooltip={"placement": "bottom", "always_visible": True}),

        html.Label('Fraction in Top 20% (Household Income):'),
        dcc.Slider(id='fraction-top20-slider', min=0, max=1, step=0.01,
                   value=df['Frac._in_Top_20%_Based_on_Household_Income_rP_gP_pall'].mean(),
                   marks={0: '0', 0.5: '0.5', 1: '1'},
                   tooltip={"placement": "bottom", "always_visible": True}),

        # Buttons for reset and apply changes
        html.Div([
            html.Button('Reset to Average', id='reset-button', n_clicks=0,
                        style={'marginRight': '10px'}),
            html.Button('Apply Changes', id='apply-button', n_clicks=0)
        ], style={'textAlign': 'center', 'marginTop': '20px'})
    ], style={'width': '80%', 'margin': '20px auto',
              'backgroundColor': '#ffffff',
              'padding': '20px',
              'borderRadius': '10px'}),

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
    [Input('variable-selector', 'value'),
     Input('hi-25000-34999-slider', 'value'),
     Input('hi-150000-slider', 'value'),
     Input('job-density-slider', 'value'),
     Input('fraction-top20-slider', 'value')]
)
def update_map(selected_variable, hi_25000_34999_change, hi_150000_change, job_density_change, fraction_top20_change):
    # Calculate predicted crime rate using actual data for each ZIP code
    df['predicted_crime_rate'] = (36.02 +
                                  0.002 * (df['HI_25000_34999'] + hi_25000_34999_change) +
                                  -0.00077 * (df['HI_150000_more'] + hi_150000_change) +
                                  -0.00004 * (df['job_density_2013'] + job_density_change) +
                                  -17.97 * (df[
                                                'Frac._in_Top_20%_Based_on_Household_Income_rP_gP_pall'] + fraction_top20_change))

    # Ensure predicted rates are non-negative
    df['predicted_crime_rate'] = df['predicted_crime_rate'].clip(lower=0)

    fig = px.choropleth(
        df,
        geojson='https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json',
        locations='ZIP Code',
        featureidkey="properties.ZCTA5CE10",
        color='predicted_crime_rate',
        color_continuous_scale="Reds",  # You can customize this scale further if needed
        range_color=[df['predicted_crime_rate'].min(), df['predicted_crime_rate'].max() * 1.25],
        # Adjusting range for better visibility
        hover_data=[selected_variable, 'predicted_crime_rate'],
        labels={
            'predicted_crime_rate': 'Predicted Crime Rate',
            selected_variable: variable_mapping[selected_variable]
        },
        scope="usa"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="Predicted Crime Rate",
            tickformat=".2f"
        ),
        title=f"Predicted Crime Rate Based on {variable_mapping[selected_variable]}",
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
        return [df['HI_25000_34999'].mean(),
                df['HI_150000_more'].mean(),
                df['job_density_2013'].mean(),
                df['Frac._in_Top_20%_Based_on_Household_Income_rP_gP_pall'].mean()]

    raise dash.exceptions.PreventUpdate


def generate_html():
    plots_html = ""
    options_html = ""

    for i, (key, value) in enumerate(variable_mapping.items()):
        if key not in ['ZIP Code', 'violent_crime_rate']:
            fig = update_map(key, df['HI_25000_34999'].mean(), df['HI_150000_more'].mean(),
                             df['job_density_2013'].mean(),
                             df['Frac._in_Top_20%_Based_on_Household_Income_rP_gP_pall'].mean())
            plot_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
            plots_html += f'<div id="plot{i}" style="display: none;">{plot_html}</div>'
            options_html += f'<option value="plot{i}">{value}</option>'

    html_string = f'''
    <html>
    <head>
        <title>Chicago Crime and Socioeconomic Data Visualization</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                background-color: #f0f0f0;
                margin: 0; 
                padding: 0; 
            }}
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px; 
            }}
            h1 {{ 
                text-align: center; 
                color: #333; 
                border-bottom: 2px solid #666; 
                padding-bottom: 10px; 
            }}
            select {{ 
                width: 80%; 
                margin: 20px auto; 
                display: block; 
                padding: 10px; 
                font-size: 16px; 
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chicago Crime and Socioeconomic Data Visualization</h1>
            <select id="variable-selector" onchange="showPlot(this.value)">
                <option value="">Select a variable</option>
                {options_html}
            </select>
            {plots_html}
        </div>
        <script>
            function showPlot(plotId) {{
                var plots = document.getElementsByTagName('div');
                for (var i = 0; i < plots.length; i++) {{
                    if (plots[i].id.startsWith('plot')) {{
                        plots[i].style.display = 'none';
                    }}
                }}
                if (plotId) {{
                    document.getElementById(plotId).style.display = 'block';
                }}
            }}
        </script>
    </body>
    </html>
    '''

    return html_string


# Generate and save the HTML file
html_content = generate_html()
with open('chicago_crime_visualization.html', 'w') as f:
    f.write(html_content)

print("HTML file 'chicago_crime_visualization.html' has been generated.")

# Time calculation
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")

if __name__ == '__main__':
    app.run_server(debug=True)