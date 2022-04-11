# Pac-Man-projects
The Pac-Man projects teach foundational AI concepts.
The projects allow you to visualize the results of the techniques you implement.
Pac-Man provides a challenging problem environment that demands creative solutions.

![Alt text](pacman_game.gif)

# Project 1
In this project, Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently.
I have built general search algorithms that apply to Pacman scenarios.


The files i edited are search.py and searchAgents.py.

**Vizualize Algorithms**

**Q1**: Finding a Fixed Food Dot using Depth First Search

    python pacman.py -l mediumMaze -p SearchAgent
    
**Q2**: Breadth First Search

    python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
    
**Q3**: A* search

    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
    
**Q4**: Finding all the corners

    python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
    
**Q5**: Corners Problem with Heuristic

    python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
    
**Q6**: Eating All The Dots (!need to wait ~1 min)

    python pacman.py -l trickySearch -p AStarFoodSearchAgent
    
**Q7**: Suboptimal Search(greedily eats the closest dot)

    python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5

# Project 2
In this project, i have designed agents for the classic version of Pacman, including ghosts.
Along the way, i implemented both minimax, expectimax search and evaluation functions.


The files i edited are multiAgents.py and pacman.py.

**Q1**:Improve the ReflexAgent to play respectably
    
    python pacman.py --frameTime 0 -p ReflexAgent -k 2

**Q2**:

**Q3**:

**Q4**:

**Q5**:

**Q6**:

**Q7**:

**Q8**:

