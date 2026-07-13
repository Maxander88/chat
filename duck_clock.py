import datetime as dt
import platform
import tkinter as tk
from tkinter import messagebox

try:
    import winsound  # Disponibile su Windows
except ImportError:  # pragma: no cover
    winsound = None


class DuckClockApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Duck Clock")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        self.alarm_time: dt.time | None = None
        self.alarm_triggered_today: dt.date | None = None

        self._build_ui()
        self._tick()
        self._schedule_duck_sound()

    def _build_ui(self) -> None:
        self.clock_label = tk.Label(
            self.root,
            text="--:--:--",
            font=("Segoe UI", 28, "bold"),
        )
        self.clock_label.pack(pady=8)

        controls = tk.Frame(self.root)
        controls.pack(fill="x", padx=10)

        tk.Label(controls, text="Sveglia (HH:MM)").grid(row=0, column=0, sticky="w")
        self.alarm_entry = tk.Entry(controls, width=10)
        self.alarm_entry.grid(row=0, column=1, padx=5)
        tk.Button(controls, text="Imposta", command=self.set_alarm).grid(row=0, column=2, padx=5)

        tk.Label(controls, text="Avviso tra (min)").grid(row=1, column=0, sticky="w", pady=6)
        self.reminder_minutes = tk.Spinbox(controls, from_=1, to=240, width=6)
        self.reminder_minutes.grid(row=1, column=1, sticky="w")
        self.reminder_text = tk.Entry(controls, width=18)
        self.reminder_text.insert(0, "Pausa")
        self.reminder_text.grid(row=1, column=2, padx=5)
        tk.Button(controls, text="Avvia avviso", command=self.set_reminder).grid(row=1, column=3)

        self.status = tk.Label(self.root, text="Suono papera automatico ogni 5 minuti", fg="#226")
        self.status.pack(pady=6)

    def _tick(self) -> None:
        now = dt.datetime.now()
        self.clock_label.config(text=now.strftime("%H:%M:%S"))
        self._check_alarm(now)
        self.root.after(1000, self._tick)

    def set_alarm(self) -> None:
        raw = self.alarm_entry.get().strip()
        try:
            alarm = dt.datetime.strptime(raw, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Formato non valido", "Usa il formato HH:MM (es. 07:30)")
            return

        self.alarm_time = alarm
        self.alarm_triggered_today = None
        self.status.config(text=f"Sveglia impostata alle {alarm.strftime('%H:%M')}")

    def _check_alarm(self, now: dt.datetime) -> None:
        if self.alarm_time is None:
            return

        today = now.date()
        if self.alarm_triggered_today == today:
            return

        if now.hour == self.alarm_time.hour and now.minute == self.alarm_time.minute:
            self.alarm_triggered_today = today
            self.play_duck_sound()
            messagebox.showinfo("Sveglia", "Quack! È ora della sveglia 🦆")

    def set_reminder(self) -> None:
        try:
            minutes = int(self.reminder_minutes.get())
            if minutes <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Valore non valido", "Inserisci un numero di minuti valido.")
            return

        text = self.reminder_text.get().strip() or "Promemoria"
        delay_ms = minutes * 60 * 1000
        self.root.after(delay_ms, lambda: self._trigger_reminder(text))
        self.status.config(text=f"Avviso impostato tra {minutes} minuti")

    def _trigger_reminder(self, text: str) -> None:
        self.play_duck_sound()
        messagebox.showinfo("Avviso", f"Quack! {text}")

    def _schedule_duck_sound(self) -> None:
        self.play_duck_sound()
        self.root.after(5 * 60 * 1000, self._schedule_duck_sound)

    @staticmethod
    def play_duck_sound() -> None:
        is_windows = platform.system().lower().startswith("win")
        if winsound and is_windows:
            # Piccola sequenza per imitare un verso di papera
            winsound.Beep(700, 120)
            winsound.Beep(500, 160)
            winsound.Beep(700, 120)
        else:  # fallback
            print("Quack!")


if __name__ == "__main__":
    app_root = tk.Tk()
    DuckClockApp(app_root)
    app_root.mainloop()
