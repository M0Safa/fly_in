import arcade
import math
import time
from models import Graph


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Self-Scaling Drone Animation"
PADDING = 100
DRONE_SPEED = 6
NODE_RADIUS = 15


class Drone_Sprite(arcade.Sprite):
    def __init__(self, drone_id: int, pixel_path: list) -> None:
        super().__init__()
        self.state = "moving"
        self.drone_id = drone_id
        self.path = pixel_path
        self.target_idx = 1

        if self.path:
            self.center_x, self.center_y = self.path[0]

        self.texture = arcade.make_soft_circle_texture(20, arcade.color.CYAN)

    def update(self, delta_time: float) -> None:  # type: ignore[override]
        if self.state == "waiting":
            return
        if self.target_idx < len(self.path):
            if self.path[self.target_idx] == "wait":
                self.state = "waiting"
                return
            else:
                dest_x, dest_y = self.path[self.target_idx]

            diff_x = dest_x - self.center_x
            diff_y = dest_y - self.center_y
            distance = math.sqrt(diff_x**2 + diff_y**2)

            if distance <= DRONE_SPEED:
                self.center_x, self.center_y = dest_x, dest_y
                self.state = "waiting"
            else:
                self.center_x += (diff_x / distance) * DRONE_SPEED
                self.center_y += (diff_y / distance) * DRONE_SPEED


class DroneVisualizer(arcade.Window):
    def __init__(self, graph: Graph, drone_paths: dict[int, list]) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.graph = graph
        self.drone_list: arcade.SpriteList[Drone_Sprite] = arcade.SpriteList()

        all_x = [z.x for z in graph.zones.values()]
        all_y = [z.y for z in graph.zones.values()]

        self.min_x, self.max_x = min(all_x), max(all_x)
        self.min_y, self.max_y = min(all_y), max(all_y)

        range_x = (self.max_x - self.min_x) if self.max_x != self.min_x else 1
        range_y = (self.max_y - self.min_y) if self.max_y != self.min_y else 1

        self.scale_x = (SCREEN_WIDTH - (2 * PADDING)) / range_x
        self.scale_y = (SCREEN_HEIGHT - (2 * PADDING)) / range_y

        for d_id, path_names in drone_paths.items():
            pixel_path = ["wait" if name == "wait" else
                          self.get_pixel_coords(name) for name in path_names]
            self.drone_list.append(Drone_Sprite(d_id, pixel_path))

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def get_pixel_coords(self, zone_name: str) -> tuple[float, float]:
        zone = self.graph.zones[zone_name]
        px = (zone.x - self.min_x) * self.scale_x + PADDING
        py = (zone.y - self.min_y) * self.scale_y + PADDING
        return px, py

    def on_draw(self) -> None:
        self.clear()

        for conn in self.graph.connections:
            start_p = self.get_pixel_coords(conn.zone1)
            end_p = self.get_pixel_coords(conn.zone2)
            arcade.draw_line(start_p[0], start_p[1], end_p[0],
                             end_p[1], arcade.color.GRAY, 2)

        for name, zone in self.graph.zones.items():
            px, py = self.get_pixel_coords(name)

            color = arcade.color.DARK_BLUE_GRAY
            if zone.zone_type == "restricted":
                color = arcade.color.RED_DEVIL
            elif zone.zone_type == "priority":
                color = arcade.color.GOLD

            arcade.draw_circle_filled(px, py, NODE_RADIUS, color)
            arcade.draw_text(name, px, py - 30, arcade.color.WHITE,
                             10, anchor_x="center")

        self.drone_list.draw()
        for drone in self.drone_list:
            arcade.draw_text(f"D{drone.drone_id}", drone.center_x,
                             drone.center_y + 25, arcade.color.CYAN,
                             10, anchor_x="center", bold=True)

    def on_update(self, delta_time: float) -> None:
        finished = True
        for d in self.drone_list:
            if d.state == "moving":
                finished = False
        if finished:
            time.sleep(0.3)
            for d in self.drone_list:
                d.state = "moving"
                d.target_idx += 1
        self.drone_list.update(delta_time)
