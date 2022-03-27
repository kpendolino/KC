+++
url = "/2022/03/24/sudoku_solver5/"
title = "Sudoku Solver - Day 5"
date = "2022-03-24"
draft = false
tags = ["python","coding"]
topics = ["sudoku_solver"]
description = ""
+++

Looks like this project is done! I plugged the semi-solved Grid 42 into a sudoku app to check for the next step, and immediately saw it: locked intersections. This happens when all of the candidates for a given digit in a box appear in the interesction of that box and a row/column or vice versa. If every cell that could contain a 1 in box 0 is in row 0, you know that the digit 1 *can't* appear anywhere else in row 0.

Here's what my code for that looks like:

```python
def lockedIntersections(grid):
  for d in range(1,10):
    for ij in range(9): # Iterate over columns/rows
      row=[cell for cell in grid.row(ij) if type(cell.val)==list and d in cell.val]
      col=[cell for cell in grid.col(ij) if type(cell.val)==list and d in cell.val]
      rowbox=[cell.box for cell in row]
      colbox=[cell.box for cell in col]
      if len(set(rowbox))==1:
        #they're locked
        for cell in grid.box(rowbox[0]):
          if cell.row!=ij:
            if type(cell.val)==list and d in cell.val: cell.remove(d)
      if len(set(colbox))==1:
        #they're locked
        #print("Locked cells in col %d, box %d"%(ij,colbox[0]))
        for cell in grid.box(colbox[0]):
          if cell.col!=ij:
            if type(cell.val)==list and d in cell.val: cell.remove(d)
    for k in range(9): # Iterate over boxes
      pos=[cell for cell in grid.box(k) if type(cell.val)==list and d in cell.val]
      rows=[cell.row for cell in pos]
      #print(k,rows)
      if len(set(rows))==1:
        #they're locked
        #print("Locked cells in row %d, box %d"%(rows[0],k))
        for cell in grid.row(rows[0]):
          if cell.box!=k:
            if type(cell.val)==list and d in cell.val: cell.remove(d)
      cols=[cell.col for cell in pos]
      if len(set(cols))==1:
        #they're locked
        #print("Locked cells in col %d, box %d"%(cols[0],k))
        for cell in grid.col(cols[0]):
          if cell.box!=k:
            if type(cell.val)==list and d in cell.val: cell.remove(d)
```

This took a little bit of troubleshooting because on my first attempt, I had the eliminations flipped. But with this code working, check it out:

```
Grid 42
384|567|921
126|439|785
759|821|346
---+---+---
563|798|214
847|312|659
912|645|873
---+---+---
231|974|568
495|286|137
678|153|492
Score: 0
Sum: 405
```

And just like that - for the first time ever - I had working code that could solve all 50 puzzles from Project Euler Problem 96. The only step left to solving the problem is to add up the 3-digit number in the top left of each grid (e.g. `384` in the grid above) for all 50 grids. I won't spoil that here, but boy did it feel good to see that great big green checkmark!
