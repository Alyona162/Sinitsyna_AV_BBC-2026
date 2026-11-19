import sys
import json
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

#ДИАЛОГОВОЕ ОКНО
class MovieDetailsDialog(QDialog):
    def __init__(self, title, year, genre, status, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Информация о фильме")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel(f"🎬 {title}")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFD700;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Детали
        details_layout = QFormLayout()
        details_layout.addRow("Год выпуска:", QLabel(str(year)))
        details_layout.addRow("Жанр:", QLabel(genre))
        details_layout.addRow("Статус:", QLabel(status))
        
        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 3px;")
        
        layout.addWidget(title_label)
        layout.addLayout(details_layout)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")


#ГЛАВНОЕ ОКНО 
class MovieLibrary(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_file = "movies.json"
        self.initUI()
        self.load_data()

    def initUI(self):
        self.setWindowTitle("Моя Кинобиблиотека")
        self.setGeometry(200, 200, 600, 500)

        # Основной виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        #Блок ввода
        input_group = QGroupBox("Добавить новый фильм")
        form_layout = QFormLayout()

        #Поле ввода (Текст)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Например: Интерстеллар")
        
        #Поле ввода (Число - год)
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2026)
        self.year_input.setValue(2024)

        #Выбор параметров
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["Фантастика", "Боевик", "Комедия", "Драма", "Ужасы", "Документальный"])

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Хочу посмотреть", "Просмотрено", "Любимый фильм"])

        form_layout.addRow("Название фильма:", self.title_input)
        form_layout.addRow("Год выпуска:", self.year_input)
        form_layout.addRow("Жанр:", self.genre_combo)
        form_layout.addRow("Статус:", self.status_combo)
        
        input_group.setLayout(form_layout)
        
        #Кнопки
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить в библиотеку")
        self.add_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px; border-radius: 5px;")
        self.delete_btn = QPushButton("Удалить выбранное")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        
        #Обработка событий
        self.add_btn.clicked.connect(self.add_movie)
        self.delete_btn.clicked.connect(self.delete_movie)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.delete_btn)

        #Вывод результатов (Список) 
        self.movie_list = QListWidget()
        self.movie_list.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0; font-size: 14px; padding: 5px;")
        #Обработка событий: Двойной клик открывает диалоговое окно
        self.movie_list.itemDoubleClicked.connect(self.show_details)

        # Статистика
        self.stats_label = QLabel("Всего фильмов: 0")
        self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50;")

        # Собираем всё вместе
        main_layout.addWidget(input_group)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(QLabel("📚 Ваша коллекция (двойной клик для деталей):"))
        main_layout.addWidget(self.movie_list)
        main_layout.addWidget(self.stats_label)

        self.apply_styles()

    # ЛОГИКА ПРИЛОЖЕНИЯ
    #Проверка данных и Обработка событий
    def add_movie(self):
        title = self.title_input.text().strip()
        
        # Проверка данных: нельзя добавить пустой фильм
        if not title:
            QMessageBox.warning(self, "Ошибка ввода", "Название фильма не может быть пустым!")
            return

        year = self.year_input.value()
        genre = self.genre_combo.currentText()
        status = self.status_combo.currentText()

        # Формируем строку для списка
        item_text = f"[{year}] {title} | {genre} | {status}"
        item = QListWidgetItem(item_text)
        
        # Красим "Просмотрено" в зеленый, остальное в белый
        if status == "Просмотрено":
            item.setForeground(QColor("#81C784"))
        elif status == "Любимый фильм":
            item.setForeground(QColor("#FFD54F"))

        self.movie_list.addItem(item)
        
        # Очищаем поля после добавления
        self.title_input.clear()
        self.title_input.setFocus() # Возвращаем курсор в поле ввода
        
        self.update_stats()
        self.save_data()

    def delete_movie(self):
        selected_item = self.movie_list.currentItem()
        
        if not selected_item:
            QMessageBox.information(self, "Внимание", "Сначала выберите фильм из списка для удаления.")
            return

        # Диалоговое окно подтверждения
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить:\n'{selected_item.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.movie_list.row(selected_item)
            self.movie_list.takeItem(row) # Удаляем из списка
            self.update_stats()
            self.save_data()

    #Кастомное диалоговое окно
    def show_details(self, item):
        # Разбираем строку обратно на части
        text = item.text()
        try:
            parts = text.split(" | ")
            title_part = parts[0]
            year = title_part.split("]")[0].replace("[", "")
            title = title_part.split("] ")[1]
            genre = parts[1]
            status = parts[2]
            
            dialog = MovieDetailsDialog(title, year, genre, status, self)
            dialog.exec()
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Не удалось прочитать данные фильма.")

    def update_stats(self):
        count = self.movie_list.count()
        self.stats_label.setText(f"Всего фильмов в коллекции: {count}")

    #Сохранение и загрузка
    def save_data(self):
        movies = []
        for i in range(self.movie_list.count()):
            movies.append(self.movie_list.item(i).text())
            
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    movies = json.load(f)
                    for movie_text in movies:
                        item = QListWidgetItem(movie_text)
                        if "Просмотрено" in movie_text:
                            item.setForeground(QColor("#81C784"))
                        elif "Любимый фильм" in movie_text:
                            item.setForeground(QColor("#FFD54F"))
                        self.movie_list.addItem(item)
                self.update_stats()
            except:
                pass

    def apply_styles(self):
        # Общие стили для темной темы
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QGroupBox { 
                color: #ffffff; 
                border: 1px solid #555; 
                border-radius: 5px; 
                margin-top: 10px; 
                padding-top: 15px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }
            QLabel { color: #ffffff; }
            QLineEdit, QSpinBox, QComboBox {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QListWidget { border: 1px solid #555; border-radius: 5px; }
            QListWidget::item { padding: 5px; border-bottom: 1px solid #333; }
            QListWidget::item:selected { background-color: #4C5052; }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MovieLibrary()
    window.show()
    sys.exit(app.exec())
