def path_exists(graph, visited_n, start) -> bool:
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