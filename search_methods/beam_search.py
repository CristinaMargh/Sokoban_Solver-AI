import random
import time

from collections import deque
from search_methods.heuristics import misplaced_boxes
from search_methods.heuristics import bfs_distance
from search_methods.heuristics import manhattan_heuristic
from search_methods.heuristics import manhattan_heuristic_improved

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
        best_h = manhattan_heuristic_improved(start_map)
        #best_h = bfs_distance(start_map)
        #best_h = manhattan_heuristic(start_map)
        #best_h = misplaced_boxes(start_map)
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

            next_gen.sort(key=lambda pr: len(pr[1]) + manhattan_heuristic_improved(pr[0]))
            best_h_next = manhattan_heuristic_improved(next_gen[0][0])

            # next_gen.sort(key=lambda pr: len(pr[1]) + bfs_distance(pr[0]))
            # best_h_next = bfs_distance(next_gen[0][0])

            # next_gen.sort(key=lambda pr: len(pr[1]) + manhattan_heuristic(pr[0]))
            # best_h_next = manhattan_heuristic(next_gen[0][0])

            # next_gen.sort(key=lambda pr: len(pr[1]) + misplaced_boxes(pr[0]))
            # best_h_next = misplaced_boxes(next_gen[0][0])

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

