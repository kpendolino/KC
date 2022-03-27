+++
url = "/2022/03/19/sudoku_solver0/"
title = "Sudoku Solver - Day 0"
date = "2022-03-19"
draft = false
tags = ["python","sudoku_solver"]
topics = ["coding"]
description = ""
+++

I got the idea for this project from [Project Euler](https://projecteuler.net/). If you're someone who likes tinkering with code and algorithms, I highly recommend checking out Project Euler to add a little something extra to your personal and professional development.

Anyway, here's the project: I want to create a sudoku-solving algorithm. That's it, really. It's nothing particularly groundbreaking, but I want to do it for myself and capture my thought process along the way.

A quick note: throughout this series, I'll use the word “group” to refer to any set of sells that can't contain repeated digets, i.e. a row, column, or 3x3 box.

In this first post, I'm just going to do some basic planning and scheming. Then the fun begins!

## Ground Rules

I'll be following two basic guidelines: **no peeking** and **keep it simple**. I won't be looking at any other sudoku algorithms. I don't want to know how other have structured their data or approached the process. On the other hand, I also don't want this project to grow too complicated, so I plan to limit the complexity to handle puzzles that can be solved without advanced sudoku methods. Naked and hidden pairs and triples? Sure, I'd love to incorporate those in my algorithm. Swordfish, sashimi, x-wings? That's probably a little too extra for this little project.

I'll be fitting this in around ::gestures vaguely:: my day job and life in general, so I'll be working in stages, probably just an hour or two at a time. I'll try to capture all the highs and lows - all the breakthroughs and all the silly mistakes.

# The Scheming Begins

## Input

I'm just going to type in random puzzles I find in my house. To keep it simple, everything will come in two-dimensional array - a list of lists. The outer list has a list for each row in the grid. Each inner list has an integer for each cell in the grid: 0 for blank cells and 1-9 for filled cells.

## Structure

I think I'm going to use a few classes to control the data. Grid, Row, Col, Cell, Box - these will let me access cells that “see” each other and easily use them in the algorithm. Each cell will hold either an integer or a list of values. If the cell is solved, it'll just be an integer. If the cell is not yet solved, it'll be a list of the candidates for that cell.

## Setup Methods

For starters, I'll need methods to set up the grid with the given values. This includes populating the cells and updating the cells’ neighbors to remove that value as a candidate. For example, if the cell at 0,0 is a 5, no other cell in row 0, col 0, or box 0 can contain 5.

## Solving Methods

Next, I'll need methods to figure out the “next steps” based on the current grid state:

- Naked singles (cells) - this will look for cells that have a candidates list with a length of one. This means there's no other value that can be placed there, so the cell can be solved.
- Hidden singles (groups) - this will look for cells which are the only place in their groups that can hold a certain value. These cells can be solved.
- Naked pairs (groups) - this will look for pairs of cells in the same group that have the same 2-number candidate list. These cells must contain those two values, so no other cell in that same group can contain those two values.
- Hidden pairs (groups) - this will look for pairs of cells in the same group that are the only cells in that group that can contain those two values. These cells must contain those two values, so all other candidates can be removed.

## Other Considerations

- Score - after each round of moves, I'll calculate some kind of score based on the current state of the grid. Maybe a sum of the lengths of all candidate lists or something like that. The purpose of this is to allow me to stop looping if my solving methods aren't going to cut it - I don't want my algorithm to endlessly search under the same stones. If a full round of processing completes and the score hasn't changed, I've reached a dead end.
- Scoring++ - I may go a little extra and calculate the score on a per-group basis as well. This will let me ignore groups that haven't changed in the last round to avoid meaningless re-processing. This may be a later addition, as it would just improve efficiency, not change the outcome.
- Output - I'll set up a print function that can show me what the grid looks like at any given state. This will allow me to print the completed solution, and will also support debugging. I may also need an easy-to-read output of the state of the candidate lists for debugging or to identify additional solving methods I need to implement.

Well, I think that's the gist of it. Next time I've got a chunk of time, I'll start putting this together and post the next installment. I hope you've enjoyed this glimpse at my thought process - see y'all soon!
