# viterbiHMM

An implementation of Viterbi algorithm in Hidden Markov Model to figure out the most likely trajectory of a robot in this grid-world.

- The file hmm-data.txt contains a map of a 10-by-10 2D grid-world. 
- The free cells are represented as '1's and the obstacles are represented as '0's. 
- There are four towers, one in each of the four corners, as indicated in the data file. 
- Assume that the initial position of the robot has a uniform prior over all free cells. 
- In each time-step, the robot moves to one of its four neighboring free cells chosen uniformly at random. 
- At a given cell, the robot measures L2 distances (Euclidean distances) to each of the towers. 
- For a true distance d, the robot records a noisy measurement chosen uniformly at random from the set of numbers in the interval [0.7d, 1.3d] with one decimal place. 
- Output the coordinates of the most likely trajectory of the robot for 11 time-steps. 
- For tie breaking, always prefer the one with a smaller x coordinate, and a smaller y coordinate if the x coordinates are equal.
