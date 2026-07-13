import datetime as dt
import math
import random
import tkinter as tk


class TransparentAnalogClock:
    """Orologio analogico 300x300 con sfondo trasparente e lancette cangianti."""

    SIZE = 300
    CENTER = SIZE // 2
    RADIUS = 140

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Orologio Analogico Trasparente")
        self.root.geometry(f"{self.SIZE}x{self.SIZE}")
        self.root.resizable(False, False)

        # Colore usato come chiave di trasparenza (funziona su Windows).
        self.transparent_key = "#00ff00"
        self.root.configure(bg=self.transparent_key)
        self.root.wm_attributes("-transparentcolor", self.transparent_key)
        self.root.wm_attributes("-topmost", True)

        self.canvas = tk.Canvas(
            self.root,
            width=self.SIZE,
            height=self.SIZE,
            bg=self.transparent_key,
            bd=0,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.hand_colors = ("#ff4d4d", "#4dff4d", "#4da6ff")

        self._draw_static_clock()
        self._update_clock()

    def _draw_static_clock(self) -> None:
        # Corona esterna opaca per rendere visibile il quadrante.
        self.canvas.create_oval(
            self.CENTER - self.RADIUS,
            self.CENTER - self.RADIUS,
            self.CENTER + self.RADIUS,
            self.CENTER + self.RADIUS,
            outline="#ffffff",
            width=4,
        )

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            outer = self.RADIUS - 2
            inner = self.RADIUS - (14 if i % 5 == 0 else 7)
            x1 = self.CENTER + inner * math.cos(angle)
            y1 = self.CENTER + inner * math.sin(angle)
            x2 = self.CENTER + outer * math.cos(angle)
            y2 = self.CENTER + outer * math.sin(angle)
            color = "#ffffff" if i % 5 == 0 else "#b3b3b3"
            width = 3 if i % 5 == 0 else 1
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    def _point_on_circle(self, angle_deg: float, length: float) -> tuple[float, float]:
        angle = math.radians(angle_deg - 90)
        return (
            self.CENTER + length * math.cos(angle),
            self.CENTER + length * math.sin(angle),
        )

    def _new_random_colors(self) -> tuple[str, str, str]:
        return tuple(f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}" for _ in range(3))

    def _update_clock(self) -> None:
        now = dt.datetime.now()

        # Cambia colore ogni secondo.
        self.hand_colors = self._new_random_colors()

        sec_angle = now.second * 6
        min_angle = now.minute * 6 + now.second * 0.1
        hour_angle = (now.hour % 12) * 30 + now.minute * 0.5

        self.canvas.delete("hands")

        hx, hy = self._point_on_circle(hour_angle, self.RADIUS * 0.50)
        mx, my = self._point_on_circle(min_angle, self.RADIUS * 0.72)
        sx, sy = self._point_on_circle(sec_angle, self.RADIUS * 0.86)

        self.canvas.create_line(self.CENTER, self.CENTER, hx, hy, fill=self.hand_colors[0], width=6, tags="hands")
        self.canvas.create_line(self.CENTER, self.CENTER, mx, my, fill=self.hand_colors[1], width=4, tags="hands")
        self.canvas.create_line(self.CENTER, self.CENTER, sx, sy, fill=self.hand_colors[2], width=2, tags="hands")

        self.canvas.create_oval(
            self.CENTER - 6,
            self.CENTER - 6,
            self.CENTER + 6,
            self.CENTER + 6,
            fill="#ffffff",
            outline="",
            tags="hands",
        )

        # Aggiorna all'inizio del prossimo secondo.
        delay = 1000 - int(now.microsecond / 1000)
        self.root.after(delay, self._update_clock)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    TransparentAnalogClock().run()
