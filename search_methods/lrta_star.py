from typing import List
from collections import deque
from sokoban.moves import *   # pentru constantele LEFT, RIGHT, BOX_LEFT, ...
from search_methods.heuristics import misplaced_boxes
from search_methods.heuristics import bfs_distance
from search_methods.heuristics import manhattan_heuristic
from search_methods.heuristics import improved_sokoban_heuristic


def lrta_star_solver(start_map) -> List[int]:
    """
    Implementare LRTA*:
      - H: dicţionar <Map, h(n)>
      - path: listă de mutări (constante din moves.py)
    """
    H = {}
    current = start_map.copy()
    path: List[int] = []

    while not current.is_solved():
        # Iniţializez h pentru starea curentă
        if str(current) not in H:
            H[str(current)] = manhattan_heuristic(current)
            #H[str(current)] = misplaced_boxes(current)
            #H[str(current)] = bfs_distance(current)
            #H[str(current)] = improved_sokoban_heuristic(current)
        best_cost = float("inf")
        best_successor = None
        best_action = None

        # Generez mutările valabile
        for move in current.filter_possible_moves():
            succ = current.copy()
            succ.apply_move(move)

            key = str(succ)
            if key not in H:
                H[key] = manhattan_heuristic(succ)
                #H[key] = misplaced_boxes(succ)
                #H[key] = bfs_distance(succ)
                #H[key] = improved_sokoban_heuristic(succ)
            cost = 1 + H[key]          # c(n, a) = 1 + h(succesor)
            if cost < best_cost:
                best_cost = cost
                best_successor = succ
                best_action = move

        # Actualizez estimarea pentru starea curentă
        H[str(current)] = best_cost

        # Avansez
        path.append(best_action)
        current = best_successor

    return path
