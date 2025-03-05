import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


def main():

    st.set_page_config(
        page_title="Madrid Mobility Dashboard",
        page_icon=":bar_chart:",
        layout="wide"
    )

    st.title("Madrid Mobility Dashboard")
    st.write("""
    This dashboard visualizes Uber movement data for Madrid neighborhoods in 2020.
    
    ### Features:
    - **Travel Time Analysis**: View average travel times between any two neighborhoods
    - **Day of Week Patterns**: Compare travel times across different days of the week
    - **Time Period Comparison**: Analyze how travel times vary by hour of the day
    - **Interactive Map**: Visualize the geographic distribution of travel times
             
    ### How to use: 
    - Use the sidebar to select source and destination neighborhoods to explore the data.
    - The dashboard will display the average travel time between the selected neighborhoods.
    - The map will show the geographic distribution of travel times between the selected neighborhoods.
    - The charts will display the average travel time by day of week and hour of day.
    """)
    
    st.markdown("---")
    
    
    # CHART 3
    # Calculate average travel times from the source to all other neighborhoods
    travel_times = data[data.src_neigh_name == source].groupby('dst_neigh_name')['mean_travel_time'].mean()

    # Prepare map data
    aux = codes.copy()
    aux = aux.set_index('DISPLAY_NAME')

    # Create a travel time column with missing values for neighborhoods without data
    aux['travel_time'] = np.nan
    aux.loc[travel_times.index, 'travel_time'] = travel_times
    aux['has_data'] = ~aux['travel_time'].isna()
    aux['is_source'] = aux.index == source

    # Create figure for neighborhoods with data
    fig = px.choropleth(
        aux[aux['has_data'] & ~aux['is_source']],  # Exclude source from this trace
        geojson=aux[aux['has_data'] & ~aux['is_source']].geometry,
        locations=aux[aux['has_data'] & ~aux['is_source']].index,
        color='travel_time',
        color_continuous_scale='Reds',
        range_color=[travel_times.min(), travel_times.max()],
        labels={'travel_time': 'Travel Time (seconds)'},
        title=f"Average Travel Times from {source}",
        height=600
    )

    # Add neighborhoods with no data in light gray
    no_data_trace = px.choropleth(
        aux[~aux['has_data'] & ~aux['is_source']],
        geojson=aux[~aux['has_data'] & ~aux['is_source']].geometry,
        locations=aux[~aux['has_data'] & ~aux['is_source']].index,
        color_discrete_sequence=['#e0e0e0']  # Light gray
    ).data[0]

    # Add the source neighborhood in navy blue
    source_trace = px.choropleth(
        aux[aux['is_source']],
        geojson=aux[aux['is_source']].geometry,
        locations=aux[aux['is_source']].index,
        color_discrete_sequence=['#000080']  # Navy blue
    ).data[0]

    # Add all traces to the figure
    fig.add_trace(no_data_trace)
    fig.add_trace(source_trace)

    # Update the layout
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"l":0,"b":0},
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
    
if __name__ == "__main__":
    main()