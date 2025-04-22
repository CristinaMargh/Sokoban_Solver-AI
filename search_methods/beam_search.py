import random
import time

from collections import deque

def bfs_distance(state):
    """
    Estimează costul pe baza celei mai scurte distanțe reale (nu doar Manhattan)
    de la fiecare cutie la un target, ignorând alte cutii dar ținând cont de obstacole.
    Returnează suma acestor distanțe.
    """
    goals = list(state.targets)
    boxes = list(state.positions_of_boxes.keys())
    walls = set(state.obstacles)

    # BFS pentru fiecare cutie până la cel mai apropiat target
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

        return float('inf')  # dacă nu e drum

    total = 0
    for box in boxes:
        total += bfs(box)

    return total


def manhattan_heuristic_basic(state):
    """
    ∑ distanțe Manhattan de la fiecare cutie la cel mai apropiat target.
    Nu ignoră cutiile deja plasate, nici nu include poziția playerului.
    """
    goals = list(state.targets)
    boxes = list(state.positions_of_boxes.keys())
    free_goals = goals.copy()

    h = 0
    for b in boxes:
        dists = [abs(b[0]-g[0]) + abs(b[1]-g[1]) for g in free_goals]
        if not dists:
            continue
        best = min(dists)
        h += best
        free_goals.pop(dists.index(best))   # scoate goal-ul folosit

    return h

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


#  BEAM SEARCH  — doar cu listă
def beam_search_solver(start_map, beam_width = 50, timeout = None,
                       restart_after = None):
    """
    Beam‑Search:
        beam_width      – câte stări păstrăm la fiecare nivel
        timeout         – secunde limite pt. un run (None = infinit)
        restart_after   – dupa cate niveluri fara progres, cu h constant facem restart
    Returnează: listă de instanțe Map (drumul)
    """  
    t0 = time.time() # folosit pentru timeout
    best_global_path = None # solutia finala daca e gasita
    stagnation_lvl   = 0 # numara cate niveluri consecutive h nu avem imbunatatiri pentru restart

    while True:  # posibil mai multe restart‑uri daca euristica nu mai scade
        # pastreaza starile candidate de explorat pe nivelul curent
        current_gen = [(start_map.copy(), [])]     # stare initiala si drum gol
        visited = {str(start_map)} # pentru a evita reexplorarile
        # euristica celei mai bune stari de pana acum pentru verificarea stagnarii
        # best_h = manhattan_heuristic_improved(start_map)
        # best_h = bfs_distance(start_map)
        best_h = manhattan_heuristic_basic(start_map)
        level = 0 # adancimea curenta, cate mutari s-au facut de la start

        while current_gen:

            #Verifică dacă timpul maxim permis a fost depășit. Dacă da, întoarce cea mai bună soluție găsită (sau None).
            if timeout is not None and time.time() - t0 > timeout:
                print("Beam Search: timeout.")
                return best_global_path

            # ---- extindere un nivel ----
            next_gen = []
            for state, path in current_gen:
                # intoarce drumul complet pana acolo
                if state.is_solved():
                    print(f"Soluție găsită la nivel {level}  (lungime {len(path)})")
                    return path + [state]

                for succ in state.get_neighbours():          # toate starile care se pot obtine printr o miscare valida
                    key = str(succ)
                    if key in visited:
                        continue
                    visited.add(key)
                    next_gen.append((succ, path + [state]))  # adaug starea curentă în path

            if not next_gen:   # blocaj
                break

            # sortăm după f = g + h
            # pr[0] starea Map curenta si pr[1] este lista cu drumul parcurs pana la acea stare

            # next_gen.sort(key=lambda pr: len(pr[1]) + manhattan_heuristic_improved(pr[0]))
            # best_h_next = manhattan_heuristic_improved(next_gen[0][0])

            # next_gen.sort(key=lambda pr: len(pr[1]) + bfs_distance(pr[0]))
            # best_h_next = bfs_distance(next_gen[0][0])

            next_gen.sort(key=lambda pr: len(pr[1]) + manhattan_heuristic_basic(pr[0]))
            best_h_next = manhattan_heuristic_basic(next_gen[0][0])

            # verific stagnarea euristicii, adica dupa h, g - cat am mers deja care creste oricum la fiecare nivel
            # h este cat mai avem pana la solutie, vrem sa scada
            if best_h_next < best_h:
                best_h = best_h_next
                stagnation_lvl = 0
            else:
                stagnation_lvl += 1

            # păstrăm doar beam_width cei mai buni
            current_gen = next_gen[:beam_width]
            level += 1

            # ---- restart dacă stagnăm prea mult ----
            if restart_after is not None and stagnation_lvl >= restart_after:
                break   # ieșim din while current_gen pentru restart

        # -------- Dacă am ieșit fără soluție --------
        if restart_after is None:
            print("Beam Search nu a găsit soluție.")
            return best_global_path

