import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# =================================================================
# 1. DATA LOADING
# =================================================================
try:
    all_trips_v2 = pd.read_csv('all_trips_github.csv')
except FileNotFoundError:
    print("Error: 'all_trips_github.csv' not found.")

# Data processing
all_trips_v2['ride_length'] = pd.to_numeric(all_trips_v2['ride_length'], errors='coerce')
all_trips_v2['year'] = pd.to_numeric(all_trips_v2['year'], errors='coerce').fillna(0).astype(int)
all_trips_v2['hour'] = pd.to_numeric(all_trips_v2['hour'], errors='coerce')

# =================================================================
# 2. GLOBAL CONFIGURATION
# =================================================================
colors = {'casual': '#FF9800', 'member': '#2196F3'}
day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

app = dash.Dash(__name__)
server = app.server

years_list = sorted(all_trips_v2['year'].unique())
stations_list = sorted(all_trips_v2['start_station_name'].dropna().unique())

# =================================================================
# 3. DASHBOARD LAYOUT
# =================================================================
app.layout = html.Div(style={'fontFamily': 'Segoe UI, sans-serif', 'padding': '30px', 'backgroundColor': '#f8f9fa'}, children=[
    
    html.Div([
        html.H1("Cyclistic Executive Data Dashboard", style={'textAlign': 'center', 'color': '#1a2a6c', 'fontWeight': 'bold'}),
        html.P("Comparative Behavior Analysis & Resource Optimization (Filtered < 120 min)", 
               style={'textAlign': 'center', 'color': '#555', 'fontSize': '18px', 'marginBottom': '30px'})
    ]),
    
    # FILTER PANEL
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px', 'backgroundColor': 'white', 'padding': '25px', 
                    'borderRadius': '12px', 'marginBottom': '30px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)'}, children=[
        
        html.Div(style={'flex': '1'}, children=[
            html.Label("Select Year", style={'fontWeight': '600'}),
            dcc.Dropdown(id='year-dropdown', options=[{'label': str(y), 'value': y} for y in years_list], 
                         value=years_list, multi=True)
        ]),

        html.Div(style={'flex': '1'}, children=[
            html.Label("User Type", style={'fontWeight': '600'}),
            dcc.Dropdown(id='user-type-dropdown', options=[{'label': 'Member', 'value': 'member'}, {'label': 'Casual', 'value': 'casual'}],
                         value=['member', 'casual'], multi=True)
        ]),

        html.Div(style={'flex': '1.5'}, children=[
            html.Label("Day of Week", style={'fontWeight': '600'}),
            dcc.Dropdown(id='day-dropdown', options=[{'label': d, 'value': d} for d in day_order], 
                         value=day_order, multi=True)
        ]),

        html.Div(style={'flex': '2'}, children=[
            html.Label("Search Station", style={'fontWeight': '600'}),
            dcc.Dropdown(id='location-dropdown', options=[{'label': s, 'value': s} for s in stations_list], 
                         value=[], placeholder="All Stations", multi=True)
        ]),

        html.Div(style={'flex': '1'}, children=[
            html.Label("Map View Mode", style={'fontWeight': '600'}),
            dcc.RadioItems(
                id='map-view-selector',
                options=[
                    {'label': ' All Stations', 'value': 'all'},
                    {'label': ' Top 25 Stations', 'value': 'top'}
                ],
                value='all',
                labelStyle={'display': 'block'}
            )
        ])
    ]),
        html.Div(style={'display': 'flex', 'gap': '25px', 'marginBottom': '25px'}, children=[
        dcc.Graph(id='volume-chart', style={'flex': '1'}),
        dcc.Graph(id='duration-chart', style={'flex': '1'}),
    ]),
    
    html.Div(style={'display': 'flex', 'gap': '25px'}, children=[
        dcc.Graph(id='heatmap-chart', style={'flex': '1'}),
        dcc.Graph(id='map-chart', style={'flex': '1.2'})
    ])
])

# =================================================================
# 4. CALLBACKS
# =================================================================
@app.callback(
    [Output('volume-chart', 'figure'), Output('duration-chart', 'figure'),
     Output('heatmap-chart', 'figure'), Output('map-chart', 'figure')],
    [Input('year-dropdown', 'value'), Input('user-type-dropdown', 'value'),
     Input('day-dropdown', 'value'), Input('location-dropdown', 'value'),
     Input('map-view-selector', 'value')]
)
def update_dashboard(selected_years, selected_users, selected_days, selected_locations, map_view):
    
    # 1. Base Filter
    filtered_df = all_trips_v2.copy()
    if selected_years:
        filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
    if selected_users:
        filtered_df = filtered_df[filtered_df['member_casual'].isin(selected_users)]
    if selected_days:
        filtered_df = filtered_df[filtered_df['day_of_week'].isin(selected_days)]
    if selected_locations:
        filtered_df = filtered_df[filtered_df['start_station_name'].isin(selected_locations)]

    if filtered_df.empty:
        return {}, {}, {}, {}

    # 2. Outlier Removal (< 120 min)
    filtered_clean = filtered_df[filtered_df['ride_length'] < 120].copy()

    # 3. Synchronized Top 25 Logic
    if map_view == 'top':
        # Get Top 25 per user type including member_casual to avoid KeyError
        top_casual = filtered_clean[filtered_clean['member_casual'] == 'casual'].groupby(
            ['start_station_name', 'start_lat', 'start_lng', 'member_casual']).size().reset_index(name='count').sort_values('count', ascending=False).head(25)
        
        top_member = filtered_clean[filtered_clean['member_casual'] == 'member'].groupby(
            ['start_station_name', 'start_lat', 'start_lng', 'member_casual']).size().reset_index(name='count').sort_values('count', ascending=False).head(25)
        
        map_data = pd.concat([top_member, top_casual])
        # RE-FILTER EVERYTHING based on these stations
        filtered_clean = filtered_clean[filtered_clean['start_station_name'].isin(map_data['start_station_name'])]
    else:
        map_data = filtered_clean.groupby(
            ['start_station_name', 'start_lat', 'start_lng', 'member_casual']).size().reset_index(name='count')

    # --- Chart 1: Volume ---
    fig1 = px.histogram(filtered_clean, x="member_casual", color="member_casual",
                        color_discrete_map=colors, title="Total Ride Volume",
                        labels={'member_casual': 'User Type'}, text_auto='.2s')

    # --- Chart 2: Average Duration (CORRECTED) ---
    avg_dur = filtered_clean.groupby(['day_of_week', 'member_casual'])['ride_length'].mean().reset_index()
    avg_dur['ride_length'] = avg_dur['ride_length'].round(1)
    
    fig2 = px.bar(avg_dur, x="day_of_week", y="ride_length", color="member_casual",
                  barmode="group", color_discrete_map=colors, category_orders={"day_of_week": day_order},
                  title="Average Trip Duration (Cleaned Metrics)",
                  text="ride_length", labels={'ride_length': 'Avg Minutes'})
    fig2.update_traces(textposition='outside', texttemplate='%{text} min')

    # --- Chart 3: Heatmap ---
    heat_data = filtered_clean.groupby(['day_of_week', 'hour']).size().reset_index(name='count')
    fig3 = px.density_heatmap(heat_data, x="hour", y="day_of_week", z="count",
                             category_orders={"day_of_week": day_order},
                             title="Peak Demand Hours", color_continuous_scale="Viridis_r")

    # --- Chart 4: Map ---
    fig4 = px.scatter_mapbox(map_data.sort_values('count', ascending=False), lat="start_lat", lon="start_lng", size="count",
                            color="member_casual", color_discrete_map=colors,
                            hover_name="start_station_name", zoom=10, height=550, 
                            title="Active Station Distribution")
    fig4.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":40,"l":0,"b":0})
    fig4.update_traces(marker=dict(opacity=0.6))

    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run(debug=True)