import asyncio
from random import choice, randint

from textual.widgets import Static


class Lumen(Static, can_focus=False):
    """Animation display widget."""

    current_worker = None

    rain_chars = list("abcdefghijklmnopqrstuvwxyz0123456789-)(;@#~óśćźż")

    async def on_mount(self):
        self.play_animation("qnote")

    def on_unmount(self):
        if self.current_worker:
            self.current_worker.cancel()

    # ---------------------------------------------------------
    # Animation switching API
    # ---------------------------------------------------------

    def play_animation(self, name: str):
        """Switch to a different animation by name."""

        # Cancel current animation if any
        if self.current_worker:
            self.current_worker.cancel()
            self.current_worker = None

        animations = {
            "qnote": self.qnote_animation,
            "pulse": self.pulse_animation,
            "waves": self.wave_animation,
            "snake": self.snake_animation,
            "none": self.no_animation
        }

        coro = animations.get(name, self.qnote_animation)
        if not coro:
            self.update(f"[red]Unknown animation: {name}")
            return

        # Start worker
        self.current_worker = self.run_worker(
            coro(),
            exclusive=True,
            name=name,
        )


    # No Animation
    async def no_animation(self):
        """Simple placeholder animation."""
        self.update(f"[orange]QNote Static Logo")
        # TODO: a static QNote logo


    # Lumen Animation 1 — Letter Rain (Standard QNote)
    async def qnote_animation(
        self,
        width: int = 65,
        height: int = 10,
        min_speed: float = 0.03,
        max_speed: float = 0.12,
        density: float = 0.2,
    ):
        """Matrix-style falling letters."""

        columns = [
            {
                "pos": randint(-height, 0),
                "speed": (randint(int(min_speed * 100), int(max_speed * 100)) / 100),
            }
            for _ in range(width)
        ]

        screen = [[" " for _ in range(width)] for _ in range(height)]

        while True:

            # Clear matrix
            for row in range(height):
                for col in range(width):
                    screen[row][col] = " "

            # Update columns
            for col_idx, col in enumerate(columns):
                if col["pos"] < 0 and randint(0, 100) / 100 > density:
                    continue

                col["pos"] += 1

                if col["pos"] >= height + 5:
                    col["pos"] = randint(-height, 0)
                    col["speed"] = (
                        randint(int(min_speed * 100), int(max_speed * 100)) / 100
                    )

                # Main falling character (bright)
                if 0 <= col["pos"] < height:
                    screen[col["pos"]][col_idx] = f"[b]{choice(self.rain_chars)}[/b]"

                # Fading tail
                for fade_offset, style in [
                    (1, "#b85727"),
                    (2, "#994b22"),
                    (3, "#80381b"),
                    (4, "#6a2a15"),
                ]:
                    y = col["pos"] - fade_offset
                    if 0 <= y < height:
                        char = choice(self.rain_chars) if randint(0, 4) == 0 else \
                               self.rain_chars[(col_idx + y) % len(self.rain_chars)]
                        screen[y][col_idx] = f"[{style}]{char}[/{style}]"

            # Output frame
            self.update("\n".join("".join(row) for row in screen))
            await asyncio.sleep(0.15)


    # Animation 2 — Placeholder Pulse
    async def pulse_animation(self, width: int = 65, height: int = 10):
        """Simple placeholder animation."""
        frame = 0
        screen = [[" " for _ in range(width)] for _ in range(height)]

        while True:
            match frame:
                case 1:
                    for row in range(height):
                        for col in range(width):
                            screen[row][col] = " "

                case 2:
                    for row in range(height):
                        for col in range(width):
                            if row == int(height/2)-1 and col == int(width/2):
                                screen[row][col] = "●"

                case 3:
                    centre = [int(height / 2) - 1, int(width / 2)]
                    for row in range(height):
                        for col in range(width):
                            if (row == centre[0]+1 or row == centre[0]-1) and (col == centre[1]+1 or col == centre[1]-1):
                                screen[row][col] = "●"

                case 4:
                    centre = [int(height / 2) - 1, int(width / 2)]
                    for row in range(height):
                        for col in range(width):
                            if (row == centre[0] + 2 or row == centre[0] - 2) and (
                                    col == centre[1] + 2 or col == centre[1] - 2):
                                screen[row][col] = "●"

                case 5:
                    frame = 0

            #self.update("[green]●[/green]" if visible else " ")


            self.update("\n".join("".join(row) for row in screen))
            frame += 1
            await asyncio.sleep(0.5)


    # Animation 3 — Placeholder Waves
    async def wave_animation(self):
        """Simple placeholder scrolling wave."""
        pattern = "~≈~≈~≈~≈~≈~≈"
        i = 0
        while True:
            self.update(pattern[i:] + pattern[:i])
            i = (i + 1) % len(pattern)
            await asyncio.sleep(0.3)

    # Animation 4 — Snake
    async def snake_animation(self, width: int = 65, height: int = 10, delay: float = 0.15, max_length: int = 99):
        """Autonomous snake game animation."""

        snake = [(width // 2, height // 2)]
        food = (randint(1, width - 2), randint(1, height - 2))
        length = 5

        while True:
            # Compute new head position
            head_x, head_y = snake[0]
            food_x, food_y = food
            new_head = snake[0]

            if head_x > food_x:  #TODO: avoid itself
                new_head = (head_x - 1, head_y)
            if head_x < food_x:
                new_head = (head_x + 1, head_y)
            if head_y > food_y:
                new_head = (head_x, head_y - 1)
            if head_y < food_y:
                new_head = (head_x, head_y + 1)

            # Add new head
            snake.insert(0, new_head)

            # If snake eats food
            if new_head == food and length < max_length:
                length += 1
                food = (randint(1, width - 2), randint(1, height - 2))
            if new_head == food and length == max_length:
                length = 5
                food = (randint(1, width - 2), randint(1, height - 2))
            else:
                snake = snake[:length]

            screen = [[" " for _ in range(width)] for _ in range(height)]
            fade_off = ["$accent", "$accent", "#b85727", "#994b22", "#80381b", "#6a2a15",]

            # Draw food
            fx, fy = food
            screen[fy][fx] = "[red]●[/red]"

            # Draw snake (head highlighted)
            for i, (x, y) in enumerate(snake):
                if i == 0:
                    screen[y][x] = f"[{fade_off[i]}]■[/{fade_off[i]}]"
                elif i == 1:
                    screen[y][x] = f"[{fade_off[i]}]■[/{fade_off[i]}]"
                elif i == 2 or i == 3:
                    screen[y][x] = f"[{fade_off[2]}]■[/{fade_off[2]}]"
                elif i == 4 or i == 5:
                    screen[y][x] = f"[{fade_off[3]}]■[/{fade_off[3]}]"
                elif i == 6 or i == 7:
                    screen[y][x] = f"[{fade_off[4]}]■[/{fade_off[4]}]"
                else:
                    screen[y][x] = f"[{fade_off[-1]}]■[/{fade_off[-1]}]"

            # Convert to text output
            out = "\n".join("".join(row) for row in screen)
            self.update(out)

            await asyncio.sleep(delay)
