+++
url = "2022/04/02/creating_data_sets/"
title = "Creating Data Sets"
date = "2022-04-02"
tags = ["python"]
topics = ["coding","data science"]
description = "Simulated Data Sets for Coding Labs"
+++

We've all been there: you're digging around for a freely-available data set that's interesting, Goldilocks-sized, and has the right types of data fields to support your learning objectives. You're an hour or two deep in searching, and nothing you find seemes quite right. What's an instructional designer to do?

Well, if you're me, the answer seems obvious: create a simulated data set to use in your examples. I've done this in technical writing contexts as well, when I needed to use "patient data" in some examples but of course could not use data for _actual patients_. All you need is Python (maybe a Jupyter notebook, if you're feeling fancy), an idea of what your data set should look like, and a little creativity.

> **Important Disclaimer:** In this post, I discuss making up plausible-looking **sample data** for educational and illustrative purposes **only**. I want to stress that it is **highly unethical** to make up data in most circumstances. If you are preparing an analysis that has any kind of real world implications - on budgets, health, someone's understanding of reality, _anything_ - you are morally and ethically obligated to use real data in your work. Not fictional data, not fudged data: 100% true and correct data.

## Scenario 1: Patient Chart Data

The first time I needed to create a fake data set was to use in a set of examples to help visualize how different combinations of parameters would affect the list of medical charts selected for review. The most important features for my purposes were the **score gap** of each patient and the **expected score** of each chart.

To start, I looked at some real (de-identified) data and ran a few quick statistics to get an idea of what a realistic patient score gap distribution would look like. I found the mean and standard deviation and plugged these into NumPy's `random.normal(loc=mean, scale=sd)` method. I used this to generate random scores for each of 100 imaginary patients.

Up next, I needed possible values for expected score for charts for those patients. I needed up to 5 charts per patient. Each chart's expected score could be anything between 0 and the total _remaining_ score gap for the patient. So for each patient, I used NumPy's `random.random()` multiplied by the remaining score gap for the patient. For example, if the patient's total score gap was 8.81, the first chart's expected score was `8.81 * random.random()`. For the sake of the example, let's say the method returned 6.12 - now the patient has a remaining score gap of 2.69. The next chart would be `2.69 * random.random()`, and so on. At the end of this process, I would have a set of 5 "charts" for each patient that totaled their score gap _or less_, which is exactly what I needed.

From there, I was able to easily manipulate the data to identify which charts would be _included_ or _excluded_ based on various combinations of the parameters. I ended up exporting the data into another tool to make the final visualizations, but if you didn't need them in a specific format, you could absolutely use `matplotlib` to do so.

## Scenario 2: Chocolate Ratings

I was looking for a data set that was small, but not tiny, and something that would be generally appealing to think about (read: not the ever-present Covid data sets or anything that would make my learners think about their own mortality). I stumbled on a data set about chocolates, and I was really excited about it - but it just didn't have enough qualitative features for me to work with. So I decided to figure out exactly which qualitative features I wanted to see in the data set and just...make them up.

I settled on the following qualitative factors: Company, Country, Type. I assigned a weight to each of those factors - how much does this factor contribute to the overall rating? And then each individual value for those factors had its own numerical value. I would then take `weight * value * random.random()` for each factor and add them up to generate a rating for that particular type of chocolate. Using this approach produced a bit too much variability, so I threw together a quick function that would adjust a random number to be between _n_ and 1, e.g. if n=.5, I know that the minimum random value will be .5. This eliminated the wild variations, leaving a really nice distribution.

The finished data set included 15 companies (named after real companies, but with totally made up rating coefficients) from five countries, for three different types of chocolate (white, milk, dark) each. Last order of business was just to write this data to a CSV using `csv.DictWriter`. Et voila!

## Scenario 3: Designing for Linear Regression

Let's say that you're designing an exervise on linear regression. You may want to make sure that your data set lends itself well to analysis by linear regression. Let's see how you could make up a data set that will meet the assumptions of linear regression without looking too perfect.

Let's look at linear regression with a single independent variable first. Consider the basic linear equation:

`y = m*x + b`

Let's rework this a little bit:

`dependent_variable = slope * independent_variable + intercept`

So you have two main values to create: the slope and the intercept. The slope represents how much your dependent variable increases for each increase in independent variable. For example, how much more (or less) do you spend on gas for each 1 mile per gallon (mpg) increase in fuel efficiency? Or, how much longer does it take to write one additional page of a paper?

For the intercept, you'll want to pick something that makes sense as the value that your dependent variable has when your independent variable has a value of 0. For example, how much did students who didn't study at all (studied 0 hours) score on average? Or, what would a house with 0 square feet of habitable space cost? Note: In the real world, this value may seem a little nonsensical - it could be negative or represent a scenario that is impossible. You can pick this by plotting two realistic values, and drawing a line back to where it crosses the y-axis.

So now you've got a realistic (ish) slope and intercept. But you don't want your data to look too perfect, so I'd recommend using `random.random()` to add a little fuzz to your slope and intercept. So if you decided that your slope should be about 0.2, you can actually code your slope as `0.2 * (1 + .02 * (random.random() - 0.5))`. This code adjusts your slope value by a random value between +/- 1%.

> Let's take a closer look at that. The 0.2 is your target slope. The 1 is a 100% multiplier. The 0.02 scales the following term to be ~2% of the target value. Since `random.random()` returns a value between 0 and 1, subtracting 0.5 converts it to a value between -0.5 and 0.5 - combined with the 0.02 or 2% multiplier, this works out to an adjustment between -1% and 1%.

You can use this process to add a little fuzz to your intercept as well. Now, there's one last thing you'll need before you can generate your data: a normal distribution for your residuals. As a reminder, the residuals are the differences between the actual values and the values predicted by your model. Or, coming at this from the other direction: to generate a value, you'll plug your independent variable into your equation and get a dependent varaible value, and then add or subtract a normally distributed random value to _simulate_ a residual. You'll want to use 0 for the mean, but your standard deviation has some wiggle room. You can start with 1 and see how your residuals look - if your data looks too clean, increase the standard deviation and try again.

I put this all together in [a Jupyter notebook that you can check out here](https://mybinder.org/v2/gh/kpendolino/Binder/HEAD?labpath=CreatingDataSets.ipynb). Feel free to play with the parameters and see how they change the results.
