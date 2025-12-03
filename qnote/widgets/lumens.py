import asyncio
from random import choice, randint, random

from textual.widgets import Static


class Lumen(Static, can_focus=False):
    """Animation display widget."""

    current_worker = None

    rain_chars = list("abcdefghijklmnopqrstuvwxyz0123456789-)(;@#~óśćźż")

    async def on_mount(self):
        self.play_animation("letter_rain")

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
            "letter_rain": self.letter_rain,
            "pulse": self.pulse_animation,
            "waves": self.wave_animation,
            "snake": self.snake_animation,
            "none": self.no_animation
        }

        coro = animations.get(name)
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
    async def letter_rain(
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
    async def pulse_animation(self):
        """Simple placeholder animation."""
        visible = True
        while True:
            self.update("[green]●[/green]" if visible else " ")
            visible = not visible
            await asyncio.sleep(0.5)


    # Animation 3 — Placeholder Waves
    async def wave_animation(self):
        """Simple placeholder scrolling wave."""
        pattern = "~≈~≈~≈~≈~≈~≈"
        i = 0
        while True:
            self.update(pattern[i:] + pattern[:i])
            i = (i + 1) % len(pattern)
            await asyncio.sleep(0.1)

    # Animation 4 — Placeholder Snake
    async def snake_animation(self, width: int = 65, height: int = 10, delay: float = 0.15):
        """Autonomous snake game animation (no user input)."""

        # Initial snake configuration
        snake = [(width // 2, height // 2)]
        direction = (1, 0)  # moving right
        food = (randint(0, width - 1), randint(0, height - 1))
        length = 5

        # Possible movement directions
        dirs = [
            (1, 0),  # right
            (-1, 0),  # left
            (0, 1),  # down
            (0, -1),  # up
        ]

        while True:

            # --------------- SNAKE MOVEMENT LOGIC -----------------

            # Randomly change direction (but avoid reversing)
            if random() < 0.15:
                new_dir = choice(dirs)
                if new_dir[0] != -direction[0] or new_dir[1] != -direction[1]:
                    direction = new_dir

            # Compute new head position
            head_x, head_y = snake[0]
            new_head = (
                (head_x + direction[0]) % width,  # wrap horizontally
                (head_y + direction[1]) % height,  # wrap vertically
            )

            # Add new head
            snake.insert(0, new_head)

            # If snake eats food
            if new_head == food:
                length += 1
                food = (randint(0, width - 1), randint(0, height - 1))
            else:
                # Trim to current length
                snake = snake[:length]

            # --------------- RENDER FRAME -------------------------

            screen = [[" " for _ in range(width)] for _ in range(height)]

            # Draw food
            fx, fy = food
            screen[fy][fx] = "[red]●[/red]"

            # Draw snake (head highlighted)
            for i, (x, y) in enumerate(snake):
                if i == 0:
                    screen[y][x] = "[green]■[/green]"  # head
                else:
                    screen[y][x] = "[#32a852]■[/#32a852]"

            # Convert to text output
            out = "\n".join("".join(row) for row in screen)
            self.update(out)

            # --------------- FRAME DELAY --------------------------

            await asyncio.sleep(delay)