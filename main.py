from sokoban import Map
from search_methods.lrta_star import lrta_star_solver
from search_methods.beam_search import beam_search_solver
from sokoban.gif import save_images, create_gif
import time

if __name__ == "__main__":
    crt_map = Map.from_yaml("tests/medium_map2.yaml")
    print("=== Harta inițială ===")
    print(crt_map)
    print("Rezolvată deja?:", crt_map.is_solved())

    #RULARE  BEAM  SEARCH
    print("\n=== RULEZ BEAM SEARCH ===")
    start_time = time.time()
    path_states = beam_search_solver(
        crt_map,
        beam_width = 60,      
        timeout = 300,         # secunde maximale (None = nelimitat)
        restart_after = 25    # niveluri fara proges inainte de restart
    )

    end_time = time.time()
    duration = end_time - start_time

    print(f"Runtime: {duration:.3f} secunde")

    # save_images(path_states, save_path="output/images")
    # create_gif("output/images", "beam_search_path", save_path="output/gifs")

    if path_states:
        print(f"\nSoluție găsită: {len(path_states)-1} niveluri")
        # print("Afișez harta după fiecare nivel:\n")
        # for idx, st in enumerate(path_states):
        #     print(f"--- nivel {idx} ---")
        #     print(st)
        print("Rezolvat?:", path_states[-1].is_solved())
        print("Număr de mutări de tip pull:", path_states[-1].undo_moves)
    else:
        print("Beam Search nu a găsit soluție în condițiile date.")


    # ==========================================================
#                RULARE  LRTA*
# ==========================================================
    print("\n=== RULEZ LRTA* ===")

    start_map_lrta = Map.from_yaml("tests/easy_map2.yaml")
    start_time = time.time()

    moves_lrta = lrta_star_solver(start_map_lrta)              # listă de mutări

    end_time = time.time()
    duration = end_time - start_time
    print(f"Runtime LRTA*: {duration:.3f} secunde")

    if moves_lrta:
        print("Număr mutări LRTA*:", len(moves_lrta))

        for i, mv in enumerate(moves_lrta, 1):
            start_map_lrta.apply_move(mv)      # mut harta pe loc
            # print(f"\n--- După mutarea {i} ({mv}) ---")
            # print(start_map_lrta)

        print("Rezolvat după LRTA*?:", start_map_lrta.is_solved())
        print("Număr de mutări de tip pull:", start_map_lrta.undo_moves)
    else:
        print("LRTA* nu a găsit nicio secvență de mutări.")
