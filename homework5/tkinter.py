import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


# ДИАЛОГОВОЕ ОКНО
class MovieDetailsDialog(tk.Toplevel):
    def __init__(self, parent, title, year, genre, status):
        super().__init__(parent)
        self.title("Информация о фильме")
        self.geometry("320x220")
        self.configure(bg="#2b2b2b")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()  # модальное окно

        # Заголовок
        tk.Label(
            self, text=f"🎬 {title}",
            font=("Arial", 14, "bold"),
            fg="#FFD700", bg="#2b2b2b"
        ).pack(pady=(15, 10))

        # Детали
        details = tk.Frame(self, bg="#2b2b2b")
        details.pack(padx=20, fill="x")

        rows = [("Год выпуска:", year), ("Жанр:", genre), ("Статус:", status)]
        for i, (label, value) in enumerate(rows):
            tk.Label(details, text=label, fg="white", bg="#2b2b2b",
                     anchor="w", font=("Arial", 10)).grid(row=i, column=0, sticky="w", pady=3)
            tk.Label(details, text=value, fg="white", bg="#2b2b2b",
                     anchor="w", font=("Arial", 10)).grid(row=i, column=1, sticky="w", padx=(10, 0), pady=3)

        # Кнопка закрытия
        tk.Button(
            self, text="Закрыть", command=self.destroy,
            bg="#4CAF50", fg="white", relief="flat",
            font=("Arial", 10), padx=20, pady=5, cursor="hand2"
        ).pack(pady=15)


# ГЛАВНОЕ ОКНО
class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.data_file = "movies.json"

        self.root.title("Моя Кинобиблиотека")
        self.root.geometry("650x550")
        self.root.configure(bg="#2b2b2b")

        self.apply_styles()
        self.build_ui()
        self.load_data()

    # СТИЛИ
    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#2b2b2b")
        style.configure("TLabel", background="#2b2b2b", foreground="white")
        style.configure("TLabelframe", background="#2b2b2b",
                        foreground="white", bordercolor="#555", relief="solid")
        style.configure("TLabelframe.Label", background="#2b2b2b", foreground="white")
        style.configure("TEntry", fieldbackground="#3c3f41", foreground="white")
        style.configure("TCombobox",
                        fieldbackground="#3c3f41", background="#3c3f41",
                        foreground="white", arrowcolor="white")

        # Выпадающий список Combobox
        self.root.option_add("*TCombobox*Listbox.background", "#3c3f41")
        self.root.option_add("*TCombobox*Listbox.foreground", "white")
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#4C5052")

    # ИНТЕРФЕЙС
    def build_ui(self):
        # Блок ввода
        input_frame = ttk.LabelFrame(self.root, text=" Добавить новый фильм ", padding=10)
        input_frame.pack(fill="x", padx=10, pady=(10, 5))

        # Название
        ttk.Label(input_frame, text="Название фильма:").grid(row=0, column=0, sticky="w", pady=3)
        self.title_input = tk.Entry(
            input_frame, bg="#3c3f41", fg="white",
            insertbackground="white", relief="flat", bd=4
        )
        self.title_input.grid(row=0, column=1, sticky="ew", pady=3, padx=(8, 0))

        # Год
        ttk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w", pady=3)
        self.year_var = tk.IntVar(value=2024)
        self.year_input = tk.Spinbox(
            input_frame, from_=1900, to=2026, textvariable=self.year_var,
            bg="#3c3f41", fg="white", insertbackground="white",
            relief="flat", bd=4, buttonbackground="#555"
        )
        self.year_input.grid(row=1, column=1, sticky="ew", pady=3, padx=(8, 0))

        # Жанр
        ttk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="w", pady=3)
        self.genre_combo = ttk.Combobox(
            input_frame, state="readonly",
            values=["Фантастика", "Боевик", "Комедия", "Драма", "Ужасы", "Документальный"]
        )
        self.genre_combo.current(0)
        self.genre_combo.grid(row=2, column=1, sticky="ew", pady=3, padx=(8, 0))

        # Статус
        ttk.Label(input_frame, text="Статус:").grid(row=3, column=0, sticky="w", pady=3)
        self.status_combo = ttk.Combobox(
            input_frame, state="readonly",
            values=["Хочу посмотреть", "Просмотрено", "Любимый фильм"]
        )
        self.status_combo.current(0)
        self.status_combo.grid(row=3, column=1, sticky="ew", pady=3, padx=(8, 0))

        input_frame.columnconfigure(1, weight=1)

        # Кнопки
        btn_frame = tk.Frame(self.root, bg="#2b2b2b")
        btn_frame.pack(fill="x", padx=10, pady=5)

        self.add_btn = tk.Button(
            btn_frame, text="Добавить в библиотеку", command=self.add_movie,
            bg="#2196F3", fg="white", relief="flat",
            font=("Arial", 10, "bold"), pady=6, cursor="hand2"
        )
        self.add_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.delete_btn = tk.Button(
            btn_frame, text="Удалить выбранное", command=self.delete_movie,
            bg="#f44336", fg="white", relief="flat",
            font=("Arial", 10), pady=6, cursor="hand2"
        )
        self.delete_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))

        # Заголовок списка
        tk.Label(
            self.root, text="📚 Ваша коллекция (двойной клик для деталей):",
            bg="#2b2b2b", fg="white", font=("Arial", 10)
        ).pack(anchor="w", padx=10, pady=(10, 2))

        # Список фильмов + скроллбар
        list_frame = tk.Frame(self.root, bg="#2b2b2b")
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        scrollbar = tk.Scrollbar(list_frame, bg="#555", troughcolor="#1e1e1e")
        scrollbar.pack(side="right", fill="y")

        self.movie_list = tk.Listbox(
            list_frame, bg="#1e1e1e", fg="#e0e0e0",
            selectbackground="#4C5052", selectforeground="white",
            font=("Arial", 11), activestyle="none",
            yscrollcommand=scrollbar.set, relief="flat", bd=1,
            highlightthickness=1, highlightbackground="#555"
        )
        self.movie_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.movie_list.yview)

        self.movie_list.bind("<Double-Button-1>", self.show_details)

        # Статистика
        self.stats_label = tk.Label(
            self.root, text="Всего фильмов: 0",
            bg="#2b2b2b", fg="#4CAF50", font=("Arial", 11, "bold")
        )
        self.stats_label.pack(anchor="w", padx=10, pady=(0, 10))

    # ЛОГИКА
    def add_movie(self):
        title = self.title_input.get().strip()

        if not title:
            messagebox.showwarning("Ошибка ввода", "Название фильма не может быть пустым!")
            return

        try:
            year = self.year_var.get()
        except tk.TclError:
            messagebox.showwarning("Ошибка ввода", "Введите корректный год!")
            return

        genre = self.genre_combo.get()
        status = self.status_combo.get()

        item_text = f"[{year}] {title} | {genre} | {status}"
        self.movie_list.insert(tk.END, item_text)
        idx = self.movie_list.size() - 1

        if status == "Просмотрено":
            self.movie_list.itemconfig(idx, foreground="#81C784")
        elif status == "Любимый фильм":
            self.movie_list.itemconfig(idx, foreground="#FFD54F")

        self.title_input.delete(0, tk.END)
        self.title_input.focus_set()

        self.update_stats()
        self.save_data()

    def delete_movie(self):
        selection = self.movie_list.curselection()
        if not selection:
            messagebox.showinfo("Внимание", "Сначала выберите фильм из списка для удаления.")
            return

        idx = selection[0]
        text = self.movie_list.get(idx)

        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить:\n'{text}'?"):
            self.movie_list.delete(idx)
            self.update_stats()
            self.save_data()

    def show_details(self, event=None):
        selection = self.movie_list.curselection()
        if not selection:
            return

        text = self.movie_list.get(selection[0])

        try:
            parts = text.split(" | ")
            title_part = parts[0]
            year = title_part.split("]")[0].replace("[", "")
            title = title_part.split("] ")[1]
            genre = parts[1]
            status = parts[2]

            MovieDetailsDialog(self.root, title, year, genre, status)
        except Exception:
            messagebox.showwarning("Ошибка", "Не удалось прочитать данные фильма.")

    def update_stats(self):
        count = self.movie_list.size()
        self.stats_label.config(text=f"Всего фильмов в коллекции: {count}")

    # СОХРАНЕНИЕ / ЗАГРУЗКА
    def save_data(self):
        movies = list(self.movie_list.get(0, tk.END))
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False)

    def load_data(self):
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                movies = json.load(f)
        except Exception:
            return

        for movie_text in movies:
            self.movie_list.insert(tk.END, movie_text)
            idx = self.movie_list.size() - 1
            if "Просмотрено" in movie_text:
                self.movie_list.itemconfig(idx, foreground="#81C784")
            elif "Любимый фильм" in movie_text:
                self.movie_list.itemconfig(idx, foreground="#FFD54F")

        self.update_stats()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
