import pandas as pd
import plotly_express as px

# Load datasets
data_athletes = pd.read_csv('Data/athlete_events.csv')

def apply_universal_styles(fig):
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0.9)',  
        plot_bgcolor='rgba(255,255,255,0.9)',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="right",
            x=1
        ),
        autosize=True
    )
    return fig

# Charts as functions
def create_sex_distribution_piechart():
    data_unique_athletes = data_athletes.drop_duplicates(subset=['ID'])
    sex_distribution = data_unique_athletes['Sex'].value_counts()
    fig = px.pie(
        sex_distribution,
        names=sex_distribution.index.map(lambda x: 'Female' if x == 'F' else 'Male'),
        values=sex_distribution.values,
        title='Sex distribution of all athletes'
    )
    # Apply universal styling
    fig = apply_universal_styles(fig)
    return fig

def create_top_ten_countries_diagram():
    country_medals = data_athletes.groupby("NOC")["Medal"].value_counts().unstack().fillna(0).sum(axis=1).reset_index(name="Total Medals")
    top_ten_countries = country_medals.sort_values(by="Total Medals", ascending=False).head(10)
    fig = px.bar(
        top_ten_countries,
        x="NOC", y="Total Medals",
        title="Top 10 countries based on total medals won",
        color="NOC"
    )
    fig = apply_universal_styles(fig)
    return fig

def create_age_group_medals_diagram():
    athlete_age_medal = data_athletes[["Sex", "Age", "Medal"]].dropna(subset=["Age"]).fillna({"Medal": "No medal"})
    age_bins = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    athlete_age_medal["Age Group"] = pd.cut(athlete_age_medal["Age"], bins=age_bins, labels=[f'{i}-{i+9}' for i in age_bins[:-1]])
    age_group_medals = athlete_age_medal.groupby(["Sex", "Age Group", "Medal"], observed=False).size().unstack(fill_value=0)
    age_group_medals_melted = pd.melt(age_group_medals.reset_index(), id_vars=["Sex", "Age Group"], var_name="Medal", value_name="Count")
    fig = px.bar(
        age_group_medals_melted,
        x="Age Group",
        y="Count",
        color="Medal",
        barmode="group",
        facet_col="Sex",
        title="Medal Counts per Age Group and Sex"
    )
    fig = apply_universal_styles(fig)
    return fig

def create_medals_per_sport_australia():
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])]
    australian_medals = australian_athletes.dropna(subset=['Medal'])
    medal_counts = australian_medals['Sport'].value_counts()
    fig = px.bar(
        medal_counts, 
        x=medal_counts.index, 
        y=medal_counts.values, 
        title='Number of Medals per Sport for Australia',
        labels={'x': 'Sport', 'y': 'Number of Medals'}
    )
    fig = apply_universal_styles(fig)
    return fig

def create_australian_medals_per_year_diagram():
    australian_medals = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])].dropna(subset=['Medal'])
    australian_medals_per_year = australian_medals.groupby(["Season", "Year", "Medal"]).size().unstack(fill_value=0)
    australian_medals_per_year = australian_medals_per_year[["Gold", "Silver", "Bronze"]].reset_index()
    fig = px.bar(
        australian_medals_per_year,
        x="Year",
        y=["Gold", "Silver", "Bronze"],
        color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "brown"},
        barmode="stack",
        facet_col="Season",
        title="Amount of medals per Olympic games for Australia",
    )
    fig = apply_universal_styles(fig)
    return fig

def create_histogram_australia():
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])]
    fig = px.histogram(
        australian_athletes,
        x="Age",
        nbins=25,
        title="Age of Australian Olympic athletes"
    )
    fig = apply_universal_styles(fig)
    return fig

def create_medals_country_swimming():
    filitered_swimming = data_athletes[data_athletes["Sport"] == "Swimming"]
    medals_swimming = filitered_swimming.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()
    medals_swimming = medals_swimming[medals_swimming[["Gold", "Silver", "Bronze"]].sum(axis=1) > 0]
    fig = px.bar(
        medals_swimming,
        x="NOC",
        y=["Gold", "Silver", "Bronze"],
        title="Amount of Swimming medals per country",
        labels={"NOC": "Country", "value": "Medals"},
        barmode="group"
    )
    fig = apply_universal_styles(fig)
    return fig

def create_age_distribution_swimming():
    filitered_swimming = data_athletes[data_athletes["Sport"] == "Swimming"]
    fig = px.histogram(
        filitered_swimming,
        x="Age",
        nbins=10,
        title="Age distribution of swimmers"
    )
    fig = apply_universal_styles(fig)
    return fig

def create_medal_distribution_per_year_tug_of_war():
    tug_of_war_data = data_athletes[data_athletes['Sport'] == 'Tug-Of-War']
    noc_medal_year_data = tug_of_war_data.groupby(['NOC', 'Year', 'Medal']).size().reset_index(name='Count')
    fig = px.histogram(
        noc_medal_year_data, 
        x="NOC",  
        y="Count",
        color="Medal",
        facet_col="Year",
        title="Medal Distribution Among Countries in Tug-Of-War by Years",
        labels={'NOC': 'National Olympic Committee', 'Count': 'Number of Medals per team'}
    )
    fig = apply_universal_styles(fig)
    return fig

def create_age_distribution_tug_of_war():
    tug_of_war_age_data = data_athletes[data_athletes['Sport'] == 'Tug-Of-War']['Age'].dropna()
    fig = px.histogram(
        tug_of_war_age_data, 
        x="Age",
        title="Age Distribution Among Athletes in Tug-Of-War",
        labels={'Age': 'Age of Athletes'}
    )
    fig = apply_universal_styles(fig)
    return fig

def create_cross_country_medals_per_country_diagram():
    cross_country_skiers = data_athletes[data_athletes["Sport"] == "Cross Country Skiing"]
    cross_country_medals = cross_country_skiers.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()
    cross_country_medals["Total Medals"] = cross_country_medals["Gold"] + cross_country_medals["Silver"] + cross_country_medals["Bronze"]
    fig = px.bar(
        cross_country_medals,
        x="NOC",
        y=["Gold", "Silver", "Bronze"],
        title="Amount of cross country skiing medals per country",
        labels={"value": "Medal Count", "NOC": "Country"},
        barmode="stack"
    )
    fig = apply_universal_styles(fig)
    return fig

def create_cross_country_skiers_age_diagram():
    cross_country_skiers = data_athletes[data_athletes["Sport"] == "Cross Country Skiing"]
    fig = px.histogram(
        cross_country_skiers,
        x="Age",
        title="Age distribution of Cross Country Skiers",
        labels={'Age': 'Age of Athletes'}
    )
    fig = apply_universal_styles(fig)
    return fig