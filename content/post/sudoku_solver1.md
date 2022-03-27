+++
url = "/2022/03/20/sudoku_solver1/"
title = "Sudoku Solver - Day 1"
date = "2022-03-20"
draft = false
tags = ["python","coding"]
topics = ["sudoku_solver"]
description = ""
+++

I wasn't able to get as much done today as I'd hoped, but I did get started with it. I'm doing my coding using Replit.com; you can see my code here: [@KendraPendolino/UnlinedSeashellMineral](https://replit.com/@KendraPendolino/UnlinedSeashellMineral). So, let's see what we have so far.


I found a very easy sudoku puzzle to start with. Here it is as a two-dimensional array.

```python
test = [
	[0,0,6,9,0,1,2,0,0],
	[0,2,0,3,0,4,0,7,0],
	[1,0,0,0,7,0,0,0,8],
	[4,6,0,0,0,0,0,2,5],
	[0,0,3,0,0,0,7,0,0],
	[7,9,0,0,0,0,0,6,4],
	[6,0,0,0,3,0,0,0,7],
	[0,4,0,2,0,9,0,8,0],
	[0,0,8,7,0,6,5,0,0]]
```

I made some game-day changes to the setup. For starters, I nixed the separate Row, Col, and Box classes in favor of row, col, and box methods on the Grid class. Note that I've made the decision to use i, j, and k as the indices of the rows, columns, and boxes, respectively. I will be trying my darndest to resist the urge to use i, j, and k as general iterators anywhere in my code. Here's what the Grid class includes so far:

- &#95;&#95;init&#95;&#95; method - this sets up a blank grid of Cell objects. If you pass in a list of lists, it'll populate the grid with the given values. I haven't yet added any kind of validation here - it doesn't check to make sure that you're giving it a 9x9 array, it just assumes that if you've given it any data, that it's the right kind of data.
- row, col, and box methods - these return a list of all cells in the indicated group
- print method - this prints out the grid, showing only solved values. Unsolved cells are marked by a 0. I use pipes (&#124;), dashes (-), and plus signs (+) to separate the boxes for clarity.

```python
class Grid():
  def __init__(self,data=None):
    self.grid=[[Cell(i,j) for j in range(9)] for i in range(9)]
    if data:
      for i in range(9):
	for j in range(9):
	  if data[i][j]>0:
	    self.grid[i][j].solve(data[i][j])
  def row(self,i):
    return [self.grid[i][j] for j in range(9)]
  def col(self,j):
    return [self.grid[i][j] for i in range(9)]
  def box(self,k):
    return [self.grid[i][j] for i in range(9) for j in range(9) if self.grid[i][j].box==k]
  def print(self):
    for i in range(9):
      str=""
      for j in range(9):
	if type(self.grid[i][j].val)==int:
	  str+="%d"%self.grid[i][j].val
	else:
	  str+="0"
	if j==2 or j==5:
	  str+="|"
      print(str)
      if i==2 or i==5:
	print("---+---+---")
```

The Cell class is pretty straightforward. Here's what I have so far:
- &#95;&#95;init&#95;&#95; method - Takes row and col indices (i,j) and calculates the box index (k). Then it populates self.val with a list of all digits from 1 to 9 - this is the raw candidate set that we'll work from.
- &#95;&#95;str&#95;&#95; method - This tells my Cell objects what they should look like if a method tries to get a string value for them. In this case, I'm printing out the i, j, and k indices as a tuple, then printing out the value or candidate list.
- solve method: This does what it says on the tin. You've figured out what value goes in this cell, so this replaces the candidate list with that value. I've got a TODO for building out logic to go through that cell's groups and remove this value from their candidate lists.

```python
class Cell():
  def __init__(self,i,j):
    self.row=i
    self.col=j
    self.box=3*(i//3)+j//3
    self.val=[n for n in range(1,10)]
  def __str__(self):
    return "(%d,%d,%d) %s"%(self.row,self.col,self.box,self.val)
  def solve(self,value):
    self.val=value
    #TODO: remove value from row, col, box
```

The rest is some testing stuff. I initialize a grid using the test data, print out each cell one by one, double check that the box indices are working as expected, and test the print() function.

```python
gr=Grid(test)
for i in range(9):
  for j in range(9):
    print(gr.grid[i][j])

for l in range(9):
  print(gr.box(0)[l])

gr.print()
```

I hope you've enjoyed following along with me so far. On the next installment, I'm hoping to get through the basic solving algorithms - eliminating values in the same group, and then scanning for single or naked values, pairs, and maybe even triples.
