# lrta_star.py
from typing import List
from sokoban.moves import *   # pentru constantele LEFT, RIGHT, BOX_LEFT, ...

# ---------------------------------------------------------------
#  EURISTICĂ Manhattan simplă (fără player)
# ---------------------------------------------------------------
def manhattan_heuristic(state) -> int:
    """
    Suma distanţelor Manhattan de la fiecare cutie la cel mai apropiat target.
    """
    total = 0
    goals = list(state.targets)
    boxes = list(state.positions_of_boxes.keys())
    remaining_goals = goals.copy()

    for box in boxes:
        dists = [abs(box[0] - g[0]) + abs(box[1] - g[1]) for g in remaining_goals]
        best = min(dists)
        total += best
        remaining_goals.pop(dists.index(best))  # elimin ţinta folosită

    return total


# ---------------------------------------------------------------
#  LRTA* care întoarce LISTA DE MUTĂRI reale
# ---------------------------------------------------------------
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
