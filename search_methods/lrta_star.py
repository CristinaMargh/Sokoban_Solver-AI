# lrta_star.py
from typing import List
from collections import deque
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

def bfs_estimation_heuristic(state) -> int:
    """
    Pentru fiecare cutie, se estimează costul de mutare la cel mai apropiat target
    folosind distanțe BFS (nu neapărat Manhattan), ignorând alte cutii.
    """
    goals = list(state.targets)
    boxes = list(state.positions_of_boxes.keys())
    total_cost = 0

    for box in boxes:
        visited = set()
        queue = deque()
        queue.append((box[0], box[1], 0))  # (x, y, dist)

        found_goal = False
        while queue and not found_goal:
            x, y, dist = queue.popleft()

            if (x, y) in visited:
                continue
            visited.add((x, y))

            if (x, y) in goals:
                total_cost += dist
                found_goal = True
                continue

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < state.length and 0 <= ny < state.width:
                    if state.map[nx][ny] != 1:  # nu e obstacol
                        queue.append((nx, ny, dist + 1))

        if not found_goal:
            total_cost += 50  # penalizare dacă nu găsesc target (fallback)

    return total_cost

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
            #H[str(current)] = bfs_estimation_heuristic(current)
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
                #H[key] = bfs_estimation_heuristic(succ)
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
