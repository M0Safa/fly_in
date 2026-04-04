from parsing import parse_file, Zone, Connection, Graph
from distance import drone, dijkstra
from validation import path_exists


def finished(drones: list[drone]) -> bool:
    for drone in drones:
        if not drone.finished:
            return False
    return True


def get_connection(graph, z1, z2) -> Connection:
    """Finds the connection object between two zones[cite: 427]."""
    for c in graph.connections:
        if (c.zone1 == z1 and c.zone2 == z2) or (c.zone1 == z2 and c.zone2 == z1):
            return c
    return None

def move_drone(graph, drone, target_name) -> str:
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


def arrive_drone(graph, drone) -> str:
    drone.waiting = False
    conn = get_connection(graph, drone.source, drone.zone)
    conn.coming_drones -= 1
    return f"D{drone.id}-{drone.zone}"


def shortest(nodes: list[Zone], dist: dict) -> int:
    minn = float('inf')
    for node in nodes:
        if dist.get(node, float('inf')) < minn:
            minn = dist[node]
    return minn


def main():
    try:
        graph = parse_file("maps/easy/03_basic_capacity.txt")
        if not path_exists(graph, [], graph.start):
            raise ValueError("your graph does not have a valid path")
    except Exception as e:
        print(e)
        return
    distances = dijkstra(graph)
    
    drones = [drone(i + 1, graph.start) for i in range(graph.nb_drones)]
    turn = 1
    while not finished(drones):
        turn_moves = []
        for d in drones:
            if d.finished:
                continue
            if d.waiting:
                move_str = arrive_drone(graph, d)
                turn_moves.append(move_str)
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
                    if target.current_drones < target.max_drones or n_name == graph.end:
                        if conn.current_drones < conn.max_link_capacity:
                            if target.zone_type != "priority" and distances[n_name] - shortest_dist > 5:
                                continue
                            if path_exists(graph, d.visited, n_name):
                                best_neighbor = n_name
                                break
                            else:
                                d.visited.append(n_name)
            
            if best_neighbor:
                move_str = move_drone(graph, d, best_neighbor)
                turn_moves.append(move_str)
        if turn_moves:
            print(turn, " ".join(turn_moves))
        for conn in graph.connections:
            conn.current_drones = conn.coming_drones
        turn += 1

main()