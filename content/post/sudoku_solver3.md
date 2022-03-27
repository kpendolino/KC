+++
url = "/2022/03/22/sudoku_solver3/"
title = "Sudoku Solver - Day 3"
date = "2022-03-22"
draft = false
tags = ["python","sudoku_solver"]
topics = ["coding"]
description = ""
+++

The next order of business was to see how far we could get solving using only naked singles and hidden singles.

```python
easy=[
    [0,5,0,4,0,9,0,0,2],
    [4,0,0,6,0,0,0,7,0],
    [0,0,2,0,0,0,8,0,9],
    [0,0,0,0,3,0,0,0,7],
    [0,0,4,0,0,0,3,6,0],
    [0,0,0,0,2,0,0,0,4],
    [0,0,3,0,0,0,7,0,5],
    [1,0,0,3,0,0,0,2,0],
    [0,4,0,7,0,8,0,0,1]]

gr=Grid(easy)
gr.solve()
```

```
358|479|612
491|682|573
672|153|849
---+---+---
816|534|297
524|917|368
739|826|154
---+---+---
963|241|785
187|395|426
245|768|931
Score: 0
Sum: 405
```

Oh, ok. I guess I'll keep going then.

```python
moderate = [
  [8,0,0,0,6,0,0,0,3],
  [0,0,2,0,0,0,4,0,0],
  [0,3,6,2,0,4,7,8,0],
  [0,0,1,3,0,7,5,0,0],
  [4,0,0,0,5,0,0,0,7],
  [0,0,8,1,0,6,2,0,0],
  [0,8,9,4,0,1,3,7,0],
  [0,0,4,0,0,0,8,0,0],
  [3,0,0,0,7,0,0,0,2]]

Grid(moderate).solve()
```

```
847|569|123
192|783|456
536|214|789
---+---+---
921|347|568
463|852|917
758|196|234
---+---+---
689|421|375
274|635|891
315|978|642
Score: 0
Sum: 405
```

Oh. Well. Ok.

```python
advanced = [
  [4,0,2,0,0,7,9,0,1],
  [0,0,0,8,0,0,0,0,0],
  [3,0,0,5,0,0,0,0,6],
  [5,0,0,0,3,0,1,6,0],
  [0,0,0,6,0,5,0,0,0],
  [0,2,6,0,4,0,0,0,3],
  [1,0,0,0,0,6,0,0,9],
  [0,0,0,0,0,9,0,0,0],
  [7,0,9,4,0,0,6,0,5]]

Grid(advanced).solve()
```

```
Score: 195
Score: 165
Score: 142
Score: 138
Score: 138
452|367|981
600|800|000
308|500|006
---+---+---
500|030|160
000|605|000
026|040|003
---+---+---
100|006|009
260|009|000
789|403|605
```

Oh thank goodness! Now it gets exciting. I decided to implement nakedPairs next - this looks for two cells in the same group that have the same candidate list 2 digits long.

```python
def nakedPairs(group):
  # Only look at cells with exactly 2 candidates
  poss=[cell for cell in group if type(cell.val)==list and len(cell.val)==2]
  if len(poss)<2: return
  for a in range(len(poss)-1):
    for b in range(a+1,len(poss)):
      if poss[a].val==poss[b].val:
        # Remove those two values from every other cell
        for cell in group:
          if type(cell.val)==int: 
            # This cell is already solved
            continue
          if cell.val==poss[a].val: 
            # This is one of the two cells that must contain these values
            continue
          # If I've gotten this far, it's a cell that shouldn't contain those two values
          if poss[a].val[0] in cell.val: cell.val.remove(poss[a].val[0])
          if poss[a].val[1] in cell.val: cell.val.remove(poss[a].val[1])
```

And now to put it to the test. I wrote this code up and tried to solve the "advanced" grid again and...no change? Ah, yeah, see, it works better if you remember to actually *call* your new methods.

```python
class Grid():
...
  def round(self):
    for i in range(9):
      nakedSingles(self.row(i))
      hiddenSingles(self.row(i))
      nakedPairs(self.row(i))
    for j in range(9):
      hiddenSingles(self.col(j))
      nakedPairs(self.col(j))
    for k in range(9):
      hiddenSingles(self.box(k))
      nakedPairs(self.box(k))
...
```

Ok, moment of truth...

```
Score: 195
Score: 159
Score: 118
Score: 62
Score: 0
Score: 0
452|367|981
691|824|537
378|591|246
---+---+---
547|932|168
813|675|492
926|148|753
---+---+---
134|256|879
265|789|314
789|413|625
```

Awesome! It worked a treat. Let's up the ante.

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
Score: 183
Score: 139
Score: 119
Score: 116
Score: 116
009|010|470
007|489|100
100|275|009
---+---+---
200|040|907
060|927|530
970|038|246
---+---+---
700|802|004
002|760|800
008|000|700
```

Excellent! Ok, so I guess it's time to implement hiddenPairs. This looks for pairs of cells in the same group that are the only cells in that group which can contain the same pair of values.

```python
def hiddenPairs(group):
  unsolved=[n for n in range(1,10) if not n in [cell.val for cell in group if type(cell.val)==int]]
  #print(unsolved)
  duos=[n for n in unsolved if len([cell for cell in group if type(cell.val)==list and n in cell.val])==2]
  #print(duos)
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

Gotta remember to actually, y'know, use that function.

```python
class Grid():
...
  def round(self):
    for i in range(9):
      nakedSingles(self.row(i))
      hiddenSingles(self.row(i))
      nakedPairs(self.row(i))
      hiddenPairs(self.row(i))
    for j in range(9):
      hiddenSingles(self.col(j))
      nakedPairs(self.col(j))
      hiddenPairs(self.col(j))
    for k in range(9):
      hiddenSingles(self.box(k))
      nakedPairs(self.box(k))
      hiddenPairs(self.box(k))
...
```

And let's see how that works for us.

```
Score: 183
Score: 119
Score: 19
Score: 0
Score: 0
829|310|475
507|489|123
104|275|689
---+---+---
203|640|907
461|927|538
970|138|246
---+---+---
713|852|694
092|764|851
648|300|702
```

Awesome! At this point, we've implemented the most basic solving techniques. I haven't decided yet whether I'll develop this further. We still haven't touched naked or hidden triples, which should be an easy enough extension of the code I wrote for pairs. And I haven't put *any* effort into efficiency, so, there are probably some gains that could be made there. But for now, I feel good with where this is. I hope you've enjoyed the ride!

> **Hi, it's hindsight Kendra here.**
> See, I've just noticed what some of you may have already noticed. There are some zeros still in that grid! So it's not actually solved, even though the score somehow got down to zero.
> I'm guessing there's a glitch in my algorithm. Next step is to troubleshoot that and figure out what the heck went wrong.
> Please enjoy my blissful unawareness of the flaws in my methods up to this point. Stay tuned for the next iteration where I'll share - as best I can gather - what the heck went wrong. Here's what that grid actually looks like:

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

> So I'll revisit this shortly. Stay tuned!
