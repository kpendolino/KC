+++
url = "/2022/03/26/project_euler_p93/"
title = "Project Euler - Problem 93"
date = "2022-03-26"
tags = ["python","coding"]
topics = []
description = ""
+++

Emboldened by my recent completion of Project Euler 96, I decided to take a crack at another problem: [Problem 93](https://projecteuler.net/problem=93). You can read the full text of the problem at the link above, but the gist of it is this: working with a set of four distinct individual digits, arranged in any order, with any combination of parentheses and basic mathematical operations (+, -, /, *), which combination of digits can form the longest string of consecutive positive integers from 1 to _n_ before reaching an integer that can't be formed using those digits?

I want to caveat this right up front and say that I wasn't concerned with efficiency for this problem - my code ran quickly enough that I only made a few small tweaks to make it go faster. So this may not be the fastest or most elegant solution, but it worked!

# Spoilers Ahead

This post contains spoilers for Problem 93. I strongly encourage you to try solving it for yourself before reading on - or at least put together a rough sketch of what approach you'd take!

# My Approach

At a high level, my approach looks like this:

- Create a list of lists of digits
- For each list of digits, create a list of all possible orders of those digits
- Create a list of all possible combinations of operations - three unique operations per expression
- Create a list of all meaningful combinations of parentheses
- For each combination of digits, iterate over each possible order, set of operations, and parentheses, calculate the value of the expression, and add that to a set
- Once that's all finished, check each set for consecutive digits from 1 to _n_, and find the digit combination that reached the highest value of _n_ before reaching an unexpressible term

So, let's take a look at some of the code I used to do this.

## Basic Setup

Here we'll look at the basic functions that I set up to solve this problem.

```python
op=["+","-","*","/"]
p_op=['*','/']

def get_ops(op):
  ops=[[a,b,c] for a in op for b in op for c in op]
  return ops

ops=get_ops(op)
```

I started by defining a `op`, a list of the possible operators. I also defined a smaller list, `p_op`, which contains operators that require me to reevaluate the parentheses. I'll come back to this idea later, but the short version is that I made sure that the order of operations is respected by adding implied parentheses around multiplication and division operations. Finally, `get_ops(op)` just returns a list of all possible orders of operators. The problem allows any selection of these operators, so `a + b + c + d` is just as valid as `a * b + c - d`. This code considers every possibility.

```python
def get_digits():
  #return[[1,2,3,4]] test case
  dig=[]
  for l in range(4,10):
    for k in range(3,l):
      for j in range(2,k):
        for i in range(1,j):
          dig.append([i,j,k,l])
  #print(dig)
  return dig

digits=get_digits()
```

Up next, setting up `get_digits()` to generate the combinations of digits. Initially I had this set to just return `[1,2,3,4]` so I could focus on making sure everything else was working - once I was getting the expected results with `[1,2,3,4]`, I went back and fleshed out the rest of this.

```python
#returns list of list of digits a,b,c,d in every possible order
def scramble(a,b,c,d):
  list=[a,b,c,d]
  orders=[]
  for i in list:
    for j in [j for j in list if not j==i]:
      for k in [k for k in list if not k==i and not k==j]:
        l=[l for l in list if not l==i and not l==j and not l==k][0]
        orders.append([i,j,k,l])
  return orders
```

The `scramble(a,b,c,d)` method does exactly what it sounds like - it takes the digits `a`, `b`, `c`, and `d` and returns each possible order they can appear in.

```python
#returns list of parenthesis combinations like '', 'ab', 'abc', 'abc,ab'
def get_paren(): 
  paren=[]
  none=[""]
  twos=["ab","bc","cd"]
  twopairs=["ab,cd"]
  threes=["abc","bcd"]
  paren+=none
  paren+=twos
  paren+=twopairs
  paren+=threes
  for tri in threes:
    paren+=[duo+","+tri for duo in twos if duo in tri]
  #print(paren)
  return paren

parens=get_paren()
```

And here is where I put together the base list of distinct parenthesis possibilities. I was intially trying to think of a way to generate this list more programatically, like generating lists of possible positions in the equation where the left and right parentheses could go, but I ended up just manually creating the list instead. In the `for tri in threes` loop, I cover situations that look like this: `a + (b * (c - d))` - this is represented as `"cd,bcd"`: "do the operation of `c` and `d` first, then do the operation betwen `b` and `cd`.

```python
def op_paren(op,paren):
  if '*' in op or '/' in op:
    #need to adjust parentheses
    if op[0] in p_op:
      #ab is the first
      if paren in ['ab','ab,cd','ab,abc','bcd','bc,bcd','cd,bcd','bc,abc']:
        pass #this is already captured in the parens
      elif paren=='':paren='ab'
      elif paren=='cd': paren='ab,cd'
      elif paren=='abc': paren='ab,abc'
      elif paren=='bc': paren='bc,abc'
    if op[1] in p_op:
      #bc is included
      if paren in ['bc','bc,abc','bc,bcd','ab,cd','ab,abc','cd,bcd']: pass #it's already included
      elif paren=='': paren='bc'
      elif paren=='ab': paren='ab,abc'
      elif paren=='cd': paren='cd,bcd'
      elif paren=='abc': paren='bc,abc'
      elif paren=='bcd': paren='bc,bcd'
    else: #cd is included
      if paren in ['cd','ab,cd','cd,bcd','abc','ab,abc','bc,abc','bc,bcd']: pass #it's already included
      if paren=='': 
        paren='cd'
      if paren=='ab': paren='ab,cd'
      if paren=='bc': paren='bc,bcd'
      if paren=='bcd': paren='cd,bcd'
  return paren
```

The `op_paren(op,paren)` method revises the parentheses to include any implied parentheses. This is to cover the fact that multiplication and division happens before addition or subtraction, so `a + b * c - d` is calculated as `a + (b * c) - d`. First I check whether the list of operations `op` has any `'*'` or `'/'` operators in it. Then I handle those operators left to right.

```python
def operate(a,b,op):
  if op=="+": return a+b
  if op=="-": return a-b
  if op=="*": return a*b
  if op=="/": 
    if b==0: return False
    return a/b
```

Last but not least for the setup phase, I needed `operate(a,b,op)`. This method takes a pair of digits (or a digit and its neighboring combination) and performs the operation between them. Full disclosure, I totally forgot to include `if b==0: return False` at first. 0 isn't one of the digits that we were working with, but it's definitely possible for an intermediate step to produce something like this: `2 / (1 - (4 - 3))`.

```python
def expr(order,paren,op):
  expr="%d %s %d %s %d %s %d"%(i,op[0],j,op[1],k,op[2],l)
  if paren=='': return expr
  elif paren=='ab':
    expr = "(" + expr[:5]+ ")" + expr[5:] 
  elif paren=='bc':
    expr = expr[:4]+"("+expr[4:9]+")"+expr[9:]
  elif paren=='cd':
    expr= expr[:8] + "(" + expr[8:] + ")"
  elif paren=='ab,cd':
    expr="("+expr[:5]+")"+expr[5:8]+"("+expr[8:]+")"
  elif paren=='abc':
    expr = "(" + expr[:9]+ ")" + expr[9:] 
  elif paren=='bcd':
    expr = expr[:4] + "(" + expr[4:]+ ")"
  elif paren=='ab,abc':
    expr="(("+expr[:5] + ")" +expr[5:9]+ ")" +expr[9:]
  elif paren=='bc,abc':
    expr="("+expr[:4] + "(" + expr[4:9] + "))" +expr[9:]
  elif paren=='bc,bcd':
    expr=expr[:4] + "((" + expr[4:9] + ")" +expr[9:]+ ")"   
  elif paren=='cd,bcd':
    expr=expr[:4] + "(" + expr[4:8] + "(" +expr[8:]+ "))"
  return expr 
```

Again, in full disclosure: I did not plan on needing an `expr(order,paren,op)` method. I don't always know what kind of support functions I'll need to make troubleshooting easier, but I really did need this. This takes the `order`, `paren`, and `op` that are currently being considered and prints it out in a human-readable format like `2 / (1 - (4 - 3))`. I'll talk more about how and why I needed this shortly.

## Putting It All Together

This set of nested loops is where all the magic happens:

```python
results={}
n=0

for dig in digits:
  a=dig[0]
  b=dig[1]
  c=dig[2]
  d=dig[3]
  s_dig="%d%d%d%d"%(a,b,c,d)
  results[s_dig]=set()
  
  orders=scramble(a,b,c,d)
  for order in orders:
    i=order[0]
    j=order[1]
    k=order[2]
    l=order[3]
    print(order)
    for paren in parens:
      for op in ops:
        if op==['+',"+","+"] or op==["*","*","*"]:
          if paren!="": continue # parentheses don't matter if they're all + or all *
          if order!=orders[0]: continue #order doesn't matter if they're all + or all *
        # Have a unique order of digits, parentheses, operators
        #print(expr(order,paren,op))
        orig_paren=paren

        paren=op_paren(op,paren) #revise for order of operations

        if paren in ['','ab','ab,abc','abc']: 
          # do them in order
          ij=operate(i,j,op[0])
          if ij==False: continue
          ijk=operate(ij,k,op[1])
          if ijk==False: continue
          ijkl=operate(ijk,l,op[2])
          if ijkl==False: continue

        ...

        if ijkl>0 and ijkl==int(ijkl):
          results[s_dig].add(int(ijkl))
          #inpt=input("%s = %d"%(expr,int(ijkl)))
          #if order==[2,3,4,1] and op==['*','*','-'] and orig_paren=='':
          #  input("[%d] %s = %s = %d"%(n, expr(order,orig_paren,op), expr(order,paren,op), ijkl))
        n+=1

print(results)
```

This code starts with a set of digits from `digits`. Then it finds the different possible `orders` of those digits. We use nested loops to iterate over every combination of `order`, operations (`op`), and parentheses (`paren`). After the list of operators is picked, I do a quick check to see if this is a redundant calculation. If all of the operators are `'+'` or if all are `'*'`, then it doesn't matter what order the digits are in or what parentheses are present, so I make sure to only handle that situation once.

Next, we revise the parentheses and then actually do the operations. I use a collection of `if` and `elif` blocks to handle groups of parentheses that are equivalent in terms of processing order. After each step, I check to see if `operate` returned `False`, which would indicate that we've just divided by zero. In hindsight, I could have just done this once after processing all operations, since with distinct digits, it should be impossible to end up with a 0 until the last step. The `...` represents the group of `elif` blocks that handle other processing orders - we'll come back to these in a moment.

You may be wondering about the last block of code here. This is how I save the results and handle debugging. The `results[s_dig].add(int(ijkl))` line is the only piece of that if statement that is required to solve the problem - the rest of it (when not commented out) lets me step through each completed calculation one by one to double-check it manually. I set up a counter `n` so that once I knew the first `n` calculations were working as expected, I could skip over those the next time I run my code. 

```python
        elif paren in ['ab,cd','cd']: 
          # ij,kl,ijkl
          ij=operate(i,j,op[0])
          if ij==False: continue
          kl=operate(k,l,op[2])
          if kl==False: continue
          ijkl=operate(ij,kl,op[1])
          if ijkl==False: continue
```

I'm not going to share each of the `elif` blocks, but I did want to share one of them to highlight a silly mistake I initially made. You can see here that this is for processing expressions that look like `(a ? b) ? (c ? d)` or `a ? b ? (c ? d)`, so first we combine the first two terms, then the last two, and then do the operation between those two. When I had the `if` block working properly, I used copy/paste to set up the rest of them and just tweaked the letters involved. But I totally forgot to revise the operator that was being used, so no matter what the order was, I was always using the first operator for the first operation - even if that operation was the last two digits!

When I first ran my code to check whether `[1,2,3,4]` gave the expected results, I was confused. This set of digits was supposed to get up to 28 before reaching a value that couldn't be formed as an expression using those four digits, but in my code, 22 and 23 were missing. I manually thought of a combination that would generate one of those values: `2 * 3 * 4 - 1 = 23`. That allowed me to realize that I had initially been ending my `scramble` function too soon, as I had mistakenly put the `return` statement inside the loop that picks the first digit, so I was considering only orders that began with `1`. Once that was fixed, the code was good to go.

```python
lengths={}
for key in results:
  if 1 in results[key]:
    n=1
    while n+1 in results[key]: n+=1
    lengths[key]=n
print(lengths)
print([key for key in lengths if lengths[key]==max([lengths[key] for key in lengths])])
```

Last but not least, it's time to check out how long of a string of consecutive positive integers each set of digits can produce. So I go through all sets of digits tested, check how many consecutive values there are, and print out the key that produced the maximum length. I won't spoil the answer here, but that set of digits produced all positive integers from 1 to 51 before getting to the first positive integer it couldn't express.

That's all for today - thanks for joining this exploration of my solution to Problem 93!
