import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

#st.title("Mona Mahdavi- Project 2 - World Happiness Dashboard")
title_parts = "Mona Mahdavi - Project 2 - World Happiness Dashboard".split(" - ")
for part in title_parts:
    st.title(part)
    
st.write("Explore Insights from the World Happiness Report Dataset with Interactive Charts.")

# Load the data
#df = pd.read_csv('/Users/mona/Desktop/Northeastern/1st Semester/6600/Project/Project-02/happiness_converted.csv')
df = pd.read_csv('happiness_converted.csv')

# Interactive Filters
st.sidebar.header("Filters")

# Continent Filter
continents = list(df["Continent"].unique())  
continents.insert(0, "All")  
selected_continents = st.sidebar.multiselect("Select Continent(s)", continents, default="All")

if "All" in selected_continents:
    filtered_data = df
else:
    filtered_data = df[df["Continent"].isin(selected_continents)]

# Score Filter
min_score, max_score = st.sidebar.slider(
    "Select Score Range", 
    float(df["Score"].min()), 
    float(df["Score"].max()), 
    (float(df["Score"].min()), float(df["Score"].max()))
)

# Rank Filter
top_10_countries = st.sidebar.checkbox("Show Top 10 Countries by Overall Rank")

if top_10_countries:
    filtered_data = filtered_data.nsmallest(10, "Overall rank") 


selected_countries = st.sidebar.multiselect("Select Countries", df["Country or region"].unique(), default=[])

# showing whole data
st.header("Data")
st.dataframe(filtered_data)


# 1 Barchart- Scores 
st.subheader("Happiness Score by Country")
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(data=filtered_data, x="Country or region", y="Score", palette="viridis", ax=ax)
#ax.set_title("Happiness Score by Country")
ax.set_xlabel("Country")
ax.set_ylabel("Hapiiness Score")
plt.xticks(rotation=45)
st.pyplot(fig)

# 2 Pichart - Portions of Continents
st.subheader("Happiness Score Ratio by Continents")
continent_scores = df.groupby("Continent")["Score"].sum()

fig, ax = plt.subplots(figsize=(12, 8))
ax.pie(
    continent_scores, 
    labels=continent_scores.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=plt.cm.tab10.colors
)
#ax.set_title("Happiness Score Share by Continent")
st.pyplot(fig)


#3 Scatter Plot - Relationship between Happiness and Healthy Life Expectancy
st.subheader("Happiness Score and Healthy Life Expectancy Relationship")
fig, ax = plt.subplots(figsize=(12, 8))
sns.scatterplot(
    data=filtered_data, 
    x="Healthy life expectancy", 
    y="Score", 
    hue="Continent", 
    palette="Set2", 
    s=100, 
    ax=ax
)
#ax.set_title("Happiness vs Healthy Life Expectancy")
ax.set_xlabel("Healthy Life Expectancy")
ax.set_ylabel("Happiness Score")
plt.grid(True)
st.pyplot(fig)

filtered_data = df[
    (df["Continent"].isin(selected_continents) if "All" not in selected_continents else True) &
    (df["Score"] >= min_score) & 
    (df["Score"] <= max_score)]


# 4 Bar Plot - Average GDP per Capita  
st.subheader("Average GDP per Capita by Country")
if not filtered_data.empty:
    gdp_by_country = (
        filtered_data.groupby("Country or region")["GDP per capita"]
        .mean()
        .sort_values(ascending=False))

    fig, ax = plt.subplots(figsize=(10, 6))
    gdp_by_country.plot(kind="bar", ax=ax, color="orange")
    ax.set_xlabel("Country")
    ax.set_ylabel("Average GDP per Capita")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.write("Select at least one continent to display Bar Plot")


# 5 Map- Generosity by Country
st.subheader("Generosity by Country")

if not filtered_data.empty:
    fig = px.choropleth(
        filtered_data,
        locations="Country or region", 
        locationmode="country names",  
        color="Generosity",  
        hover_name="Country or region",  
        color_continuous_scale="Plasma")
    st.plotly_chart(fig)
else:
    st.write("Select ‘All’ from the sidebar to display the map.")


#6 Bar Plot - Key Indicators for Selected Countries

if selected_countries:
    filtered_countries = df[df["Country or region"].isin(selected_countries)]
    st.subheader("Key Indicators for Selected Countries")
    bar_data = filtered_countries.melt(
        id_vars=["Country or region"],
        value_vars=["Score", "GDP per capita", "Social support", 
                    "Healthy life expectancy", "Freedom to make life choices", 
                    "Generosity", "Perceptions of corruption"],
        var_name="Indicator",
        value_name="Value",
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=bar_data, x="Indicator", y="Value", hue="Country or region", ax=ax)
    ax.set_title("Comparison of Key Indicators")
    ax.set_ylabel("Value")
    ax.set_xlabel("Indicator")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.write("Please select at least one country to view the Bar plot.")

# 7 Radar- Comparison of Indicators for Selected Countries

st.subheader("Comparison of Key Indicators for Selected Countries")

selected_countries = st.sidebar.multiselect(
    "Radar Filter ", 
    df["Country or region"].unique(), 
    default=[], 
    key="country_multiselect")

if selected_countries:
    country_data = filtered_data[filtered_data["Country or region"].isin(selected_countries)]
    radar_data = country_data.melt(
        id_vars=["Country or region"],
        value_vars=["Score", "GDP per capita", "Social support", 
                    "Healthy life expectancy", "Freedom to make life choices", 
                    "Generosity", "Perceptions of corruption"],
        var_name="Indicator",
        value_name="Value",)

    fig = px.line_polar(
        radar_data,
        r="Value",
        theta="Indicator",
        color="Country or region",
        line_close=True,
    )
    st.plotly_chart(fig)
else:
    st.write("Please select at least one country from <<Radar Filter>> to compare.")



# 8 Heatmap: Correlation between Indicators

st.subheader("Correlation Matrix of Selected Indicators")

if not filtered_data.empty:
    numeric_columns = ["Score", "GDP per capita", "Social support", 
                       "Healthy life expectancy", "Freedom to make life choices", 
                       "Generosity", "Perceptions of corruption"]
    
    correlation_matrix = filtered_data[numeric_columns].corr()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)
else:
    st.write("Select at Least on Continet to display the Matrix.")

    
