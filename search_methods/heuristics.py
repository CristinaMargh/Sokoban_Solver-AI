from collections import deque

def misplaced_boxes(state):
    """
    Euristică: numărul de cutii care NU sunt pe targeturi.
    """
    return sum(1 for box in state.positions_of_boxes if box not in state.targets)

def bfs_distance(state, penalize_if_blocked=True, fallback_penalty=50):
    """
    Estimează suma celor mai scurte distanțe BFS de la cutii la targeturi.
    Parametri:
    - penalize_if_blocked: dacă este True, adaugă fallback_penalty dacă nu se poate ajunge la un target
    - fallback_penalty: penalizarea adăugată dacă o cutie nu poate ajunge la niciun target
    """
    goals = list(state.targets)
    boxes = list(state.positions_of_boxes.keys())
    walls = set(state.obstacles)

    def bfs(box):
        visited = set()
        queue = deque([(box, 0)])
        while queue:
            (x, y), dist = queue.popleft()
            if (x, y) in goals:
                return dist
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < state.length and 0 <= ny < state.width and
                    (nx, ny) not in visited and
                    (nx, ny) not in walls):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1))
        return fallback_penalty if penalize_if_blocked else float('inf')

    return sum(bfs(box) for box in boxes)

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
# pentru beam search

def manhattan_heuristic_improved(state):
    """
    Euristică pentru Sokoban:
    - Ignoră cutiile deja plasate pe target (nu le penalizează).
    - Calculează distanța Manhattan de la fiecare cutie rămasă la cel mai apropiat target liber.
    - Adaugă distanța playerului la cea mai apropiată cutie neplasată (pentru a favoriza începutul mutării).
    """
    boxes = list(state.positions_of_boxes.keys())
    goals = list(state.targets)
    player_pos = (state.player.x, state.player.y)

    movable_boxes = [b for b in boxes if b not in goals]
    free_goals = goals.copy()
    h = 0

    for box in movable_boxes:
        dists = [abs(box[0] - g[0]) + abs(box[1] - g[1]) for g in free_goals]
        if not dists:
            continue
        best = min(dists)
        h += best
        free_goals.pop(dists.index(best))  # rezervăm acel goal

    if movable_boxes:
        dist_player_to_box = min(abs(player_pos[0] - b[0]) + abs(player_pos[1] - b[1]) for b in movable_boxes)
        h += dist_player_to_box  # cât de departe e playerul de o cutie mutabilă

    return h
## folosita la lrta
def improved_sokoban_heuristic(state) -> int:
    """
    Heuristica personalizată pentru Sokoban:
    - distanțe BFS de la cutii neplasate la targeturi libere
    - distanța playerului la cea mai apropiată cutie utilă
    - penalizare pentru mișcări de tip "pull" (undo_moves)
    """
    boxes = list(state.positions_of_boxes.keys())
    goals = list(state.targets)
    player_pos = (state.player.x, state.player.y)
    movable_boxes = [b for b in boxes if b not in goals]
    free_goals = goals.copy()
    h = 0

    # 1. Distanța cutii → target (BFS)
    for box in movable_boxes:
        visited = set()
        queue = deque()
        queue.append((box[0], box[1], 0))
        found_goal = False

        while queue and not found_goal:
            x, y, dist = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))

            if (x, y) in free_goals:
                h += dist
                free_goals.remove((x, y))
                found_goal = True
                break

            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < state.length and 0 <= ny < state.width:
                    if state.map[nx][ny] != 1:  # nu e obstacol
                        queue.append((nx, ny, dist + 1))

        if not found_goal:
            h += 50  # penalizare dacă nu poate ajunge la un target

    # 2. Distanța player → cea mai apropiată cutie
    if movable_boxes:
        dist_player_to_box = min(abs(player_pos[0] - b[0]) + abs(player_pos[1] - b[1]) for b in movable_boxes)
        h += dist_player_to_box

    # 3. Penalizare pentru mișcări de tip "pull"
    h += 2 * state.undo_moves

    return h

