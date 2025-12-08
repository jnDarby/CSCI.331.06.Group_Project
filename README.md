# CSCI.331.06.Group_Project
## Group Members
- Emma Schmitt
- Nafiu Chowdhury
- Jacob Darby

## Project Outline
We decided to tackle Project 3 which is the New York City Route Planner Project, the outline of the projectis isted below. Our plan is to seperate out the search algorithms accordingly and work together to complete them. We will be using Python for this project as every group member is comfortable with the language and for the amount of graphing and drawing libraries that are avaliable. Each group member has also worked on figuring out the best way to represent the cities in terms of coordinates and the spreadsheet we created will be listed below...

### Project Description
You will design a New York City Route Planner where ~20-30 major cities in New York State
(e.g., Rochester, Buffalo, Syracuse, Albany, Ithaca, Binghamton, Niagara Falls, New York City,
etc.) are represented as nodes in a graph. The edges between cities will be weighted by actual
road distances (miles). The heuristic cost for informed search will be the straight-line distance
between city coordinates (compute using the Haversine formula or any other alternatives). The
start node is Rochester (RIT), and the user will choose the destination city. You should
implement DFS, BFS, IDS, UCS, Greedy Best-First Search, A*, and IDA* search to find paths
from Rochester to the chosen destination. For each algorithm, compare the path cost, number
of expanded nodes, and runtime, and clearly identify which algorithm(s) return optimal solutions
under these conditions. A graph drawing with nodes and weighted edges must be developed.
You are required to prepare the dataset yourself (nodes, road distances, and heuristic values),
making any reasonable assumptions whenever needed or when exact data is not obvious

### Search Algorithms Needed
- DFS
- BFS
- IDS
- UCS
- Greedy Best First Search (Greedy Algo)
- A*
- and IDA*

### Graph Representation
At the moment, we are unsure of how we will represent or create the graph but we have started research/have brainstormed a few libraries. We have also asked the Professor for advice in terms of possible resources/libraries. In the end, we decided to use Graphviz for implementing and generating our graphs, which are created automatically when running the program for each of the searches. Below, however, are some brainstorming ideas that were generated...
  - SNAPPY: https://snap.stanford.edu/snappy/
  - Turtle
  - graph-tool: https://graph-tool.skewed.de/static/docs/stable/index.html
  - NetworkX: https://networkx.org/
 
### Links to Group Resources
  - WEEKLY MEETINGS ON MONDAY AT 3:30 PM
  - Google Sheet: https://docs.google.com/spreadsheets/d/10dCfXj0hHEcB0W_tjT5zHKGt1g8L4ttx7wqCLtV5MFg/edit?usp=sharing
