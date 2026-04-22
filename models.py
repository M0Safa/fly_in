from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field, validator


class Zone(BaseModel):
    name: str
    x: int
    y: int
    zone_type: Literal["normal", "blocked",
                       "restricted", "priority"] = "normal"
    max_drones: int = Field(default=1, gt=0)
    color: Optional[str] = None
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
