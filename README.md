# Sokoban Solver – AI Project

This project focuses on implementing and analyzing heuristic search algorithms for solving the **Sokoban puzzle game** as part of an Artificial Intelligence assignment.  

## Features
- **Implemented algorithms:**
  - **Beam Search** – global, level-based search strategy with tunable `beam_width`.
  - **LRTA\*** – online learning algorithm updating heuristic values incrementally.

- **Heuristics tested:**
  - Manhattan distance (basic and improved versions).
  - BFS-based distance heuristic (accounts for real obstacles).
  - Misplaced boxes heuristic.
  - Custom Sokoban-specific heuristic (penalizing unnecessary moves, prioritizing useful box pushes).

- **Optimizations:**
  - Adaptive restart for Beam Search when heuristic stagnates.
  - Ignoring already placed boxes (cost = 0).
  - Integration of player-to-box distance to better guide moves.
  - Controlled fallback for BFS failures with finite cost.
  - Performance charts comparing algorithms across multiple map sets.

## Results
- Beam Search achieved efficient runtimes on most maps, with sub-second performance on small/medium ones.
- Improved heuristics significantly reduced time on complex maps
- LRTA\* performed well on small maps but showed higher oscillation and pull moves on complex maps.

## Tech & Skills
- **Language:** Python  
- **Concepts:** Heuristic search, pathfinding, state-space representation, incremental learning  
- **Skills gained:** Algorithm optimization, heuristic design, performance analysis, AI problem-solving  

## Conclusion
This project highlights the trade-offs between offline search strategies like Beam Search and online learning approaches like LRTA\*. By designing better heuristics and optimizations, Sokoban instances of increasing difficulty can be solved more efficiently.
