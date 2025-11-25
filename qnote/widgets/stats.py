import asyncio
from datetime import datetime
from random import choice, randint

from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalGroup, Vertical
from textual.reactive import reactive
from textual.widgets import Label, Static


class Stats(Static, can_focus=False):
    """Stats and Visuals."""

    wordcount = Static()
    created = Static()
    updated = Static()
    age = Static()
    lumen = Static(id="lumen")

    note_id = reactive(None)
    lumen_active = reactive(True, bindings=True)
    _rain_task = None

    rain_chars = list("abcdefgmnopxyz0123456789-)(;@#~óśćźż")


    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical():
                with HorizontalGroup():
                    yield Label("Created on: ")
                    yield self.created
                with HorizontalGroup():
                    yield Label("Updated on: ")
                    yield self.updated
                with HorizontalGroup():
                    yield Label("Wordcount: ")
                    yield self.wordcount
                with HorizontalGroup():
                    yield Label("Age: ")
                    yield self.age
            with Vertical():
                with HorizontalGroup():
                    yield self.lumen


    async def matrix_rain(
        self,
        width: int = 65,
        height: int = 10,
        min_speed: float = 0.03,
        max_speed: float = 0.12,
        density: float = 0.2,
    ):
        """
        Matrix letter rain simulation.

        width     = number of columns
        height    = number of rows
        density   = probability of new droplets appearing
        min_speed = fastest column delay
        max_speed = slowest column delay
        """

        columns = [
            {
                "pos": randint(-height, 0),  # start above screen
                "speed": (randint(int(min_speed * 100), int(max_speed * 100)) / 100),
            }
            for _ in range(width)
        ]

        screen = [[" " for _ in range(width)] for _ in range(height)]

        while True:
            # Clear frame
            for row in range(height):
                for col in range(width):
                    screen[row][col] = " "

            # Update each column
            for col_idx, col in enumerate(columns):
                if col["pos"] < 0 and randint(0, 100) / 100 > density:
                    continue

                col["pos"] += 1  # fall

                # Loop to top when reaching bottom
                if col["pos"] >= height + 5:
                    col["pos"] = randint(-height, 0)
                    col["speed"] = (
                        randint(int(min_speed * 100), int(max_speed * 100)) / 100
                    )

                # Render head (bright)
                if 0 <= col["pos"] < height:
                    screen[col["pos"]][col_idx] = f"[b]{choice(self.rain_chars)}[/b]"

                # Render fading trail (past 4 chars)
                for fade_offset, style in [
                    (1, "#b85727"),
                    (2, "#994b22"),
                    (3, "#80381b"),
                    (4, "#6a2a15"),
                ]:
                    y = col["pos"] - fade_offset
                    if 0 <= y < height:
                        if randint(0, 4) == 0:  # random "shimmer"
                            char = choice(self.rain_chars)
                        else:
                            char = self.rain_chars[(col_idx + y) % len(self.rain_chars)]
                        screen[y][col_idx] = f"[{style}]{char}[/{style}]"

            out = "\n".join("".join(row) for row in screen)
            self.lumen.update(out)

            await asyncio.sleep(0.15)


    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data["id"]
            self.wordcount.content = str(len(data["content"].split()))
            self.created.content = str(data["created"])
            self.updated.content = str(data["updated"])
            self.age.content = str(datetime.now() - data["created"])
        except TypeError:
            pass
            # TODO: logging


    def on_mount(self) -> None:
        self.border_title = "Stats"
        self.disabled = True
        self._rain_task = asyncio.create_task(self.matrix_rain())


    def on_unmount(self):
        if self._rain_task:
            self._rain_task.cancel()
