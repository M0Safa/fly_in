import heapq

class drone:
    def __init__(self, id: int, zone: str):
        self.id = id
        self.zone = zone
        self.waiting = False
        self.source = zone
        self.finished = False
        self.visited = [zone]


def zone_cost(zone):
    if zone.zone_type == "restricted":
        return 2
    return 1


def dijkstra(graph):

    distances = {}

    for zone in graph.zones:
        distances[zone] = float("inf")

    end = graph.end
    distances[end] = 0

    pq = []
    heapq.heappush(pq, (0, end))
    while pq:

        current_cost, node = heapq.heappop(pq)
        for neighbor in graph.zones[node].neighbors:
            zone = graph.zones[neighbor]
            if zone.zone_type == "blocked":
                continue
            new_cost = current_cost + zone_cost(zone)
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))
    for zone in graph.zones.values():
        zone.neighbors.sort(key=lambda n: (
            0 if graph.zones[n].zone_type == "priority" else 1, 
            distances.get(n, float('inf'))
        ))
    return distances

    
