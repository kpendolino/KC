+++
url = "/2022/03/23/sudoku_solver4/"
title = "Sudoku Solver - Day 4"
date = "2022-03-23"
draft = false
tags = ["python","coding"]
topics = ["sudoku_solver"]
description = ""
+++

WELL turns out I had a glitch in my code. Let's recap where the last installment left off. My algorithm thought that this was fully solved:

```
829|31 |475
5 7|489|123
1 4|275|689
---+---+---
2 3|64 |9 7
461|927|538
97 |138|246
---+---+---
713|852|694
 92|764|851
648|3  |7 2
```

So, that's a miss. I went back through my code to identify the issue and discovered that there was a bug in my hiddenPairs code. Take a look and see if you can spot it:

```python
# Original Code
def hiddenPairs(group):
  unsolved=[n for n in range(1,10) if not n in [cell.val for cell in group if type(cell.val)==int]]
  duos=[n for n in unsolved if len([cell for cell in group if type(cell.val)==list and n in cell.val])==2]
  if len(duos)<2: 
    # There can't be a hidden pair if there aren't two different values that appear exactly twice
    return
  # Now check to see if the same two values appear in the same two cells
  for a in range(len(duos)-1):
    pairA=[cell for cell in group if type(cell.val)==list and duos[a] in cell.val]
    for b in range(1,len(duos)):
      pairB=[cell for cell in group if type(cell.val)==list and duos[b] in cell.val]
      if pairA==pairB: 
        # This is it, folks!
        for cell in pairA:
          # Only need to do this once
          cell.val=[duos[a],duos[b]]
      else: 
        continue
```

Do you see it? No? Let me zoom in.

```python
# Original Code
def hiddenPairs(group):
  ...
  for a in range(len(duos)-1):
    ...
    for b in range(1,len(duos)):
      ...
```

Oofta. That `for b in range(1,len(duos))` was supposed to say `for b in range(a+1,len(duos))`. I wish I could say that I spotted that typo easily, but I very much did not. I had to add a lot of extra print statements to support debugging, and eventually discovered that instead of setting the candidates list for a hidden pair to something like `[1,6]`, it was setting them to things like `[6,6]`. Here's the corrected code: 

```python
def hiddenPairs(group):
  #print("HIDDEN PAIRS")
  unsolved=[n for n in range(1,10) if not n in [cell.val for cell in group if type(cell.val)==int]]
  #print("unsolved: ", unsolved)
  duos=[n for n in unsolved if len([cell for cell in group if type(cell.val)==list and n in cell.val])==2]
  #print("duos: ",duos)
  if len(duos)<2: 
    # There can't be a hidden pair if there aren't two different values that appear exactly twice
    return
  # Now check to see if the same two values appear in the same two cells
  for a in range(len(duos)-1):
    pairA=[cell for cell in group if type(cell.val)==list and duos[a] in cell.val]
    assert len(pairA)==2, "%s should be a list of length 2"%pairA
    for b in range(a+1,len(duos)):
      pairB=[cell for cell in group if type(cell.val)==list and duos[b] in cell.val]
      if pairA==pairB: 
        # This is it, folks!
        #print("hiddenPairs is doing something!")
        #for cell in group: 
        #  if type(cell.val)==list: print(cell)
        #print("unsolved: %s"%unsolved)
        #print("duos: %s"%duos)
        #print("cells: %s and %s"%(pairA[0],pairA[1]))
        #print("values: %d, %d"%(duos[a],duos[b]))
        for cell in pairA:
          if len(cell.val)==2: continue
          # Only need to do this once
          #print(cell)
          cell.val=[duos[a],duos[b]]
          #print(cell)
      else: 
        continue
```

You can see a LOT of extra print statements that I commented out once I was done debugging. I was really puzzled for a while. While debugging, I added a "sum" function to the Grid class to calculate the sum of solved cells - a full sudoku grid adds to 405, so if my count is less than 405, it's not solved. Anyway, now that's sorted out, I can go ahead and run that "hard" difficulty grid through again and get...

```python
hard = [
  [0,0,9,0,0,0,4,0,0],
  [0,0,7,0,8,0,1,0,0],
  [1,0,0,2,0,5,0,0,9],
  [2,0,0,0,4,0,0,0,7],
  [0,6,0,9,0,7,0,3,0],
  [9,0,0,0,3,0,0,0,6],
  [7,0,0,8,0,2,0,0,4],
  [0,0,2,0,6,0,8,0,0],
  [0,0,8,0,0,0,7,0,0]]

Grid(hard).solve()
```

```
  9| 1 |47 
  7|489|1  
1  |275|  9
---+---+---
2  | 4 |9 7
 6 |927|53 
97 | 38|246
---+---+---
7  |8 2|  4
  2|76 |8  
  8|   |7  
Score: 116
Sum: 226
```

Ok so like, halfway solved? I guess these basic algorithms weren't enough to get through a "hard" difficulty puzzle. That's a shame, because I was considering running this algorithm against [Project Euler problem # 96](https://projecteuler.net/problem=96), which I've never successfully solved. So I guess it's time to build a bit more complexity.

# X-Wings Are Go

The next strategy that I think will help get this grid solved is called an X-wing. (I know, I know, I said that was "too extra" - I was wrong!). Here's the basic idea: let's say in row 0, you have the digit 1 confined to columns 2 and 4. In row 3, digit 1 is also confined to columns 2 and 4. That means that in those two rows, there are only two possibilities for digit 1 - columns 2 and 4. *So we have narrowed down digit 1 in columns 2 and 4 - it **must** be in row 0 or 3.* This lets us eliminate 1 as a possibility from every other cell in those columns.

Let's take a look at that as a visual. In the grid below, ? represents the "X-wing" of cells that must contain a certain digit as a candidate. Assuming those two rows don't contain any other cells that could contain this digit, each cell marked X can have this digit eliminated as a possibility

```
  ?| ? |   
  X| X |   
  X| X |   
---+---+---
  ?| ? |   
  X| X |   
  X| X |   
---+---+---
  X| X |   
  X| X |   
  X| X |   
```

So, time to write this as an algorithm. This one is a first for us because it looks at the grid as a whole rather than operating on individual groups. Here's the first draft:

```python
def xWings(grid):
  for d in range(1,10):
    # By Rows
    rows=[i for i in range(9) if len([cell for cell in grid.row(i) if type(cell.val)==list and d in cell.val])==2]
    # By Cols
    cols=[i for i in range(9) if len([cell for cell in grid.col(i) if type(cell.val)==list and d in cell.val])==2]

    if len(rows)>=2: # Check for locked columns in 2 rows
      pos={}
      for row in rows:
        pos[row]=[cell.col for cell in grid.row(row) if type(cell.val)==list and d in cell.val]
      for a in range(len(rows)-1):
        for b in range(a+1,len(rows)):
          if pos[rows[a]]==pos[rows[b]]:
            lockedrows=[rows[a],rows[b]]
            lockedcols=pos[rows[a]]
            #print("digit %d is locked in columns %s in rows %s" %(d,lockedcols,lockedrows))
            for col in lockedcols:
              for cell in grid.col(col):
                if cell.row not in lockedrows:
                  if type(cell.val)==list and d in cell.val: cell.remove(d)
    #TODO - check for locked rows in 2 cols
```

I got this chunk of code working the way I expected with a little trial and error and ran it against that same "hard" grid. Along the way, I identified a piece of the algorithm I wanted to refactor - I want to add a remove method on the Cell class so that when I remove a candidate from the cell, if there's only one candidate left, it goes ahead and solves that cell. You can see that I've used it above: `cell.remove(d)` instead of `cell.val.remove(d)`. Here's what that method looks like:

```python
class Cell():
  ...
  def remove(self,cand):
    assert type(self.val)==list, "Can't remove a candidate from a solved cell"
    if cand in self.val: self.val.remove(cand)
    if len(self.val)==1: self.solve(self.val[0])
```

And here's the results:

```python
hard = [
  [0,0,9,0,0,0,4,0,0],
  [0,0,7,0,8,0,1,0,0],
  [1,0,0,2,0,5,0,0,9],
  [2,0,0,0,4,0,0,0,7],
  [0,6,0,9,0,7,0,3,0],
  [9,0,0,0,3,0,0,0,6],
  [7,0,0,8,0,2,0,0,4],
  [0,0,2,0,6,0,8,0,0],
  [0,0,8,0,0,0,7,0,0]]

Grid(hard).solve()
```

```
829|613|475
657|489|123
134|275|689
---+---+---
283|546|917
461|927|538
975|138|246
---+---+---
716|852|394
392|764|851
548|391|762
Score: 0
Sum: 405
```

Woohoo! Feeling pretty confident, I run all 50 of the sudoku grids from Project Euler problem 96 through my algorithm. Here are the sums of the solved squares:

```
'Grid 01': 405, 'Grid 02': 405, 'Grid 03': 405, 'Grid 04': 405, 'Grid 05': 405,
'Grid 06': 160, 'Grid 07': 405, 'Grid 08': 405, 'Grid 09': 405, 'Grid 10': 405,
'Grid 11': 405, 'Grid 12': 405, 'Grid 13': 405, 'Grid 14': 405, 'Grid 15': 405,
'Grid 16': 405, 'Grid 17': 405, 'Grid 18': 405, 'Grid 19': 405, 'Grid 20': 405,
'Grid 21': 405, 'Grid 22': 405, 'Grid 23': 405, 'Grid 24': 405, 'Grid 25': 405,
'Grid 26': 405, 'Grid 27': 405, 'Grid 28': 405, 'Grid 29': 405, 'Grid 30': 405,
'Grid 31': 405, 'Grid 32': 405, 'Grid 33': 405, 'Grid 34': 405, 'Grid 35': 405,
'Grid 36': 405, 'Grid 37': 405, 'Grid 38': 405, 'Grid 39': 405, 'Grid 40': 405,
'Grid 41': 405, 'Grid 42': 223, 'Grid 43': 405, 'Grid 44': 405, 'Grid 45': 405,
'Grid 46': 405, 'Grid 47': 405, 'Grid 48': 405, 'Grid 49': 405, 'Grid 50': 405
```

Holy cow! Only two of the grids weren't solved with these methods!! I guess I'll try adding the X-wing functionality for columns. Here's the new code for that:

```python
    if len(cols)>=2:
      pos={}
      for col in cols:
        pos[col]=[cell.row for cell in grid.col(col) if type(cell.val)==list and d in cell.val]
      for a in range(len(cols)-1):
        for b in range(a+1,len(cols)):
          if pos[cols[a]]==pos[cols[b]]:
            lockedcols=[cols[a],cols[b]]
            lockedrows=pos[cols[a]]
            #print("digit %d is locked in rows %s in columns %s" %(d,lockedrows,lockedcols))
            for row in lockedrows:
              for cell in grid.row(row):
                if cell.col not in lockedcols:
                  if type(cell.val)==list and d in cell.val: cell.remove(d)
```

And that solved grid 06! All but grid 42 are now solved. I'm going to call it a day there - this is the farthest I've ever gotten in solving problem 96, so I feel really good about my progress. Before I do any more coding, I'm going to plug grid 42 into a sudoku app and see if I can figure out what my next step would be in solving it, because I don't want to put too much time into building an alorithm that isn't actually going to help. So I guess stay tuned!
