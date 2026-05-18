from typing import Dict, List, Literal
from pydantic import BaseModel, Field, validator


class Zone(BaseModel):
    name: str
    x: int
    y: int
    zone_type: Literal["normal", "blocked",
                       "restricted", "priority"] = "normal"
    max_drones: int = Field(default=1, gt=0)
    color: str = "Gray"
    neighbors: List[str] = []
    current_drones: int = Field(default=0, gt=-1)

    @validator("name")
    def validate_name(cls, v: str) -> str:
        if "-" in v or " " in v:
            raise ValueError("Zone name cannot contain dash or space")
        return v


class Connection(BaseModel):
    zone1: str
    zone2: str
    max_link_capacity: int = Field(default=1, gt=0)
    current_drones: int = Field(default=0, gt=-1)
    coming_drones: int = 0

    @validator("zone1", "zone2")
    def validate_zone_name(cls, v: str) -> str:
        if "-" in v or " " in v:
            raise ValueError("Zone name cannot contain dash or space")
        return v


class Graph(BaseModel):
    nb_drones: int = Field(gt=0)
    zones: Dict[str, Zone] = {}
    connections: List[Connection] = []
    start: str = "None"
    end: str = "None"


class Drone:
    def __init__(self, id: int, zone: str) -> None:
        self.id = id
        self.zone = zone
        self.waiting = False
        self.source = zone
        self.finished = False
        self.visited = [zone]

    def get_connection(self, graph: Graph, z1: str, z2: str) -> Connection:
        for c in graph.connections:
            if (c.zone1 == z1 and c.zone2 == z2):
                return c
            if (c.zone1 == z2 and c.zone2 == z1):
                return c
        return c

    def move_drone(self, graph: Graph, target_name: str) -> str:
        old_zone = graph.zones[self.zone]
        new_zone = graph.zones[target_name]
        conn = self.get_connection(graph, self.zone, target_name)
        dest = target_name

        if new_zone.zone_type == "restricted":
            self.waiting = True
            self.source = self.zone
            conn.coming_drones += 1
            dest = f"({old_zone.name}-{target_name})"

        if self.zone != graph.start:
            old_zone.current_drones -= 1

        if target_name != graph.end:
            new_zone.current_drones += 1

        conn.current_drones += 1
        self.zone = target_name
        self.visited.append(target_name)

        if target_name == graph.end:
            self.finished = True

        return f"D{self.id}-{dest}"

    def arrive_drone(self, graph: Graph) -> str:
        self.waiting = False
        conn = self.get_connection(graph, self.source, self.zone)
        conn.coming_drones -= 1
        return f"D{self.id}-{self.zone}"

    def shortest(self, nodes: list[str], dist: dict) -> float:
        minn = float('inf')
        for node in nodes:
            if dist.get(node, float('inf')) < minn:
                minn = dist[node]
        return minn
