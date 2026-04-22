from models import Zone, Connection, Graph


def parse_metadata(meta_str: str, is_hub: bool) -> dict:
    meta: dict[str, str] = {}

    if not meta_str:
        return meta

    meta_str = meta_str.strip()[1:-1]
    parts = meta_str.split()

    allowed_keys = ["zone", "color", "max_drones"]
    if not is_hub:
        allowed_keys = ["max_link_capacity"]

    for part in parts:
        if "=" not in part:
            raise ValueError(f"Invalid metadata format [{meta_str}]")

        key, value = part.split("=")

        if key not in allowed_keys:
            raise ValueError(f"Invalid metadata key '{key}'")

        meta[key] = value

    return meta


def parse_zone_line(line: str) -> Zone:

    parts = line.split()

    if len(parts) < 3:
        raise ValueError("Zone definition requires name x y")

    name = parts[0]

    try:
        x = int(parts[1])
        y = int(parts[2])
    except ValueError:
        raise ValueError("Coordinates must be integers")

    meta_str = " ".join(parts[3:]) if len(parts) > 3 else ""
    meta = parse_metadata(meta_str, True) if meta_str else {}

    return Zone(
        name=name,
        x=x,
        y=y,
        zone_type=meta.get("zone", "normal"),
        max_drones=int(meta.get("max_drones", 1)),
        color=meta.get("color")
    )


def parse_con_line(line: str) -> Connection:

    if "[" in line:
        main, meta_str = line.split("[", 1)
        meta_str = "[" + meta_str
    else:
        main = line
        meta_str = ""

    if "-" not in main:
        raise ValueError("Connection must use format zone1-zone2")

    z1, z2 = main.strip().split("-")

    meta = parse_metadata(meta_str, False) if meta_str else {}

    return Connection(
        zone1=z1,
        zone2=z2,
        max_link_capacity=int(meta.get("max_link_capacity", 1))
    )


def parse_file(filepath: str) -> Graph:

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f
                 if line.strip() and not line.startswith("#")]

    if not lines:
        raise ValueError("Empty file")

    if not lines[0].startswith("nb_drones:"):
        raise ValueError("First line must define nb_drones")

    try:
        nb_drones = int(lines[0].split(":")[1].strip())
    except Exception:
        raise ValueError("Invalid nb_drones format")

    graph = Graph(nb_drones=nb_drones)

    seen_connections = set()

    for line_num, line in enumerate(lines[1:], 2):

        try:

            if line.startswith("start_hub:"):

                if graph.start != "None":
                    raise ValueError("start_hub defined multiple times")

                zone = parse_zone_line(line.replace("start_hub:", "").strip())

                if zone.name in graph.zones:
                    raise ValueError("Duplicate zone")

                graph.start = zone.name
                graph.zones[zone.name] = zone

            elif line.startswith("end_hub:"):

                if graph.end != "None":
                    raise ValueError("end_hub defined multiple times")

                zone = parse_zone_line(line.replace("end_hub:", "").strip())

                if zone.name in graph.zones:
                    raise ValueError("Duplicate zone")

                graph.end = zone.name
                graph.zones[zone.name] = zone

            elif line.startswith("hub:"):

                zone = parse_zone_line(line.replace("hub:", "").strip())

                if zone.name in graph.zones:
                    raise ValueError("Duplicate zone")

                graph.zones[zone.name] = zone

            elif line.startswith("connection:"):

                conn = parse_con_line(line.replace("connection:", "").strip())

                key = tuple(sorted([conn.zone1, conn.zone2]))

                if key in seen_connections:
                    raise ValueError("Duplicate connection")

                seen_connections.add(key)

                graph.connections.append(conn)

            else:
                raise ValueError("Unknown line type")

        except Exception as e:
            raise ValueError(f"Error at line {line_num}: {line}\n{e}")

    if graph.start == "None":
        raise ValueError("Missing start_hub")

    if graph.end == "None":
        raise ValueError("Missing end_hub")

    for conn in graph.connections:

        if conn.zone1 not in graph.zones or conn.zone2 not in graph.zones:
            raise ValueError(
                f"Connection references unknown zone {conn.zone1}-{conn.zone2}"
            )
        graph.zones[conn.zone1].neighbors.append(conn.zone2)
        graph.zones[conn.zone2].neighbors.append(conn.zone1)
    return graph
