##### Working with Pandas DataFrames #####

## Setup ##

import pandas as pd

# You can use these constants to refer to columns in the DataFrame.
COMPANY="Company"
COUNTRY="Country"
RATING="Rating"
RATERS="Raters"
TYPE="Type"

OVERALLRANK="Overall Rank"
COUNTRYRANK="Rank In Country"
INTRATING="Integer Rating"



## Load the DataFrame ##

# Load the data from 'chocolate_data.csv' into pandas as a DataFrame called `chocolate`.
chocolate =  pd.read_csv('chocdata.csv')


# Print the first five rows.
print(chocolate.head())

print("")

# Print the last five rows.
print(chocolate.tail())

print("")


## Working With Columns ##

# Print the first five values in the _Company_ column using square brackets.
print(chocolate[COMPANY].head())

print("")

# Print the last five values in the _Rating_ column by accessing it as an attribute.
print(chocolate.Rating.tail())

print("")



## Accessing Multiple Columns ##

# Print the first five rows of `chocolate`, showing only the _Company_, _Country_, and _Type_ columns.
print(chocolate[[COMPANY,COUNTRY,TYPE]].head())

print("")



## DataFrame Attributes ##

# Print the list of columns in `chocolate`.
print(chocolate.columns)

print("")

# Print the dimensions of `chocolate`.
print(chocolate.shape)

print("")




## Manipulating Data ##

# Print the first five rows of `chocolate` after sorting by _Rating_, descending.
print(chocolate.sort_values(RATING,ascending=False).head())

print("")

# Add a new column to `chocolate` using the `OVERALLRANK` constant as the label. Populate it with the rank of each record by _Rating_, descending. Use the "min" ranking method.
chocolate[OVERALLRANK]=chocolate[RATING].rank(method="min",ascending=False)

# Print the first five rows of `chocolate`, showing only _Company_, _Country_, _Type_, and _Rating_.
print(chocolate[[COMPANY,COUNTRY,TYPE,RATING]].head())

print("")



## Modifying Data Types ##

# Add a new column to `chocolate` using the `INTRATING` constant as the column label. Populate the column with values from `RATING`, cast as integers.
chocolate[INTRATING]=chocolate[RATING].astype(int)

# Print the _Company_, _Type_, `RATING`, and `INTRATING` values for the first five records.
print(chocolate[[COMPANY,TYPE,RATING,INTRATING]].head())

print("")



## Grouping Data ##

# Calculate ranks for chocolates within each _Country_ using the "min" ranking method in descending order. Save them as a new column on `chocolate` using the `COUNTRYRANK` constant as a label.
chocolate[COUNTRYRANK]=chocolate.groupby(COUNTRY)[RATING].rank(method="min",ascending=False)

# Print out the top five records, showing the _Country_, _Type_, `RATING`, `OVERALLLRATING`, and `COUNTRYRANK`.
print(chocolate[[COUNTRY,TYPE,RATING,OVERALLRANK,COUNTRYRANK]].head())

print("")

# Save the ranks as integers.
chocolate[COUNTRYRANK]=chocolate[COUNTRYRANK].astype(int)

# Print out the top five records again, showing the _Country_, _Type_, `RATING`, `OVERALLLRATING`, and `COUNTRYRANK`.
print(chocolate[[COUNTRY,TYPE,RATING,OVERALLRANK,COUNTRYRANK]].head())

print("")



## Filtering Columns ##

# Create a new DataFrame called `tenbest` that contains only the ten highest-rated chocolate bars in `chocolate`. 
tenbest=chocolate.loc[chocolate[OVERALLRANK] <= 10].sort_values(RATING,ascending=False)

#Print out only the _Company_, _Country_, _Type_, _Rating_, and `OVERALLRANK` values for `tenbest`.
print(chocolate[[COMPANY,COUNTRY,TYPE,RATING,OVERALLRANK]])

print("")

# Create a new DataFrame called `bestincountry` that contains only the highest rated chocolate bar from each _Country_. 

bestincountry=chocolate.loc[chocolate[COUNTRYRANK] == 1].sort_values(RATING,ascending=False)

#Print out only the _Company_, _Country_, _Type_, _Rating_, _Overall Rank_, and `COUNTRYRANK` values for `bestincountry`.
print(bestincountry[[COMPANY,COUNTRY,TYPE,RATING,OVERALLRANK,COUNTRYRANK]])

print("")



## Filtering Columns, Continued ##

# Create a new DataFrame called `usa_uk` that includes only chocolate bars made in "America" or "United Kingdom" that are in the top 5 best chocolate bars from their country. Sort the values by _Country_, ascending, then by _Rating_, descending.
usa_uk=chocolate.loc[chocolate[COUNTRY].isin(["America","United Kingdom"]) &
     (chocolate[COUNTRYRANK]<=5)].sort_values([COUNTRY,RATING],ascending=[True,False])

# Print `usa_uk`, showing only the _Type_, _Company_, _Country_, and `COUNTRYRANK`.
print(usa_uk[[TYPE,COMPANY,COUNTRY,COUNTRYRANK]])

print("")



## The Big Picture ##

# Which country has the most chocolate bars in the top ten overall?



# Which company has the greatest range in the ratings of their bars? Which company is the most consistently rated?



# What do you think the rating scale used in this data set was?




## Congratulations on completing this lab exercise! ##