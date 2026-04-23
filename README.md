# fly_in

This project has been created as part of the 42 curriculum by [mosafa]https://profile-v3.intra.42.fr/users/mosafa

## Description

This project implements a graph-based pathfinding algorithm designed to navigate drones from a starting vertex to a target destination. The primary objective is to minimize 
total turns while adhering to multi-layered constraints, including connection capacities and zone-specific traversal rules. Zones are categorized by cost and accessibility: 
Priority (preferred), Normal, Restricted (incurring a 2-turn penalty), and Blocked (traversal prohibited).


## Instructions

For using the script of fly_in run `fly_in.py` by puting your desired map path in the (MAP) in Makefile and run:

```Bash
make run
```

first to make sure you install all required packages run:

```Bash
make install
```
And for run the main script in debug mode:

```Bash
make debug
```
To clean temporary files:

```Bash
make clean
```
Lastly to run flake8 and mypy:

```Bash
make lint
```


## Resource

Dijikstra algorithm: https://youtu.be/_lHSawdgXpI?si=rx2DGCb4LGGy-1sW

BFS algorithm: https://youtu.be/xlVX7dXLS64?si=I0ZYINY7la3RAYzp

**I used AI to understand how to use the arcade package to draw the graph and the moving of drones and also to know how 
 to implement dijikstra algo as a code.**

## input instructions:

Define the number of drones at the very beginning of the file. Ensure the configuration includes exactly one start and one end zone. Every zone must have a unique name and 
coordinate set. Additionally, connections between zones must be unique (no duplicate pairs). You may include optional metadata fields for both zones and connections, such as 
capacity and color.lastly you map will be tested (by BFS) if a path to the end zone exist or not.

**hint: a set of maps is given with the project will help to test the script**

## technical choices

For this project, I implemented a multi-layered algorithmic approach to ensure efficient drone navigation and system reliability:

### Dijkstra’s Algorithm:

 Selected as the primary pathfinding engine, Dijkstra's algorithm calculates the optimal distance from each node to the destination. This enables the drones to consistently 
 select the shortest path while accounting for weighted costs across different zone types.

### Breadth-First Search (BFS):

 I utilized BFS as a pre-processing validation step. It effectively detects dead ends and verifies map connectivity, ensuring a valid path exists between the start and end 
 zones before path calculation begins.

### Arcade Library:

 For the graphical interface, I chose the Python Arcade package. This allows for a dynamic visual representation of the map and provides smooth, real-time animation of the 
 drones as they traverse the graph.
 