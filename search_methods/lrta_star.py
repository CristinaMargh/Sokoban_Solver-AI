from queue import PriorityQueue

def manhattan_heuristic(state):
    """
    Calculează suma celor mai mici distanțe Manhattan între cutii și ținte.
    """
    total = 0
    box_positions = list(state.positions_of_boxes.keys())  # [(x, y), ...]
    goals = list(state.targets)

    remaining_goals = goals.copy()
    for box in box_positions:
        dists = [abs(box[0] - g[0]) + abs(box[1] - g[1]) for g in remaining_goals]
        min_dist = min(dists)
        total += min_dist
        remaining_goals.pop(dists.index(min_dist))

    return total

def lrta_star_solver(start_map):
    H = {}
    current = start_map.copy()
    path = []
    visited = set()

    while not current.is_solved():
        visited.add(current)

        if current not in H:
            H[current] = manhattan_heuristic(current)

        min_cost = float('inf')
        best_successor = None
        best_action = None

        for succ in current.get_neighbours():  # succ = Map (already copied)
            if succ not in H:
                H[succ] = manhattan_heuristic(succ)

            cost = 1 + H[succ]
            if cost < min_cost:
                min_cost = cost
                best_successor = succ

        H[current] = min_cost
        current = best_successor
        path.append("step")  # opțional, poți salva și acțiunea dacă `get_neighbours()` le returnează

    return path