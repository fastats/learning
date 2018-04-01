
# Approaches using Python

**1st Apr 2018**

The following are three examples of non-OO approached using pure Python.

## Updating unit tests

Start by updating test expectations as follows:


## Payoff matrix

This approach uses an explicitly defined payoff matrix Game Theory formulation.
To adapt to our change in business requirement, we need simply to update the matrix:


## The obligatory one-liner

This is not necessarily a recommended approach, but as an occasional code golf
enthusiast (albeit one with a pretty poor handicap) it would seem remiss not to
include it.


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

To support the change in business requirement:



There would be cleaner and more obvious graph representations with some
refinement to the way the graph is modelled, but this might lean on some OO
principles and is therefore not included here.
