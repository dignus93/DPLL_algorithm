# DPLL_algorithm

A personal python version of the Davis–Putnam–Logemann–Loveland (DPLL) algorithm: a complete, backtracking-based search algorithm for deciding the satisfiability of propositional logic formulae in conjunctive normal form, i.e. for solving the CNF-SAT problem.

When you run the algorithm on a python IDE like pycharm, the console asks you:
-input n
The half size of the alphabet
-input k
The number of the literal in clauses
-input m
The number of clauses

If a letter is true in lowerCase, it is false in upperCase and viceversa.
For example with n=k=m=3 we could have a proposition like
p={[A or B or c] and [A or b or c] and [B or C or a]}
The algorithm will find the value for A,B,C in order to have a TRUE proposition p

The algorithm assign values to the letters in order to have a true formula. For every letter the procedure follows an heuristic:
1) It is checked if the letter is pure, i.e. there is not its negation in all other clauses. If the letter is pure the true value is assigned.
2) If the letter is not pure it is checked if the letter is in a unitarian clause, i.e. a clause where all the other letter has a false value. If it is like that a true value is assigned.
3) If the letter is not pure and is not in a unitarian clause a random boolean value is assigned

There is a TEST section in the code to check the performance of the code. Decomment it and comment the MAIN section to try it. The test showed that if we increase the m/n ratio over 0.24 we have a less true formulas. 
