
# Approaches using Python

**1st Apr 2018**

The following are three examples of non-OO approached using pure Python.

## Updating unit tests

Start by updating the Move enum:

<img src="images/enum.PNG">

...and test expectations as follows:

<img src="images/updated_test.PNG">


## Payoff matrix

This approach uses an explicitly defined payoff matrix Game Theory formulation.
To adapt to our change in business requirement, we need simply to update the matrix:

<img src="images/payoff.PNG">

## The obligatory one-liner

As an occasional code golf enthusiast (albeit one with a pretty poor handicap) it 
would seem remiss not to include it.

<img src="images/one_liner.PNG">

## Directed graph

This approach (loosely) models the problem as a directed graph where each vertex
has an edge which 'points at' the vertex which it beats and 'is pointed at' by
the vertex which it is beaten by.  In abstract:

```
 _______        _______
|       | ---> |       |
| Node0 |      | Node1 |
|_______| <--- |_______|

```

Each edge has a penalty which encodes the payoff; to play the game, we navigate
from player 1's chosen Node to player 2's in one step - if we can, then we 
observe the edge penalty to infer game outcome; if we can't then it's a draw.

No changes are required since the structure of the graph is inferred entirely 
from the ordering of enum values.

It would be possible to leverage some OO principles to make the graph modelling
and edge traversal more obvious, but this is deemed out of scope for this lesson.

## Others

There are some interesting solutions using truth tables which involve binary / 
one-hot encoding of possible moves and composition of OR, AND and NOT logic to
determine outcome.  But even the vanilla Rock-Paper-Scissors is laborious to
encode and its extension to 4 moves is even more so.
