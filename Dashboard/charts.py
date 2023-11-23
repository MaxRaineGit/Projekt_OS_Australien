import pandas as pd
import plotly_express as px

# Load datasets
data_athletes = pd.read_csv('Data/athlete_events.csv')

def apply_universal_styles(fig):
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0.9)',  
        plot_bgcolor='rgba(255,255,255,0.9)',
        autosize=True,
        legend_bgcolor='rgba(255,255,255,0.01)'
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
        title="Top 10 countries based on total medals won:",
        color="NOC",
        labels={"NOC": "Countries", "Total Medals": "Medals"}
    )
    fig = apply_universal_styles(fig)
    return fig

def create_age_group_medals_diagram():
    athlete_age_medal = data_athletes[["Sex", "Age", "Medal"]].dropna(subset=["Age"]).fillna({"Medal": "No medal"})
    age_stats = athlete_age_medal["Age"]
    age_stats_by_sex = athlete_age_medal.groupby("Sex")["Age"]
    age_stats.describe()
    age_stats_by_sex.describe()

    age_bins = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    athlete_age_medal["Age Group"] = pd.cut(athlete_age_medal["Age"], bins=age_bins, labels=[f'{i}-{i+9}' for i in age_bins[:-1]])
    age_group_medals = athlete_age_medal.groupby(["Sex", "Age Group", "Medal"], observed=False).size().unstack(fill_value=0)
    age_group_medals = age_group_medals[["Gold", "Silver", "Bronze"]]
    age_group_medals
    age_group_medals_melted = pd.melt(age_group_medals.reset_index(), id_vars=["Sex", "Age Group"], var_name="Medal", value_name="Count")

    fig = px.bar(
    age_group_medals_melted,
    x="Age Group",
    y="Count",
    color="Medal",
    color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "brown"},
    barmode="group",
    facet_col="Sex",
    category_orders={"Medal": ["Gold", "Silver", "Bronze", "No medal"]},
    labels={"Count": "Medal Count", "Age Group": "Age Group"},
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
    fig.update_layout(xaxis_tickangle=-45)
    fig = apply_universal_styles(fig)
    return fig

def create_australian_medals_per_year_diagram():
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])]
    australian_medals = australian_athletes.dropna(subset=['Medal'])
    australian_medals_per_year = australian_medals.groupby(["Season", "Year", "Medal"]).size().unstack(fill_value=0)
    australian_medals_per_year = australian_medals_per_year[["Gold", "Silver", "Bronze"]].reset_index()

    fig = px.bar(
    australian_medals_per_year,
    x="Year",
    y=["Gold", "Silver", "Bronze"],
    color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "brown"},
    barmode="stack",
    facet_col="Season",
    labels={"value": "Medal Count", "Year": "Year"},
    title="Amount of medals per olympic games for Australia",
)
    fig = apply_universal_styles(fig)
    return fig

def create_histogram_australia():
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])]
    fig = px.histogram(
    australian_athletes,
    x="Age",
    nbins=25,
    title="Age of Australian olympic athletes"
)
    fig.update_layout(
    bargap=0.2
)
    fig = apply_universal_styles(fig)
    return fig

def create_medals_country_swimming():
    filter_sport = "Swimming"
    filitered_swimming = data_athletes[data_athletes["Sport"] == filter_sport]
    medals_swimming = filitered_swimming.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()
    medals_swimming = medals_swimming[medals_swimming[["Gold", "Silver", "Bronze"]].sum(axis=1) > 0]
    medals_swimming["Total Medals"] = medals_swimming[["Gold", "Silver", "Bronze"]].sum(axis=1)
    medals_swimming = medals_swimming.sort_values(by="Total Medals", ascending=False)
    medals_swimming = medals_swimming.head(20)

    fig = px.bar(
        medals_swimming,
        x="NOC",
        y=["Gold", "Silver", "Bronze"],
        labels={"NOC": "Country", "value" : "Medals"},
        barmode="group",
        title="Amount of Swimming medals per country"
)
    fig = apply_universal_styles(fig)
    return fig

def create_age_distribution_swimming():
    filter_sport = "Swimming"
    filitered_swimming = data_athletes[data_athletes["Sport"] == filter_sport]
    medals_swimming = filitered_swimming.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()
    medals_swimming = medals_swimming[medals_swimming[["Gold", "Silver", "Bronze"]].sum(axis=1) > 0]

    fig = px.histogram(
        filitered_swimming,
        x="Age",
        nbins=10,
        title="Age distrubution of swimmers"
)
    fig.update_layout(
    bargap=0.1
)
    fig = apply_universal_styles(fig)
    return fig

def create_medal_distribution_per_year_tug_of_war():
    tug_of_war_data = data_athletes[data_athletes['Sport'] == 'Tug-Of-War']
    noc_medal_year_data = tug_of_war_data.groupby(['NOC', 'Year', 'Medal']).size().reset_index(name='Count')
    noc_medal_year_data = noc_medal_year_data.sort_values(by='Year')

    fig = px.histogram(
        noc_medal_year_data, 
        x="NOC",  
        y="Count",
        color="Medal",
        facet_col="Year",
        color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "#cd7f32"},
        title="Medal Distribution Among Countries in Tug-Of-War by Years",
        labels={'NOC': 'National Olympic Committee', 'Count': 'Number of Medals per team'}
    )

    fig.update_xaxes(tickangle=-90)
    for annotation in fig.layout.annotations:
        annotation.text = annotation.text.split("=")[-1]

    fig = apply_universal_styles(fig)
    return fig

def create_age_distribution_tug_of_war():
    tug_of_war_data = data_athletes[data_athletes['Sport'] == 'Tug-Of-War']
    tug_of_war_age_data = tug_of_war_data[tug_of_war_data['Age'].notna()]
    min_age = tug_of_war_age_data['Age'].min()
    max_age = tug_of_war_age_data['Age'].max()

    fig = px.histogram(
        tug_of_war_age_data, 
        x="Age",
        nbins=int(max_age - min_age + 1),
        title="Age Distribution Among Athletes in Tug-Of-War",
        labels={'Age': 'Age of Athletes'}
)
    fig.update_layout(bargap = 0.2)
    fig.update_xaxes(dtick=1)

    fig = apply_universal_styles(fig)
    return fig

def create_cross_country_medals_per_country_diagram():
    cross_country_skiers = data_athletes[data_athletes["Sport"] == "Cross Country Skiing"]
    cross_country_medals = cross_country_skiers.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()
    cross_country_medals["Total Medals"] = cross_country_medals["Gold"] + cross_country_medals["Silver"] + cross_country_medals["Bronze"]
    cross_country_medals_sorted = cross_country_medals.sort_values(by='Total Medals', ascending=False)
    cross_country_medals_sorted[["NOC", "Gold", "Silver", "Bronze"]]

    fig = px.bar(
        cross_country_medals_sorted,
        x="NOC",
        y=["Gold", "Silver", "Bronze"],
        color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "brown"},
        barmode="stack",
        labels={"value": "Medal Count", "NOC": "Country"},
        title="Amount of cross country skiing medals per country",
)
    fig = apply_universal_styles(fig)
    return fig

def create_cross_country_skiers_age_diagram():
    cross_country_skiers = data_athletes[data_athletes["Sport"] == "Cross Country Skiing"]
    cross_country_medals = cross_country_skiers.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()
    cross_country_medals["Total Medals"] = cross_country_medals["Gold"] + cross_country_medals["Silver"] + cross_country_medals["Bronze"]
    cross_country_medals_sorted = cross_country_medals.sort_values(by='Total Medals', ascending=False)
    cross_country_medals_sorted[["NOC", "Gold", "Silver", "Bronze"]]

    fig = px.histogram(
        cross_country_skiers,
        x="Age",
        title="Age distribution of Cross Country Skiers",
        labels={'Age': 'Age of Athletes'}
    )
    fig = px.histogram(
    cross_country_skiers,
    x="Age"
)
    fig.update_layout(bargap=0.2)

    fig = apply_universal_styles(fig)
    return fig