import pandas as pd
import plotly_express as px

# Load dataset
data_athletes = pd.read_csv('Data/athlete_events.csv')

# Functions:


# Applies universal styling to the plotly figures for consistency and readability.
def apply_universal_styles(fig):
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0.9)',  
        plot_bgcolor='rgba(255,255,255,0.9)',
        autosize=True,
        legend_bgcolor='rgba(255,255,255,0.01)'
    )
    return fig

# Charts
def create_sex_distribution_piechart():
    # Remove duplicate entries based on 'ID' to ensure each athlete is counted only once.
    data_unique_athletes = data_athletes.drop_duplicates(subset=['ID'])
    sex_distribution = data_unique_athletes['Sex'].value_counts() # Count the number of male and female participants

    # Create a pie chart
    fig = px.pie(
        sex_distribution,
        names=sex_distribution.index.map(lambda x: 'Female' if x == 'F' else 'Male'), # Used to map "F" to "Female" and "M" to "Male".
        values=sex_distribution.values,
        title='Sex distribution of all athletes'
    )
    # Apply universal styling
    fig = apply_universal_styles(fig)
    return fig

def create_top_ten_countries_diagram():
    # Creates a new dataframe grouping that only shows the columns "Team" and "Total Medals"
    # Value_counts Counts the values for each row
    # Unstack transforms the groupby into a new dataframe
    # fillna changes the missing data to having a value of 0 so it wont effect the counting
    # Sum counts everthing in the first axis which is "Total Medals" after we used reset_index to both reset the index and change the name of the second column.
    country_medals = data_athletes.groupby("NOC")["Medal"].value_counts().unstack().fillna(0).sum(axis=1).reset_index(name="Total Medals")
    top_ten_countries = country_medals.sort_values(by="Total Medals", ascending=False).head(10)

    # Create a bar chart
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
    # Create dataframe grouping with athletes age, sex and medal
    # Dropping rows without age data and filling NaN in Medals with "No medal"
    athlete_age_medal = data_athletes[["Sex", "Age", "Medal"]].dropna(subset=["Age"]).fillna({"Medal": "No medal"})

    # Defining age bins
    # Creating new column "Age Group" based on the age bins
    age_bins = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    athlete_age_medal["Age Group"] = pd.cut(athlete_age_medal["Age"], bins=age_bins, labels=[f'{i}-{i+9}' for i in age_bins[:-1]])

    # Group by "Sex", "Age Group" and "Medals" and count the medal occurrences
    # Sort the columns, gold first, no medal last.
    age_group_medals = athlete_age_medal.groupby(["Sex", "Age Group", "Medal"], observed=False).size().unstack(fill_value=0)
    age_group_medals = age_group_medals[["Gold", "Silver", "Bronze"]]

    # Melt the DataFrame for easier plotting
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
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])] # Filter for Australian participants, including Australasia.
    australian_medals = australian_athletes.dropna(subset=['Medal']) # Filter for rows where a medal has been won
    medal_counts = australian_medals['Sport'].value_counts() # Group by sport and count the number of medals

    fig = px.bar(
        medal_counts, 
        x=medal_counts.index, 
        y=medal_counts.values, 
        title='Number of Medals per Sport for Australia',
        labels={'x': 'Sport', 'y': 'Number of Medals'}
    )
    fig.update_layout(xaxis_tickangle=-45) # Rotating values on the x-axis
    fig = apply_universal_styles(fig)
    return fig

def create_australian_medals_per_year_diagram():
    # Filter for Australian participants, including Australasia.
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])]

    # Create dataframe grouping australian medals per season, year and medal amounts
    # Sort the columns, gold first, bronze last
    australian_medals = australian_athletes.dropna(subset=['Medal'])
    australian_medals_per_year = australian_medals.groupby(["Season", "Year", "Medal"]).size().unstack(fill_value=0)
    australian_medals_per_year = australian_medals_per_year[["Gold", "Silver", "Bronze"]].reset_index()

    # Create stacked bar chart to show results
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
    # Filter for Australian participants, including Australasia.
    australian_athletes = data_athletes[data_athletes['NOC'].isin(['AUS', 'ANZ'])]

    # Creating the diagram
    fig = px.histogram(
        australian_athletes,
        x="Age",
        nbins=25,
        title="Age of Australian olympic athletes"
)
    fig.update_layout(
    bargap=0.2 # Creating a gap between each bar so it's easier to look at
)
    fig = apply_universal_styles(fig)
    return fig

def create_medals_country_swimming():
    filter_sport = "Swimming"

    # Filteres the data so only swimmers are left
    filitered_swimming = data_athletes[data_athletes["Sport"] == filter_sport]

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

    # Filteres the data so only swimmers are left
    filitered_swimming = data_athletes[data_athletes["Sport"] == filter_sport]

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
    # Filter for Tug-Of-War
    tug_of_war_data = data_athletes[data_athletes['Sport'] == 'Tug-Of-War']

    # Grouping data by year, medal and 'NOC'
    # .size() for amount of medals per group
    # .reset_index() transforms the result into a new DataFrame column "Count" for size of each group
    noc_medal_year_data = tug_of_war_data.groupby(['NOC', 'Year', 'Medal']).size().reset_index(name='Count')
    noc_medal_year_data = noc_medal_year_data.sort_values(by='Year') # Sorting the years chronologically

    fig = px.histogram(
        noc_medal_year_data, 
        x="NOC",  
        y="Count",
        color="Medal",
        facet_col="Year", # Separete grid for each year
        color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "#cd7f32"}, # Colouring the medal bars
        title="Medal Distribution Among Countries in Tug-Of-War by Years",
        labels={'NOC': 'Countries', 'Count': 'Number of Medals per team'}
    )

    fig.update_xaxes(tickangle=-90)
    # Updating each annotation showing only the numerical value of what year is represented
    for annotation in fig.layout.annotations:
        annotation.text = annotation.text.split("=")[-1]

    fig = apply_universal_styles(fig)
    return fig

def create_age_distribution_tug_of_war():
    # Filter for Tug-Of-War
    tug_of_war_data = data_athletes[data_athletes['Sport'] == 'Tug-Of-War']

    # Removing entries with missing 'Age' values to ensure accurate age analysis.
    tug_of_war_age_data = tug_of_war_data[tug_of_war_data['Age'].notna()]

    # Determining the minimum and maximum ages of Tug-Of-War athletes for histogram bin calculation.
    min_age = tug_of_war_age_data['Age'].min()
    max_age = tug_of_war_age_data['Age'].max()

    fig = px.histogram(
        tug_of_war_age_data, 
        x="Age",
        nbins=int(max_age - min_age + 1), # Setting the number of bins to the range of ages
        title="Age Distribution Among Athletes in Tug-Of-War",
        labels={'Age': 'Age of Athletes'}
)
    fig.update_layout(bargap = 0.2)
    fig.update_xaxes(dtick=1) # Setting the x-axis ticks to increment by 1 to show each age year

    fig = apply_universal_styles(fig)
    return fig

def create_cross_country_medals_per_country_diagram():
    # Making new dataframe only containing cross country skiers
    # Grouping by NOC and amount of medals
    cross_country_skiers = data_athletes[data_athletes["Sport"] == "Cross Country Skiing"]
    cross_country_medals = cross_country_skiers.groupby(["NOC", "Medal"]).size().unstack(fill_value=0).reset_index()

    # Sorting each NOC by total medals for nicer looking diagram
    cross_country_medals["Total Medals"] = cross_country_medals["Gold"] + cross_country_medals["Silver"] + cross_country_medals["Bronze"]
    cross_country_medals_sorted = cross_country_medals.sort_values(by='Total Medals', ascending=False)

    # Creating stacked bar diagram showing amount of cross country skiing medals for each country
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
    # Making new dataframe only containing cross country skiers
    cross_country_skiers = data_athletes[data_athletes["Sport"] == "Cross Country Skiing"]

    # Creating histogram showing cross country skiers ages
    fig = px.histogram(
        cross_country_skiers,
        x="Age",
        title="Age distribution of Cross Country Skiers",
        labels={'Age': 'Age of Athletes'}
    )
    fig.update_layout(bargap=0.2)

    fig = apply_universal_styles(fig)
    return fig