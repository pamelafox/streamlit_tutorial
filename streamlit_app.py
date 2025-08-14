import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv("state_data.csv")

st.header("US State Demographics")

# Let user select which state to graph
state = st.selectbox("State:", df["State"].unique())

# Create a graph of total population
df_state = df[df["State"] == state]
fig = px.line(
    df_state, x="Year", y="Total Population", title=f"Total Population of {state}"
)
st.plotly_chart(fig)

# Show the entire dataframe
st.write("All Data")
st.dataframe(df)

# Add a bar graph of the current population of each state
fig = px.bar(
    df, x="State", y="Total Population", title="Total Population by State"
)
st.plotly_chart(fig)

# Calculate the slope from 2021-2023 for each state, and display a sorted table of slopes
# add input for start year and end year
start_year = st.number_input("Start Year:", min_value=2006, value=2021)
end_year = st.number_input("End Year:", max_value=2023, value=2023)

# check if year is BETWEEN or INCLUDING the start and end years
df_slope = df[df["Year"].between(start_year, end_year)]

df_slope = df_slope.groupby("State").apply(lambda x: (x["Total Population"].iloc[-1] - x["Total Population"].iloc[0]) / 2)
# display slope as table
st.write(f"Population Change ({start_year}-{end_year})")

# display as a horizontal bar graph so that states are on the Y axis, SORTED by the largest increase
df_slope = df_slope.sort_values(ascending=False, key=lambda x: x.abs())
fig = px.bar(
    df_slope,
    x=df_slope.values,
    y=df_slope.index,
    title=f"Population Change ({start_year}-{end_year}) by State",
    orientation="h",
    height=20*len(df_slope)
)
st.plotly_chart(fig)
st.dataframe(df_slope)
