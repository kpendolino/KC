+++
title = "Pandas DataFrames"
date = "2022-04-02"
draft = true
tags = ["python","pandas"]
topics = ["coding","data science"]
description = "Getting to Know DataFrames in Pandas"
url = "2022/04/02/pandas_dataframes/"
+++

# Working with Pandas DataFrames

Pandas uses the DataFrame class for working with tabular data. DataFrames allow you to read, sort, manipulate, and display data. In this exercise, you'll create your first DataFrame and use it to do some initial exploration of a data set.

## Objectives

When you finish this lab, you should be comfortable with:

- Loading data into a DataFrame from a CSV file
- Printing out the first or last five rows
- Viewing DataFrame attributes like its columns and shape
- Accessing individual columns
- Manipulating the data set including sorting, ranking, grouping
- Adding new columns and populating them with generated data
- Changing the data type of a column
- Filtering data by column values using `loc` and numerical or qualitative values

We'll build on these further in the next lab.

## Resources

### Exercise Files

You can view this lab [as an interactive Jupyter notebook here](https://mybinder.org/v2/gh/kpendolino/PandasDataFrames/HEAD?labpath=PandasDataFrames.ipynb).

You can use right-click + "save link as" to download these files. You can also access them from GitHub at [kpendolino/PandasDataFrames](https://github.com/kpendolino/PandasDataFrames)

- Data Set: [chocdata.csv](/samples/PandasDataFrames/chocdata.csv)
- Starter Script: [start.py](/samples/PandasDataFrames/start.py)
- Full Expected Output: [full-output.txt](/samples/PandasDataFrames/full-output.txt)
- Finished Script (no peeking!) [finished.py](/samples/PandasDataFrames/finished.py)

### Pandas Documentation

- [pandas.read_csv()](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
- [DataFrame.head()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html)
- [DataFrame.tail()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.tail.html)
- [DataFrame.columns](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.columns.html)
- [DataFrame.shape](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shape.html)
- [DataFrame.sort_values()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html)
- [DataFrame.rank()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html)
- [DataFrame.astype()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html)
- [DataFrame.groupby()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html)
- [DataFrame.loc[]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html) <br/>Related Reading
    - [DataFrame.at[]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.at.html)
    - [DataFrame.iloc[]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html#pandas.DataFrame.iloc)
    - [DataFrame.iat[]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iat.html)
- [DataFrame.isin()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html)

## Setup

We've started you off with some basic setup, including importing `pandas` and defining some useful constants.

To create your DataFrame, you'll use `pd.read_csv(<filename>)`. This reads a CSV file and loads it into a DataFrame using the first row as column headers. To take a quick peek at your data, you can use `DataFrame.head()` to print out the first five rows or `DataFrame.tail()` to print out the last five. Take a look at this in action:

**Example**
```python
chips =  pd.read_csv('snackdata.csv')
print(chips.head())
print()
print(chips.tail())
```

**Output**
```
     Company     Flavor    Style  Rating
0  Old Dutch      Plain  Regular   6.307
1  Old Dutch      Plain   Kettle   5.887
2  Old Dutch      Plain   Canned   5.771
3  Old Dutch      Plain   Ridges   5.152
4  Old Dutch  Bar-B-Que  Regular   6.837

                Company                Flavor    Style  Rating
175  President's Choice       Salt and Pepper   Ridges   6.076
176  President's Choice  Sour Cream and Onion  Regular   4.734
177  President's Choice  Sour Cream and Onion   Kettle   6.014
178  President's Choice  Sour Cream and Onion   Canned   5.232
179  President's Choice  Sour Cream and Onion   Ridges   7.059
```

> Load the data from 'chocolate_data.csv' into pandas as a DataFrame called `chocolate`.

> Print the first five rows and the last five rows.

## Working With Columns

Pandas allows you to access column datas in several ways. First, you can use square brackets to access column data the same way you would use them to access dictionary data by key, for example, `df['Column Name']` returns the data in the _Column Name_ column. For simple column names, you can also access that data as an attribute, for example, `df.ColName` returns the data in the _ColName_ column.

**Example**
```python
print(chips[STYLE].head())
print()
print(chips.Flavor.tail())
```

**Output**
```
0    Regular
1     Kettle
2     Canned
3     Ridges
4    Regular
Name: Style, dtype: object

175         Salt and Pepper
176    Sour Cream and Onion
177    Sour Cream and Onion
178    Sour Cream and Onion
179    Sour Cream and Onion
Name: Flavor, dtype: object
```

> Print the first five values in the _Company_ column using square brackets.

> Print the last five values in the _Rating_ column by accessing it as an attribute.

## Accessing Multiple Columns

To access a subset of the DataFrame that includes multiple columns, you can use `df[[column1, column2, ...]].

**Example**
```python
print(chips[[COMPANY,STYLE,FLAVOR]].head())
```

**Output**
```
     Company    Style     Flavor
0  Old Dutch  Regular      Plain
1  Old Dutch   Kettle      Plain
2  Old Dutch   Canned      Plain
3  Old Dutch   Ridges      Plain
4  Old Dutch  Regular  Bar-B-Que
```

> Print the first five rows of `chocolate`, showing only the _Company_, _Country_, and _Type_ columns.

## DataFrame Attributes

DataFrames have several built-in attributes that you can use to view summary information. For example, you can view a list of columns in a DataFrame using `df.columns`. You can view the dimensions of the DataFrame - the number of rows and columns in it - using `df.shape`.

**Example**
```python
print(chips.columns)
print()
print(chips.shape)
```

**Output**
```
Index([u'Company', u'Flavor', u'Style', u'Rating'], dtype='object')

(180, 4)
```
> Print the list of columns in `chocolate`.

> Print the dimensions of `chocolate`.

## Manipulating Data

DataFrames have several methods that you can use to manipulate the data. For example, you can use `df.sort_values(<column(s)>, ascending=<direction(s)>)` to sort a DataFrame. You can use `df.rank(method=method, ascending=<boolean>)` to calculate ranks for each row. We'll use the _min_ ranking method; this means that records with the same value will all share the rank on the lower end of the tied range - if three records are tied for second place, they will all receive rank 2, and the next record will start at rank 5. These methods do not modify the DataFrame in place, but you can save the results as a new DataFrame or a new column in the DataFrame. To save results as a new column, use square brackets - just as you would to add a new element to a dictionary.

**Example**
```python
# Sort the rows by Rating, then print the best five
print(chips.sort_values(RATING,ascending=False).head())
print()

# Calculate overall rankings
chips[OVERALLRANK]=chips[RATING].rank(method="min",ascending=False)

print(chips[[COMPANY,STYLE,FLAVOR,OVERALLRANK]].head())
```

**Output**
```
              Company                Flavor   Style  Rating
94           Cape Cod  Sour Cream and Onion  Kettle   9.525
24             Kettle  Sour Cream and Onion  Kettle   9.455
17          Old Dutch  Sour Cream and Onion  Kettle   9.415
23             Kettle       Salt and Pepper  Kettle   9.343
159  Jay's of Chicago  Sour Cream and Onion  Ridges   8.874

     Company    Style     Flavor  Overall Rank
0  Old Dutch  Regular      Plain          74.0
1  Old Dutch   Kettle      Plain         105.0
2  Old Dutch   Canned      Plain         116.0
3  Old Dutch   Ridges      Plain         143.0
4  Old Dutch  Regular  Bar-B-Que          51.0
```

> Print the first five rows of `chocolate` after sorting by _Rating_, descending.

> Add a new column to `chocolate` using the `OVERALLRANK` constant as the label. Populate it with the rank of each record by _Rating_, descending. Use the "min" ranking method.

> Print the first five rows of `chocolate`, showing only _Company_, _Country_, _Type_, and _Rating_.

## Modifying Data Types

You can use `df[column].astype(type)` to cast the values in a column to another data type. For example, you can use this to change integers into floats or strings.

**Example**
```python
chips[INTRATING]=chips[RATING].astype(int)
print(chips[[COMPANY,STYLE,RATING,INTRATING]].head())
```

**Output**
```
     Company    Style  Rating  Integer Rating
0  Old Dutch  Regular   6.307               6
1  Old Dutch   Kettle   5.887               5
2  Old Dutch   Canned   5.771               5
3  Old Dutch   Ridges   5.152               5
4  Old Dutch  Regular   6.837               6
```

> Add a new column to `chocolate` using the `INTRATING` constant as the column label. Populate the column with values from `RATING`, cast as integers.

> Print the _Company_, _Type_, `RATING`, and `INTRATING` values for the first five records.


## Grouping Data

You can use `df.groupby(column(s))` to access the data grouped by the indicated column. This can be handy for manipulating sub-sets of the data, such as to calculate ranks or statistics by groups.

**Example**
```python
# Calculate ranks within each Style
chips[STYLERANK]=chips.groupby(STYLE)[RATING].rank(method="min",ascending=False)
print(chips[[STYLE,RATING,OVERALLRANK,STYLERANK]].head())
print()

# Cast ranks as integers
chips[STYLERANK]=chips[STYLERANK].astype(int)
print(chips[[STYLE,RATING,OVERALLRANK,STYLERANK]].head())
```

**Output**
```
     Style  Rating  Overall Rank  Rank In Style
0  Regular   6.307          74.0            7.0
1   Kettle   5.887         105.0           37.0
2   Canned   5.771         116.0           27.0
3   Ridges   5.152         143.0           37.0
4  Regular   6.837          51.0            4.0

     Style  Rating  Overall Rank  Rank In Style
0  Regular   6.307          74.0              7
1   Kettle   5.887         105.0             37
2   Canned   5.771         116.0             27
3   Ridges   5.152         143.0             37
4  Regular   6.837          51.0              4
```

> Calculate ranks for chocolates within each _Country_ using the "min" ranking method in descending order. Save them as a new column on `chocolate` using the `COUNTRYRANK` constant as a label.

> Print out the top five records, showing the _Country_, _Type_, `RATING`, `OVERALLLRATING`, and `COUNTRYRANK`.

> Save the ranks as integers.

> Print out the top five records again, showing the _Country_, _Type_, `RATING`, `OVERALLLRATING`, and `COUNTRYRANK`.

## Filtering Columns

You can view data at a specific _location_ using the `df.loc()` method. The location identifier can be a simple column label or row index, a combination for labels and indices, or even logical operators on column labels or row values.

**Example**
```python
tenbest=chips.loc[chips[OVERALLRANK] <= 10].sort_values(RATING,ascending=False)
print(tenbest[[COMPANY,FLAVOR,STYLE,RATING,OVERALLRANK]])
print()


bestinstyle=chips.loc[chips[STYLERANK] == 1].sort_values(RATING,ascending=False)
print(bestinstyle[[STYLE,COMPANY,FLAVOR,RATING,OVERALLRANK,STYLERANK]])

```

**Output**
```
              Company                Flavor   Style  Rating  Overall Rank
94           Cape Cod  Sour Cream and Onion  Kettle   9.525           1.0
24             Kettle  Sour Cream and Onion  Kettle   9.455           2.0
17          Old Dutch  Sour Cream and Onion  Kettle   9.415           3.0
23             Kettle       Salt and Pepper  Kettle   9.343           4.0
159  Jay's of Chicago  Sour Cream and Onion  Ridges   8.874           5.0
11          Old Dutch      Salt and Vinegar  Ridges   8.754           6.0
130            Zapp's      Salt and Vinegar  Canned   8.725           7.0
13          Old Dutch       Salt and Pepper  Kettle   8.686           8.0
150  Jay's of Chicago      Salt and Vinegar  Canned   8.440           9.0
22             Kettle      Salt and Vinegar  Kettle   8.340          10.0

       Style           Company  ... Overall Rank  Rank In Style
94    Kettle          Cape Cod  ...          1.0              1
159   Ridges  Jay's of Chicago  ...          5.0              1
130   Canned            Zapp's  ...          7.0              1
144  Regular  Jay's of Chicago  ...         39.0              1
```

> Create a new DataFrame called `tenbest` that contains only the ten highest-rated chocolate bars in `chocolate`. Print out only the _Company_, _Country_, _Type_, _Rating_, and `OVERALLRANK` values for `tenbest`.

> Create a new DataFrame called `bestincountry` that contains only the highest rated chocolate bar from each _Country_. Print out only the _Company_, _Country_, _Type_, _Rating_, _Overall Rank_, and `COUNTRYRANK` values for `bestincountry`.

## Filtering Columns, Continued

You can also use `df.isin(values)` to filter a DataFrame to only records that include values in the provided list. Usually, you'll use this with a subset of the full DataFrame _within_ a call to `df.loc[]`. For example, `df.loc[chips.Style.isin(["Kettle","Ridges","Canned"])]` will return only records from `chips` where the _Style_ column contains either "Kettle", "Ridges", or "Canned".

**Example**
```python
# Get the 5 best-ranked Kettle and Ridges chips across all companies and flavors
crunch=chips.loc[chips[STYLE].isin(["Kettle","Ridges"]) &
     (chips[STYLERANK]<=5)].sort_values([STYLE,RATING],ascending=[True,False])
print(crunch[[STYLE,COMPANY,FLAVOR,STYLERANK]])
```

**Output**
```
      Style           Company                Flavor  Rank In Style
94   Kettle          Cape Cod  Sour Cream and Onion              1
24   Kettle            Kettle  Sour Cream and Onion              2
17   Kettle         Old Dutch  Sour Cream and Onion              3
23   Kettle            Kettle       Salt and Pepper              4
13   Kettle         Old Dutch       Salt and Pepper              5
159  Ridges  Jay's of Chicago  Sour Cream and Onion              1
11   Ridges         Old Dutch      Salt and Vinegar              2
111  Ridges       Better Made      Salt and Vinegar              3
15   Ridges         Old Dutch       Salt and Pepper              4
61   Ridges              Lays      Salt and Vinegar              5
```

> Create a new DataFrame called `usa_uk` that includes only chocolate bars made in "America" or "United Kingdom" that are in the top 5 best chocolate bars from their country.

> Sort the values by _Country_, ascending, then by _Rating_, descending.

> Print `usa_uk`, showing only the _Type_, _Company_, _Country_, and `COUNTRYRANK`.

## The Big Picture

You've now explored the basics of creating and manipulating DataFrames in Pandas. You can pair DataFrames with standard python methods that act on lists to take them even further. Take a few minutes to think through what kinds of insights these tools can provide.

> Which country has the most chocolate bars in the top ten overall?

> Which company has the greatest range in the ratings of their bars? Which company is the most consistently rated?

> What do you think the rating scale used in this data set was?

Congratulations on completing this lab exercise!

* * *

&copy; 2022 Kendra Pendolino