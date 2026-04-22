from parsing import parse_file
from models import Connection, Graph, Drone
from utils import dijkstra, path_exists
from my_arcade import DroneVisualizer
import arcade
import sys


def finished(drones: list[Drone]) -> bool:
    for drone in drones:
        if not drone.finished:
            return False
    return True


def get_connection(graph: Graph, z1: str, z2: str) -> Connection:
    for c in graph.connections:
        if (c.zone1 == z1 and c.zone2 == z2):
            return c
        if (c.zone1 == z2 and c.zone2 == z1):
            return c
    return c


def move_drone(graph: Graph, drone: Drone, target_name: str) -> str:
    old_zone = graph.zones[drone.zone]
    new_zone = graph.zones[target_name]
    conn = get_connection(graph, drone.zone, target_name)
    dest = target_name

    if new_zone.zone_type == "restricted":
        drone.waiting = True
        drone.source = drone.zone
        conn.coming_drones += 1
        dest = f"({old_zone.name}-{target_name})"

    if drone.zone != graph.start:
        old_zone.current_drones -= 1

    if target_name != graph.end:
        new_zone.current_drones += 1

    conn.current_drones += 1
    drone.zone = target_name
    drone.visited.append(target_name)

    if target_name == graph.end:
        drone.finished = True

    return f"D{drone.id}-{dest}"


def arrive_drone(graph: Graph, drone: Drone) -> str:
    drone.waiting = False
    conn = get_connection(graph, drone.source, drone.zone)
    conn.coming_drones -= 1
    return f"D{drone.id}-{drone.zone}"


def shortest(nodes: list[str], dist: dict) -> float:
    minn = float('inf')
    for node in nodes:
        if dist.get(node, float('inf')) < minn:
            minn = dist[node]
    return minn


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise ValueError("Error: plz enter only the map path")
        graph = parse_file(f"{sys.argv[1]}")
        if not path_exists(graph, [], graph.start):
            raise ValueError("your graph does not have a valid path")
    except Exception as e:
        print(e)
        return
    distances = dijkstra(graph)

    drones = [Drone(i + 1, graph.start) for i in range(graph.nb_drones)]
    turn = 1
    while not finished(drones):
        turn_moves = []
        for d in drones:
            if d.finished:
                d.visited.append("wait")
                continue
            if d.waiting:
                move_str = arrive_drone(graph, d)
                turn_moves.append(move_str)
                d.visited.append("wait")
                continue
            current_zone = graph.zones[d.zone]
            best_neighbor = None
            shortest_dist = shortest(current_zone.neighbors, distances)
            if graph.end in current_zone.neighbors:
                best_neighbor = graph.end
            else:
                for n_name in current_zone.neighbors:
                    target = graph.zones[n_name]
                    if target.zone_type == "blocked" or n_name in d.visited:
                        continue
                    conn = get_connection(graph, d.zone, n_name)
                    if target.current_drones < target.max_drones:
                        if conn.current_drones < conn.max_link_capacity:
                            if target.zone_type != "priority":
                                if distances[n_name] - shortest_dist > 5:
                                    continue
                            if path_exists(graph, d.visited, n_name):
                                best_neighbor = n_name
                                break
                            else:
                                continue

            if best_neighbor:
                move_str = move_drone(graph, d, best_neighbor)
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
