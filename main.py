import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class DevConsole(tk.Toplevel):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.title("Консоль разработчика [ADMIN]")
        self.geometry("400x250")
        self.configure(bg="#11111b")
        self.resizable(False, False)

        # Вывод логов и результатов
        self.output = tk.Text(self, bg="#1e1e2e", fg="#a6e3a1", font=("Consolas", 10), state="disabled", height=8)
        self.output.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Поле ввода команд
        self.entry = tk.Entry(self, bg="#313244", fg="#cdd6f4", font=("Consolas", 11), insertbackground="white")
        self.entry.pack(fill="x", padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.execute_command)
        self.entry.focus_set()

        self.log("Консоль запущенa. Введите /help для списка команд.")

    def log(self, text):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.config(state="disabled")

    def execute_command(self, event=None):
        cmd = self.entry.get().strip()
        self.entry.delete(0, "end")

        if not cmd:
            return

        self.log(f"> {cmd}")
        parts = cmd.split()
        base_cmd = parts[0].lower()

        if base_cmd == "/help":
            self.log("/give <кол-во>  - выдать очки")
            self.log("/cps <кол-во>   - установить CPS")
            self.log("/power <кол-во> - установить силу клика")
            self.log("/reset          - сбросить весь прогресс")

        elif base_cmd == "/give" and len(parts) > 1:
            if parts[1].isdigit():
                val = int(parts[1])
                self.game.score += val
                self.game.update_ui()
                self.log(f"[Успех] Выдано {val} очков!")
            else:
                self.log("[Ошибка] Укажите число.")

        elif base_cmd == "/cps" and len(parts) > 1:
            if parts[1].isdigit():
                val = int(parts[1])
                self.game.cps = val
                self.game.update_ui()
                self.log(f"[Успех] Пассивный доход установлен в {val}/сек.")
            else:
                self.log("[Ошибка] Укажите число.")

        elif base_cmd == "/power" and len(parts) > 1:
            if parts[1].isdigit():
                val = int(parts[1])
                self.game.click_power = val
                self.game.update_ui()
                self.log(f"[Успех] Сила клика установлена в {val}.")
            else:
                self.log("[Ошибка] Укажите число.")

        elif base_cmd == "/reset":
            self.game.score = 0
            self.game.click_power = 1
            self.game.click_cost = 10
            self.game.auto_clickers = 0
            self.game.auto_cost = 50
            self.game.cps = 0
            self.game.update_ui()
            self.log("[Успех] Прогресс полностью сброшен!")

        else:
            self.log("[Ошибка] Неизвестная команда. Введите /help")


class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Супер Кликер — Big Update 2.0 (+Admin Console)")
        self.root.geometry("450x620")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        # Значения по умолчанию
        self.score = 0
        self.click_power = 1
        self.click_cost = 10
        
        self.auto_clickers = 0
        self.auto_cost = 50
        self.cps = 0

        self.console_window = None
        self.save_file = "save.json"
        self.load_data()

        # Биндим нажатие F1 на открытие консоли
        self.root.bind("<F1>", self.open_console)

        # Заголовок
        self.title_label = tk.Label(
            root, text="⚡ BIG CLICKER UPDATE ⚡", 
            font=("Arial", 18, "bold"), bg="#1e1e2e", fg="#cba6f7"
        )
        self.title_label.pack(pady=10)

        # Подсказка про консоль
        self.hint_label = tk.Label(
            root, text="Нажмите F1 для вызова админ-консоли", 
            font=("Arial", 9, "italic"), bg="#1e1e2e", fg="#6c7086"
        )
        self.hint_label.pack(pady=2)

        # Счет очков
        self.score_label = tk.Label(
            root, text=f"Очки: {self.score}", 
            font=("Arial", 26, "bold"), bg="#1e1e2e", fg="#a6e3a1"
        )
        self.score_label.pack(pady=5)

        # CPS (Кликов в секунду)
        self.cps_label = tk.Label(
            root, text=f"Пассивный доход: {self.cps} / сек", 
            font=("Arial", 12), bg="#1e1e2e", fg="#89dceb"
        )
        self.cps_label.pack(pady=5)

        # Главная кнопка клика
        self.click_btn = tk.Button(
            root, text="КЛИК!", font=("Arial", 22, "bold"),
            bg="#f38ba8", fg="#11111b", activebackground="#f5e0dc",
            width=12, height=2, command=self.on_click, bd=0, cursor="hand2"
        )
        self.click_btn.pack(pady=15)

        # Панель магазина
        self.shop_frame = tk.LabelFrame(
            root, text=" 🛒 Магазин Улучшений ", font=("Arial", 12, "bold"),
            bg="#313244", fg="#cdd6f4", bd=2, relief="groove"
        )
        self.shop_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Кнопка прокачки клика
        self.upgrade_click_btn = tk.Button(
            self.shop_frame, 
            text=f"+1 к клику (Цена: {self.click_cost})", 
            font=("Arial", 11, "bold"), bg="#89b4fa", fg="#11111b",
            command=self.buy_click_power, cursor="hand2"
        )
        self.upgrade_click_btn.pack(fill="x", padx=15, pady=8)

        # Кнопка автокликера
        self.buy_auto_btn = tk.Button(
            self.shop_frame, 
            text=f"+1 Автокликер (Цена: {self.auto_cost})", 
            font=("Arial", 11, "bold"), bg="#fab387", fg="#11111b",
            command=self.buy_auto_clicker, cursor="hand2"
        )
        self.buy_auto_btn.pack(fill="x", padx=15, pady=8)

        # Запуск таймера автокликов и сохранения при закрытии
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.auto_click_loop()
        self.update_ui()

    def open_console(self, event=None):
        if self.console_window is None or not self.console_window.winfo_exists():
            self.console_window = DevConsole(self.root, self)
        else:
            self.console_window.focus_set()

    def on_click(self):
        self.score += self.click_power
        self.update_ui()

    def buy_click_power(self):
        if self.score >= self.click_cost:
            self.score -= self.click_cost
            self.click_power += 1
            self.click_cost = int(self.click_cost * 1.5)
            self.update_ui()

    def buy_auto_clicker(self):
        if self.score >= self.auto_cost:
            self.score -= self.auto_cost
            self.auto_clickers += 1
            self.cps = self.auto_clickers
            self.auto_cost = int(self.auto_cost * 1.6)
            self.update_ui()

    def auto_click_loop(self):
        if self.cps > 0:
            self.score += self.cps
            self.update_ui()
        self.root.after(1000, self.auto_click_loop)

    def update_ui(self):
        self.score_label.config(text=f"Очки: {self.score}")
        self.cps_label.config(text=f"Пассивный доход: {self.cps} / сек")
        self.upgrade_click_btn.config(text=f"+1 к клику [Ур. {self.click_power}] (Цена: {self.click_cost})")
        self.buy_auto_btn.config(text=f"+1 Автокликер [{self.auto_clickers} шт] (Цена: {self.auto_cost})")

    def save_data(self):
        data = {
            "score": self.score,
            "click_power": self.click_power,
            "click_cost": self.click_cost,
            "auto_clickers": self.auto_clickers,
            "auto_cost": self.auto_cost,
            "cps": self.cps
        }
        with open(self.save_file, "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    self.score = data.get("score", 0)
                    self.click_power = data.get("click_power", 1)
                    self.click_cost = data.get("click_cost", 10)
                    self.auto_clickers = data.get("auto_clickers", 0)
                    self.auto_cost = data.get("auto_cost", 50)
                    self.cps = data.get("cps", 0)
            except Exception:
                pass

    def on_close(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGame(root)
    root.mainloop()
