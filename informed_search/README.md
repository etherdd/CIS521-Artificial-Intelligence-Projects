# informed search problems

### 1. Tile Puzzle
This game provides two solvers for a generalized version of the Eight Puzzle, in which the board can have any number of rows and columns. You can play with an interactive version of the Tile Puzzle using the provided GUI by running the following command: 

`python3 homework3_tile_puzzle_gui.py rows cols`

The arguments `rows` and `cols` are positive integers designating the size of the puzzle. You can choose the solvers implemented with IDDFS / A* search using the Manhattan distance heuristic.
   
### 2. Grid Navigation
This game is a navigation on a two-dimensional grid with obstacles. The goal is to produce the shortest path between a provided pair of points. You can visualize the paths it produces using the provided GUI by running the following command: 

`python InformedSearch_grid_navigation_gui.py scene_path` 

The argument `scene_path` is a path to a scene file storing the layout of the target grid and obstacles. Here provides 3 scene files `scene_path/scene_simple.txt` `scene_path/scene_barrier.txt` `scene_path/scene_randon.txt`. The solver is implemented with A* asearch using the Euclidean distanc heuristic.
