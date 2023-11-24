import pandas as pd
import plotly_express as px

# Load datasets
data_athletes = pd.read_csv('Data/athlete_events.csv')

# Charts as functions
def create_sex_distribution_piechart():
    data_unique_athletes = data_athletes.drop_duplicates(subset=['ID'])
    sex_distribution = data_unique_athletes['Sex'].value_counts()
    return px.pie(
        sex_distribution,
        names=sex_distribution.index.map(lambda x: 'Female' if x == 'F' else 'Male'),
        values=sex_distribution.values,
        title='Sex distribution of all athletes'
    )

def create_top_ten_countries_diagram():
    # Creates a new dataframe grouping that only shows the columns "Team" and "Total Medals"
    # Value_counts Counts the values for each row
    # Unstack transforms the groupby into a new dataframe
    # fillna changes the missing data to having a value of 0 so it wont effect the counting
    # Sum counts everthing in the first axis which is "Total Medals" after we used reset_index to both reset the index and change the name of the second column.
    country_medals = data_athletes.groupby("NOC")["Medal"].value_counts().unstack().fillna(0).sum(axis=1).reset_index(name="Total Medals")

    # Sorts the dataframe by Total medals and creates a new dataframe with the top 10
    top_ten_countries = country_medals.sort_values(by="Total Medals", ascending=False).head(10)
    
    return px.bar(
        top_ten_countries,
        x="NOC", y="Total Medals",
        title="Top 10 countries based on total medals won",
        color="NOC"
    )

def create_age_group_medals_diagram():
    athlete_age_medal = data_athletes[["Sex", "Age", "Medal"]].dropna(subset=["Age"]).fillna({"Medal": "No medal"})
    age_bins = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    athlete_age_medal["Age Group"] = pd.cut(athlete_age_medal["Age"], bins=age_bins, labels=[f'{i}-{i+9}' for i in age_bins[:-1]])
    age_group_medals = athlete_age_medal.groupby(["Sex", "Age Group", "Medal"], observed=False).size().unstack(fill_value=0)
    age_group_medals_melted = pd.melt(age_group_medals.reset_index(), id_vars=["Sex", "Age Group"], var_name="Medal", value_name="Count")
    return px.bar(
        age_group_medals_melted,
        x="Age Group",
        y="Count",
        color="Medal",
        barmode="group",
        facet_col="Sex",
        title="Medal Counts per Age Group and Sex"
    )

def create_medals_per_sport_australia():
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])]
    australian_medals = australian_athletes.dropna(subset=['Medal'])
    medal_counts = australian_medals['Sport'].value_counts()
    return px.bar(
        medal_counts, 
        x=medal_counts.index, 
        y=medal_counts.values, 
        title='Number of Medals per Sport for Australia',
        labels={'x': 'Sport', 'y': 'Number of Medals'}
    )

def create_australian_medals_per_year_diagram():
    australian_medals = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])].dropna(subset=['Medal'])
    australian_medals_per_year = australian_medals.groupby(["Season", "Year", "Medal"]).size().unstack(fill_value=0)
    australian_medals_per_year = australian_medals_per_year[["Gold", "Silver", "Bronze"]].reset_index()
    return px.bar(
        australian_medals_per_year,
        x="Year",
        y=["Gold", "Silver", "Bronze"],
        color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "brown"},
        barmode="stack",
        facet_col="Season",
        title="Amount of medals per Olympic games for Australia",
    )

def create_histogram_australia():
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])]
    
    histogram = px.histogram(
        australian_athletes,
        x="Age",
        nbins=25,
        title="Age of Australian Olympic athletes"
    )

    # Creating a gap between each bar so it's easier to look at
    histogram.update_layout(
        bargap=0.2
    )

    return histogram

def create_medals_country_swimming():
    filitered_swimming = data_athletes[data_athletes["Sport"] == "Swimming"]
    # Creates a series by grouping NOC and medal column together.
    # .size() counts the values in each group
    # unstack(fill_value=0) reshapes it into a dataframe again, while also changing the NaN values to 0
    # reset_index() resets the index again
    medals_swimming = filitered_swimming.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()

    # Filtering out the countries who has participated but has not won any medals
    medals_swimming = medals_swimming[medals_swimming[["Gold", "Silver", "Bronze"]].sum(axis=1) > 0]

    # Sorting the countries based on total medals for easier readability
    medals_swimming["Total Medals"] = medals_swimming[["Gold", "Silver", "Bronze"]].sum(axis=1)
    medals_swimming = medals_swimming.sort_values(by="Total Medals", ascending=False)

    # Taking the top 20 countries for easier readability
    medals_swimming = medals_swimming.head(20)
    return px.bar(
        medals_swimming,
        x="NOC",
        y=["Gold", "Silver", "Bronze"],
        title="Amount of Swimming medals per country",
        labels={"NOC": "Country", "value": "Medals"},
        barmode="group"
    )

def create_age_distribution_swimming():
    filitered_swimming = data_athletes[data_athletes["Sport"] == "Swimming"]
    
    swimming_histogram = px.histogram(
        filitered_swimming,
        x="Age",
        nbins=10,
        title="Age distribution of swimmers"
    )

    swimming_histogram.update_layout(
        bargap=0.2
    )

    return swimming_histogram

def create_medal_distribution_per_year_tug_of_war():
    tug_of_war_data = data_athletes[data_athletes['Sport'] == 'Tug-Of-War']
    noc_medal_year_data = tug_of_war_data.groupby(['NOC', 'Year', 'Medal']).size().reset_index(name='Count')
    return px.histogram(
        noc_medal_year_data, 
        x="NOC",  
        y="Count",
        color="Medal",
        facet_col="Year",
        title="Medal Distribution Among Countries in Tug-Of-War by Years",
        labels={'NOC': 'National Olympic Committee', 'Count': 'Number of Medals per team'}
    )

def create_age_distribution_tug_of_war():
    tug_of_war_age_data = data_athletes[data_athletes['Sport'] == 'Tug-Of-War']['Age'].dropna()
    return px.histogram(
        tug_of_war_age_data, 
        x="Age",
        title="Age Distribution Among Athletes in Tug-Of-War",
        labels={'Age': 'Age of Athletes'}
    )

def create_cross_country_medals_per_country_diagram():
    cross_country_skiers = data_athletes[data_athletes["Sport"] == "Cross Country Skiing"]
    cross_country_medals = cross_country_skiers.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()
    cross_country_medals["Total Medals"] = cross_country_medals["Gold"] + cross_country_medals["Silver"] + cross_country_medals["Bronze"]
    return px.bar(
        cross_country_medals,
        x="NOC",
        y=["Gold", "Silver", "Bronze"],
        title="Amount of cross country skiing medals per country",
        labels={"value": "Medal Count", "NOC": "Country"},
        barmode="stack"
    )

def create_cross_country_skiers_age_diagram():
    cross_country_skiers = data_athletes[data_athletes["Sport"] == "Cross Country Skiing"]
    return px.histogram(
        cross_country_skiers,
        x="Age",
        title="Age distribution of Cross Country Skiers",
        labels={'Age': 'Age of Athletes'}
    )