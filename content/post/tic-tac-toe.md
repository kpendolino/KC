+++
url = "2022/03/30/tic_tac_toe/"
title = "Tic Tac Toe"
date = "2022-03-30"
tags = ["python"]
topics = ["coding"]
description = "How many unique games of Tic-Tac-Toe are there?"
+++

Have you ever wondered how many unique games of Tic-Tac-Toe there are? This question snuck into my brain the other day and I just had to find out. Come with me and see! My full source code for this exercise, including comments and random debugging notes that I omitted in this post, can be seen at [https://replit.com/@KendraPendolino/TicTacToe](https://replit.com/@KendraPendolino/TicTacToe). 

Before we dive in, I want to talk a little bit about **equivalent boards**. For the purposes of these exercises, I'm calling two boards **equivalent** if they:

- Match
- Match after one grid is mirrored (horizontally, vertically, or both)
- Match after one grid is rotated (90&deg;, 180&deg;, or 270&deg;)
- Match after one grid is mirrored **and** rotated

In short, if you can make the boards look the same by turning your head or playing with mirrors, they're the same for my purposes.

## Setup

First, some housekeeping.

```python
x="X"
o="O"
e="-"
```

This code just sets up a shorthand for the three possible values a space can contain: "X", "O", or "-" (_e_ for _empty_).

```python
win=[]
diag1=[]
diag2=[]
for a in range(3):
  win.append([[a,j] for j in range(3)]) #cols
  win.append([[i,a] for i in range(3)]) #rows
  diag1.append([a,a])
  diag2.append([a,2-a])
win.append(diag1)
win.append(diag2)
```

This code defines the combinations of cells that can trigger a victory, e.g. each row, column, and diagonal.

## Defining The Board

I decided to set up a `Board` class to wrangle storing, formatting, and printing data, calculating equivalent grids, determining valid moves, and checking whether the game is won.

```python
class Board():
  def __init__(self, board=None,hash=None):
    if not hash==None: 
      lines=[hash[0:3],hash[4:7],hash[8:12]]
      self.b = [[c for c in line] for line in lines]
    elif not board==None: self.b = board
    else: self.b = [[e for j in range(3)] for i in range(3)]
  ...
```

In the init method, I handle setting up the board. If `board` and `hash` are both omitted, it sets up a blank board in `self.e`, with a 3x3 array containing `e` in each cell. If `board` is provided, it is saved as `self.b`. I also added support for initializing a board from a `hash`. This is just a representation of a board as a string, like <span style="white-space: nowrap;">`"XO-,---,-OX"`</style>. You'll see why I added this a little later.

> Note: This is code that I wrote for myself for exploration - it doesn't include the kind of validation and error checking that you'd want if you were going to make this class public. For instance, I don't check that `board` is a 3x3 array that contains only "X", "O", or "e".

```python
class Board():
  ...
  def hash(self):
    return "%s,%s,%s"%("".join([self.b[0][j] for j in range(3)]),
                       "".join([self.b[1][j] for j in range(3)]),
                       "".join([self.b[2][j] for j in range(3)]), 
                       )
  def copy(self):
    return Board(board=[[self.b[i][j] for j in range(3)] for i in range(3)])
  ...
```

In this section, I added two utility methods: `hash` to return a representation of the grid as a string - this can be fed back into the Board constructor to generate a new board - and `copy` to make a clone of a board.

```python
class Board():
  ...
  def flip(self,flip):
    if flip=="": return self.b
    if flip=="H": return [[self.b[i][2-j] for j in range(3)]
                          for i in range (3)]
    if flip=="V": return [[self.b[2-i][j] for j in range(3)]
                          for i in range (3)]
    if flip in ["HV","VH"]: return [[self.b[2-i][2-j] for j in range (3)] 
                                    for i in range (3)]
    return False
  def rot(self,rot):
    if rot=="": return self.b
    if rot=="CW": return [[self.b[2-j][i] for j in range (3)] 
                          for i in range (3)]
    if rot=="CCW": return [[self.b[j][2-i] for j in range (3)] 
                           for i in range (3)]
    if rot=="180": return [[self.b[2-j][2-i] for j in range (3)] 
                           for i in range (3)]
    return False
  ...
```

Here, I've added code to generate equivalent versions of the same board - these return what the grid would look like if it were flipped (vertically, horizontally, or both) or rotated (clockwise, counterclockwise, or 180 degrees). These will come into play when I'm checking to make sure I'm not retracing my steps or duplicating effort.


```python
class Board():
  ...
  def pr(self,label=None):
    if label: print(label)
    for i in range(3):
      print("".join(self.b[i]))
    print()
  ...
```

Up next, a method to print out the board in a readable grid, with an optional label for clarity. I used this a lot when I was testing the code to generate flips and rotations and the code to test whether two boards are equivalent.

```python
class Board():
  ...
  def getEqHashes(self):
    hashes=[]
    for b_rot in ["","CW","CCW","180"]:
      r = Board(board=self.rot(b_rot))
      for b_flip in ["","H","V","VH"]:
        f= Board(board=r.flip(b_flip))
        hashes.append(f.hash())
    return hashes 
  ...
```

This little fella returns a list of hashes of all boards that are equivalent to this board.

```python
class Board():
  ...
  def eqhash(self, bd2hash):
    return self.equivalent(Board(hash=bd2hash))
  def equivalent(self, bd2):
    self.pr("Board 1")
    bd2.pr("Board 2")
    if self.b==bd2.b: return True
    for b_rot in ["","CW","CCW","180"]:
      r = Board(bd2.rot(b_rot))
      for b_flip in ["","H","V","VH"]:
        f=r.flip(b_flip)
        if self.b==f: 
          #self.pr("Board 1")
          #bd2.pr("Board 2")
          #r.pr("Board 2, rotated %s"%b_rot)
          #Board(f).pr("Board 2, rotated %s and flipped %s"%(b_rot,b_flip))
          return True
    return False
  ...
```

These two are friends! The `equivalent(bd2)` method tells you whether the current board (`self`) and the board provided as `bd2` are equivalent. `equivalent(bd2hash)` does the same thing, but takes a hash instead of a `Board`.

```python
class Board():
  ...
  def unclaimed(self):
    return [[i,j] for j in range(3) for i in range(3) if self.b[i][j]==e ]
  def move(self,player,i,j):
    # returns [board after this move (Board), 
    #          isGameOver (boolean), 
    #          [isGameVictory (boolean)]]
    if self.b[i][j]!=e: return False
    self.b[i][j]=player
    #check if win condition met
    for w in win:
      thisw=True
      for c in w:
        if self.b[c[0]][c[1]]!=player: 
          thisw=False
          break
      if thisw:
        return [self,True,True]
    if len(self.unclaimed())==0: return [self,True,False] # it's a draw
    return [self,False]
  ...
```

The `unclaimed()` method just serves up a list of possible moves (`i`, `j` coordinates) that aren't yet taken. I use this with `move(player,i,j)` to explore all possible outcomes of the games. Since I only try moves in the `unclaimed` list, there shouldn't ever be an illegal move, but I do have this method return `False` in case that does happen. If the move doesn't end the game, this will return a list like `[Board, False]`. If the move ends the game, it will look like `[Board, True, (boolean)]`, where the last boolean value indicates whether it's a victory (`True`) or a tie (`False`).

Last but not least, I added two stand-alone functions to help view the output in a human-friendly way.

```python
def writeandprint(out=""):
  with open("summary.txt","a") as file:
    file.write(out+"\n")  
    print(out)  

def printFinished(finished,label=None):
  if label: writeandprint("There are %d distinct %s boards"%(len(finished),label))
  else: writeandprint("There are %d distinct boards"%len(finished))
  fin=list(finished)

  for x in range(len(fin)):
    b_x=Board(hash=fin[x])
    b_hashes=b_x.getEqHashes()
    for y in range(x+1,len(fin)):
      if fin[y] in b_hashes:
        input("duplicate boards: %s and %s"%(fin[x],fin[y]))
  
  for bds in [fin[5*a:5*a+5] for a in range(len(fin)//5)]:
    #print(bds)
    writeandprint("\t\t".join([bds[a][:3] for a in range(5)]))
    writeandprint("\t\t".join([bds[a][4:7] for a in range(5)]))
    writeandprint("\t\t".join([bds[a][8:11] for a in range(5)]))
    writeandprint()
  if len(fin)/5>len(fin)//5:
    bds=fin[5*(len(fin)//5):len(fin)]
    writeandprint("\t\t".join([bds[a][:3] for a in range(len(bds))]))
    writeandprint("\t\t".join([bds[a][4:7] for a in range(len(bds))]))
    writeandprint("\t\t".join([bds[a][8:11] for a in range(len(bds))]))
    writeandprint()
```

I added `writeandprint()` because I wanted to save the output to a file _and_ see it in the console output. Last but not least, `printFinished(finished,label)` goes through the boards in the `finished` set and prints them out five at a time.

Now we're ready to get rolling!

## Exploring All Possible Moves

I use a recursive function to explore all possible moves from a given point. Here's some basic setup before we dive in there:

```python
turns={}
finished=set()
wins=set()
ties=set()
```

Just setting up a way to track the possible turns we've seen (e.g. what can the board look like after 1 turn? After 3? After 6?). Now for the juicy bit.


```python
def allMoves(board,turn):
  if not turn in turns: turns[turn]=set()

  if turn%2==0: player=o
  else: player=x

  opts=board.unclaimed()
  for opt in opts:
    next = board.copy().move(player,opt[0],opt[1])
    if next==False: 
      print("illegal move: ","%s,%s,%s + %s @ (%d,%d)" % 
               (board.b[0],board.b[1],board.b[2],player,opt[0],opt[1]))
      continue
    hashes=next[0].getEqHashes()
    alreadyseen=False
    for hash in hashes:
      if hash in turns[turn]: 
        alreadyseen=True
        break
    if alreadyseen: continue
    hash=next[0].hash()
    turns[turn].add(hash)
    if next[1]==True: #game over
      finished.add(hash)
      if next[2]==True: wins.add(hash)
      elif next[2]==False: ties.add(hash)
    else: #keep playing
      allMoves(next[0],turn+1)
```

This function calls itself over and over again until the game ends. Each time, it plays out a different scenario for the next move - by the time the first call to `allMoves` finishes, every possible scenario has been played.

First, I do a little housekeeping - setting up `turns[turn]` if it's not already there. I'm using `set()` because I don't want to store duplicates - unique hashes only, please! Incidentally, this is why I created the `Board.hash()` method - I couldn't add the 3 x 3 arrays to these sets since Python can't hash lists, so I created my own hash function for this purpose.

Next, I figure out whose turn it is ("X" or "O"), then it's time to get all possible options (`opts`) for the next move by checking `board.unclaimed()`. This is how I fork the function to see all possibilities. I loop through this list, cloning the board for each iteration and having the current player make their move in the indicated space. Just in case there's a bug in my code, I continue to the next iteration if the move is invalid.

> Note: I never did see that "illegal move" message - it's such a nice feeling when you build in guard rails that you don't end up needing!

Once I've completed the indicated move, I check through all of the equivalent hashes (e.g hashes of other boards that are functionally identical) and compare them against the moves saved in `turns[turn]`. If we've already been here, `alreadyseen=True` and we can move on to the next move. Otherwise, I get the hash of this move and check whether the game continues or not. If it's game over, I add the hash to `finished` and either `wins` or `ties` depending on how the game ended. If the game continues, I call `allMoves` again to do the next move.

```python
allMoves(blank,1)
printFinished(finished,label="Finished")
printFinished(wins,label="Wins")
printFinished(ties,label="Ties")
```

The only thing left to do is call `allMoves` with a blank board for turn 1, and take a look at the output. Here's an excerpt from that output:

```
There are 138 distinct Finished boards
X-O		XXO		O--		OXO		XOO
O-O		X-X		XXX		XOX		OXX
XXX		OOO		-O-		OX-		XXO

...

XXX		X-X		X--
OOX		OOO		XOO
O--		-X-		X--

There are 135 distinct Wins boards
X-O		XXO		O--		OXO		XXX
O-O		X-X		XXX		XOX		XO-
XXX		OOO		-O-		OX-		O-O

...

X-O		XX-		XXX		X-X		X--
XXO		--X		OOX		OOO		XOO
OXO		OOO		O--		-X-		X--

There are 3 distinct Ties boards
XOO		XXO		XOX
OXX		OOX		OOX
XXO		XXO		XXO
```

You can see the full output here: [summary.txt](https://replit.com/@KendraPendolino/TicTacToe#summary.txt).

To be extra sure that my results were correct, I used Excel to generate a complete list of all possible grids (filling all 9 positions using any combination of "X" and "O"). I filtered these to show only valid grids (5 "X" and 4 "O") that are ties. The result was 16 possible grids - every one of them equivalent to one of the three tie results shown above. Woohoo!

## Conclusion

It turns out there are 138 _functionally different_ outcomes of Tic-Tac-Toe. There are three ties, which you've probably seen variations on again _and again_ **and again**. There are 135 ways to win the game, but the vast majority of these are implausible if you're playing with experienced players; however they may show up if you're playing with someone who's just learning the game.

I hope you've enjoyed exploring this question with me!

