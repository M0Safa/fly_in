from parsing import parse
from models import Drone
from utils import utils
from my_arcade import DroneVisualizer
import arcade
import sys



def main() -> None:
    par = parse()
    ut = utils()
    try:
        if len(sys.argv) != 2:
            raise ValueError("Error: plz enter only the map path")
        graph = par.parse_file(f"{sys.argv[1]}")
        if not ut.path_exists(graph, [], graph.start):
            raise ValueError("your graph does not have a valid path")
    except Exception as e:
        print(e)
        return
    distances = ut.dijkstra(graph)

    drones = [Drone(i + 1, graph.start) for i in range(graph.nb_drones)]
    turn = 1
    while not ut.finished(drones):
        turn_moves = []
        for d in drones:
            if d.finished:
                d.visited.append("wait")
                continue
            if d.waiting:
                move_str = d.arrive_drone(graph)
                turn_moves.append(move_str)
                d.visited.append("wait")
                continue
            current_zone = graph.zones[d.zone]
            best_neighbor = None
            shortest_dist = d.shortest(current_zone.neighbors, distances)
            if graph.end in current_zone.neighbors:
                best_neighbor = graph.end
            else:
                for n_name in current_zone.neighbors:
                    target = graph.zones[n_name]
                    if target.zone_type == "blocked" or n_name in d.visited:
                        continue
                    conn = d.get_connection(graph, d.zone, n_name)
                    if target.current_drones < target.max_drones:
                        if conn.current_drones < conn.max_link_capacity:
                            if distances[n_name] - shortest_dist > 4:
                                continue
                            if ut.path_exists(graph, d.visited, n_name):
                                best_neighbor = n_name
                                break
                            else:
                                continue

            if best_neighbor:
                move_str = d.move_drone(graph, best_neighbor)
                turn_moves.append(move_str)
            else:
                d.visited.append("wait")
        if turn_moves:
            print(turn, " ".join(turn_moves))
        for conn in graph.connections:
            conn.current_drones = conn.coming_drones
        turn += 1
    paths = {d.id: d.visited for d in drones}
    DroneVisualizer(graph, paths)
    arcade.run()


if __name__ == "__main__":
    main()
