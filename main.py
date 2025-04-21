from sokoban import Map
from search_methods.lrta_star import lrta_star_solver
from search_methods.beam_search import beam_search_solver

if __name__ == "__main__":
    crt_map = Map.from_yaml("tests/easy_map1.yaml")
    print("=== Harta inițială ===")
    print(crt_map)
    print("Rezolvată deja?:", crt_map.is_solved())

    #RULARE  BEAM  SEARCH
    print("\n=== RULEZ BEAM SEARCH ===")
    path_states = beam_search_solver(
        crt_map,
        beam_width=60,      
        timeout=30,         # secunde maximale (None = nelimitat)
        restart_after=25    # niveluri fara proges inainte de restart
    )

    if path_states:
        print(f"\nSoluție găsită: {len(path_states)-1} niveluri")
        print("Afișez harta după fiecare nivel:\n")
        for idx, st in enumerate(path_states):
            print(f"--- nivel {idx} ---")
            print(st)
        print("Rezolvat?:", path_states[-1].is_solved())
    else:
        print("Beam Search nu a găsit soluție în condițiile date.")


    # ==========================================================
    #                RULARE  LRTA*   (opțional)
    # ==========================================================
    # crt_lrta = crt_map.copy()
    # print("\n=== RULEZ LRTA* ===")
    # solution_lrta = lrta_star_solver(crt_lrta)
    # print("Lungime soluție LRTA*:", len(solution_lrta))
    # for move in solution_lrta:
    #     crt_lrta.move(move)
    # print("Rezolvat după LRTA*?:", crt_lrta.is_solved())
