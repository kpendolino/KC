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


# Print the first five rows.


print("")

# Print the last five rows.


print("")


## Working With Columns ##

# Print the first five values in the _Company_ column using square brackets.


print("")

# Print the last five values in the _Rating_ column by accessing it as an attribute.


print("")



## Accessing Multiple Columns ##

# Print the first five rows of `chocolate`, showing only the _Company_, _Country_, and _Type_ columns.


print("")



## DataFrame Attributes ##

# Print the list of columns in `chocolate`.


print("")

# Print the dimensions of `chocolate`.


print("")




## Manipulating Data ##

# Print the first five rows of `chocolate` after sorting by _Rating_, descending.


print("")

# Add a new column to `chocolate` using the `OVERALLRANK` constant as the label. Populate it with the rank of each record by _Rating_, descending. Use the "min" ranking method.


# Print the first five rows of `chocolate`, showing only _Company_, _Country_, _Type_, and _Rating_.


print("")



## Modifying Data Types ##

# Add a new column to `chocolate` using the `INTRATING` constant as the column label. Populate the column with values from `RATING`, cast as integers.


# Print the _Company_, _Type_, `RATING`, and `INTRATING` values for the first five records.


print("")



## Grouping Data ##

# Calculate ranks for chocolates within each _Country_ using the "min" ranking method in descending order. Save them as a new column on `chocolate` using the `COUNTRYRANK` constant as a label.


# Print out the top five records, showing the _Country_, _Type_, `RATING`, `OVERALLLRATING`, and `COUNTRYRANK`.


print("")

# Save the ranks as integers.


# Print out the top five records again, showing the _Country_, _Type_, `RATING`, `OVERALLLRATING`, and `COUNTRYRANK`.


print("")



## Filtering Columns ##

# Create a new DataFrame called `tenbest` that contains only the ten highest-rated chocolate bars in `chocolate`. 


#Print out only the _Company_, _Country_, _Type_, _Rating_, and `OVERALLRANK` values for `tenbest`.


print("")

# Create a new DataFrame called `bestincountry` that contains only the highest rated chocolate bar from each _Country_. 


#Print out only the _Company_, _Country_, _Type_, _Rating_, _Overall Rank_, and `COUNTRYRANK` values for `bestincountry`.


print("")



## Filtering Columns, Continued ##

# Create a new DataFrame called `usa_uk` that includes only chocolate bars made in "America" or "United Kingdom" that are in the top 5 best chocolate bars from their country. Sort the values by _Country_, ascending, then by _Rating_, descending.



# Print `usa_uk`, showing only the _Type_, _Company_, _Country_, and `COUNTRYRANK`.


print("")



## The Big Picture ##

# Which country has the most chocolate bars in the top ten overall?



# Which company has the greatest range in the ratings of their bars? Which company is the most consistently rated?



# What do you think the rating scale used in this data set was?




## Congratulations on completing this lab exercise! ##