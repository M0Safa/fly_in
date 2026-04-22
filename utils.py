import heapq
from models import Zone, Graph


def zone_cost(zone: Zone) -> int:
    if zone.zone_type == "restricted":
        return 2
    return 1


def dijkstra(graph: Graph) -> dict:

    distances: dict[str, float] = {}

    for z in graph.zones:
        distances[z] = float("inf")

    end: str = graph.end
    distances[end] = 0

    pq: list[tuple[int, str]] = []
    heapq.heappush(pq, (0, end))
    while pq:

        current_cost, node = heapq.heappop(pq)
        for neighbor in graph.zones[node].neighbors:
            zone: Zone = graph.zones[neighbor]
            if zone.zone_type == "blocked":
                continue
            new_cost = current_cost + zone_cost(zone)
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))
    for zon in graph.zones.values():
        zon.neighbors.sort(key=lambda n: (
            0 if graph.zones[n].zone_type == "priority" else 1,
            distances.get(n, float('inf'))
        ))
    return distances


def path_exists(graph: Graph, visited_n: list, start: str) -> bool:
    visited = visited_n.copy()
    queue = [start]

    while queue:
        zone = queue.pop(0)

        if zone == graph.end:
            return True

        for n in graph.zones[zone].neighbors:
            if n not in visited and graph.zones[n].zone_type != "blocked":
                visited.append(n)
                queue.append(n)

    return False
