+++
url = "/2022/03/21/sudoku_solver2/"
title = "Sudoku Solver - Day 2"
date = "2022-03-21"
draft = false
tags = ["python","sudoku_solver"]
topics = ["coding"]
description = ""
+++

Today's work had some ups and downs for sure. Once again, if you want to follow along, you can see my code here: [@KendraPendolino/UnlinedSeashellMineral](https://replit.com/@KendraPendolino/UnlinedSeashellMineral). I started by adding basic elimination for cells in the same group as a solved cell. While there, I realized I had forgotten to put in a reference from the cell back to the grid, so I added that too.

```python
class Cell():
  ...
  def setGrid(self,grid):
    self.grid=grid
  def solve(self,value):
    self.val=value
    # Remove value from row, col, box
    for cell in self.grid.row(self.row) + self.grid.col(self.col) + self.grid.box(self.box):
      if type(cell.val)==list and value in cell.val:
        cell.val.remove(value)
```

I had to update the Grid init method accordingly.

```python
class Grid():
  def __init__(self,data=None):
    self.grid=[[Cell(i,j) for j in range(9)] for i in range(9)]
    for i in range(9):
      for j in range(9):
        self.grid[i][j].setGrid(self)
    ...
```

I built a quick little function to calculate a score for the grid - again, this is just a really quick check to see if the grid is making progress toward a solution. Full disclosure: at this stage, I made a goof. I was originally using "score" for both the method name and the attribute. Whoops! 

```python
class Grid():
  ...
  def calcScore(self):
    total=0
    for i in range(9):
      for j in range(9):
        if type(self.grid[i][j].val)==list:
          total+=len(self.grid[i][j].val)
    self.score=total
    print("Score: %d"%total)
  ...
```

Then I started putting in the basic solving methods. I set up methods for nakedSingles and hiddenSingles. I set up a method to process a single round of scanning the grid, and a method to handle solving via repeated rounds, including checking the sccore before and after and breaking if it's no longer making progress. 

Note that since naked singles apply to individual cells, I only need to call those once on each pass through the grid. Hidden singles and things I'll build later operate on the whole group, so we do those for each group.

```python
class Grid():
  ...
  def round(self):
    for i in range(9):
      nakedSingles(self.row(i))
      hiddenSingles(self.row(i))
    for j in range(9):
      hiddenSingles(self.col(j))
    for k in range(9):
      hiddenSingles(self.box(k))
  def solve(self):
    changed=True
    self.calcScore()
    while changed==True:
      before=self.score
      self.round()
      self.calcScore()
      if before==self.score: changed=False
    self.print()

def nakedSingles(group):
  # Checks for cells that have only one candidate remaining
  for cell in group:
    if type(cell.val)==list and len(cell.val)==1:
      cell.solve(cell.val[0])

def hiddenSingles(group):
  # Checks for cells that are the only place in their group which can hold a given value
  for n in range(1,10):
    count=0
    for cell in group:
      if type(cell.val)==list and n in cell.val:
        count+=1
    if count==1:
      for cell in group:
        if type(cell.val)==list and n in cell.val:
          cell.solve(n)
          break
```

Then I tried to put it all together, and I got worried. You see, I did a single round of solving, looked at the output, and noticed something alarming. I saw these scroll by:

```python
(2,7,2) []
...
(4,4,4) []
...
(6,3,7) []
```

Perhaps you've already figured out what the problem is - the grid is unsolvable. You can tell because these three cells have somehow ended up with an empty candidates list - there's no value that is allowed for that cell. So, the first question is: is my test grid flawed, or are my solving methods? I took a bet on my solving methods, and sure enough, there was a typo in the test grid. So next step was to correct the test grid. Here it is, with a 4 in the last row in place of the 5 I'd mistakenly entered.

```pyton
test = [
    [0,0,6,9,0,1,2,0,0],
    [0,2,0,3,0,4,0,7,0],
    [1,0,0,0,7,0,0,0,8],
    [4,6,0,0,0,0,0,2,5],
    [0,0,3,0,0,0,7,0,0],
    [7,9,0,0,0,0,0,6,4],
    [6,0,0,0,3,0,0,0,7],
    [0,4,0,2,0,9,0,8,0],
    [0,0,8,7,0,6,4,0,0]]
```

With that fixed, I moved on to testing the full solve method.

```
gr=Grid(test)
gr.solve()
```

And here's how that went:

```
Score: 149
Score: 5
Score: 0
Score: 0
576|981|243
829|364|571
134|572|698
---+---+---
461|897|325
283|645|719
795|123|864
---+---+---
612|438|957
347|259|186
958|716|432
```

Great success! It turns out this "very easy" grid was so simple it could be solved using only naked singles and hidden singles. So, up next time is finding a more difficult puzzle and adding code to check for naked pairs and hidden pairs. I hope to see you there!
