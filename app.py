import sqlite3
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd

DB_PATH = Path("verifiche.db")
DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%d.%m.%Y",
]


class VerificheApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Gestore Verifiche Periodiche")
        self.root.geometry("980x600")

        self.conn = sqlite3.connect(DB_PATH)
        self._create_tables()

        self._build_ui()
        self._load_clienti()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        top_bar = ttk.Frame(container)
        top_bar.pack(fill="x", pady=(0, 12))

        ttk.Label(
            top_bar,
            text="Importa un file Excel per aggiornare l'ultima verifica dei clienti",
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left")

        ttk.Button(
            top_bar,
            text="Carica Excel",
            command=self._import_excel,
        ).pack(side="right")

        columns = ("id", "nome", "ultima_verifica", "email", "telefono")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=22)

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Cliente")
        self.tree.heading("ultima_verifica", text="Ultima verifica")
        self.tree.heading("email", text="Email")
        self.tree.heading("telefono", text="Telefono")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nome", width=320)
        self.tree.column("ultima_verifica", width=150, anchor="center")
        self.tree.column("email", width=220)
        self.tree.column("telefono", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status_var = tk.StringVar(value="Pronto")
        ttk.Label(container, textvariable=self.status_var, anchor="w").pack(fill="x", pady=(12, 0))

    def _create_tables(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clienti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                email TEXT,
                telefono TEXT,
                ultima_verifica DATE
            )
            """
        )
        self.conn.commit()

    def _load_clienti(self) -> None:
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, nome, IFNULL(ultima_verifica, ''), IFNULL(email, ''), IFNULL(telefono, '')
            FROM clienti
            ORDER BY nome COLLATE NOCASE
            """
        )

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def _import_excel(self) -> None:
        filepath = filedialog.askopenfilename(
            title="Seleziona file Excel",
            filetypes=[("File Excel", "*.xlsx *.xls")],
        )
        if not filepath:
            return

        try:
            dataframe = pd.read_excel(filepath)
        except Exception as error:
            messagebox.showerror("Errore", f"Impossibile leggere il file Excel.\n\n{error}")
            return

        required_columns = ["cliente", "data_verifica"]
        normalized_columns = {col.strip().lower(): col for col in dataframe.columns}
        missing = [c for c in required_columns if c not in normalized_columns]

        if missing:
            messagebox.showerror(
                "Colonne mancanti",
                "Il file deve contenere almeno queste colonne: Cliente, Data_Verifica",
            )
            return

        cliente_col = normalized_columns["cliente"]
        data_col = normalized_columns["data_verifica"]
        email_col = normalized_columns.get("email")
        telefono_col = normalized_columns.get("telefono")

        aggiornati = 0
        cursor = self.conn.cursor()

        for _, row in dataframe.iterrows():
            cliente = str(row.get(cliente_col, "")).strip()
            if not cliente or cliente.lower() == "nan":
                continue

            verifica = self._parse_date(row.get(data_col))
            if verifica is None:
                continue

            email = self._value_or_empty(row.get(email_col)) if email_col else ""
            telefono = self._value_or_empty(row.get(telefono_col)) if telefono_col else ""

            cursor.execute(
                "SELECT ultima_verifica, email, telefono FROM clienti WHERE nome = ?",
                (cliente,),
            )
            existing = cursor.fetchone()

            if existing:
                old_date = self._parse_date(existing[0])
                new_date = verifica if old_date is None or verifica > old_date else old_date
                new_email = email if email else (existing[1] or "")
                new_telefono = telefono if telefono else (existing[2] or "")

                cursor.execute(
                    """
                    UPDATE clienti
                    SET ultima_verifica = ?, email = ?, telefono = ?
                    WHERE nome = ?
                    """,
                    (new_date.isoformat(), new_email, new_telefono, cliente),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO clienti (nome, email, telefono, ultima_verifica)
                    VALUES (?, ?, ?, ?)
                    """,
                    (cliente, email, telefono, verifica.isoformat()),
                )
            aggiornati += 1

        self.conn.commit()
        self._load_clienti()
        self.status_var.set(f"Import completato: {aggiornati} righe processate")
        messagebox.showinfo("Completato", f"Importazione completata. Righe processate: {aggiornati}")

    @staticmethod
    def _value_or_empty(value: object) -> str:
        text = str(value).strip()
        return "" if text.lower() == "nan" else text

    @staticmethod
    def _parse_date(value: object):
        if pd.isna(value):
            return None

        if isinstance(value, datetime):
            return value.date()

        text = str(value).strip()
        if not text:
            return None

        for fmt in DATE_FORMATS:
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue

        converted = pd.to_datetime(text, errors="coerce", dayfirst=True)
        if pd.isna(converted):
            return None
        return converted.date()

    def close(self) -> None:
        self.conn.close()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    app = VerificheApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == "__main__":
    main()
