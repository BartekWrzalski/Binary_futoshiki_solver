# Binary sudoku and futoshiki solver
Binary sudoku and futoshiki solver that solves puzzles using backtracking or forward checking, with 2 possible heuristics for 2nd algorithm

Some examples of puzzles are in `Puzzles` folder. If you want to put your own, you have to keep it in this format:
## Binary NxN (6x6 below)
```
xxx1xx
xx0xx1
0xxx0x
x11xxx
xxxxxx
1xxx0x
```
## Futoshiki NxN (4x4 below)
```
x>x-x-x
----
x<x-3>x
-->-
x-x-x-x
<---
x-x>x<x
```
Where `>` and `<` in rows with `x` values means which value have to greater/lower in row. In column, `>` means that value above have to be greater than the value below, analogously, the `<` means opposite.

## Algorithms
There are two implemented algorithms that solves puzzle, first is backtracking, second is forward-checking. For forward checking there is two heuristic implemented for selecting next fields in puzzle and selecting values for them. You can either choose selecting new field next to the previous one, or looking for the one with smallest domain. For value you can choose selecting values one by another or in order of the smallest number of value occurences in row and column. You can select them by writing an option to method call.
Exaples:
```
backtrack.backtrack_searching(puzzle)
forward.forward_checking(puzzle, choose_variable='sequence', choose_value='sequence')
forward.forward_checking(puzzle, choose_variable='sequence', choose_value='low_occurrence')
forward.forward_checking(puzzle, choose_variable='small_domain', choose_value='sequence')
forward.forward_checking(puzzle, choose_variable='small_domain', choose_value='low_occurrence')
```
`Sequence` is default value for both of options.
