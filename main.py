import customtkinter as ctk
import json
import os
import random

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CrystalClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crystal Clicker v3.0")
        self.geometry("950x650")
        self.configure(fg_color="#0d1117")

        self.score = 0
        self.crystals = 0
        self.rebirths = 0
        self.click_power = 1
        self.click_cost = 10
        self.auto_clickers = 0
        self.auto_cost = 50
        self.factories = 0
        self.factory_cost = 250
        self.save_file = "save.json"

        self.load_data()

        # Разметка окна на 2 колонки: Игровое поле и Магазин
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Левая панель (Клик и Статистика) ---
        self.left_panel = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=15)
        self.left_panel.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # Статы
        self.score_card = ctk.CTkFrame(self.left_panel, fg_color="#21262d", corner_radius=10)
        self.score_card.pack(fill="x", padx=15, pady=15)

        self.lbl_score = ctk.CTkLabel(self.score_card, text=f"Очки: {self.score}", font=ctk.CTkFont(size=24, weight="bold"), text_color="#3fb950")
        self.lbl_score.pack(pady=5)

        self.lbl_crystals = ctk.CTkLabel(self.score_card, text=f"💎 Кристаллы: {self.crystals}", font=ctk.CTkFont(size=14), text_color="#58a6ff")
        self.lbl_crystals.pack(pady=2)

        # Кликер-зона
        self.click_btn = ctk.CTkButton(
            self.left_panel, text="💎\nКЛИК!", font=ctk.CTkFont(size=28, weight="bold"),
            fg_color="#1f6beb", hover_color="#388bfd", corner_radius=100, width=180, height=180,
            command=self.on_click
        )
        self.click_btn.pack(expand=True, pady=20)

        # --- Правая панель (Магазин прокачек) ---
        self.right_panel = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=15)
        self.right_panel.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(self.right_panel, text="🛒 Магазин", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        # Карточки товаров в стиле интерфейса со скриншота
        self.card_click = self.create_shop_item("✊ Сила клика", self.buy_click_power)
        self.card_auto = self.create_shop_item("⚙️ Автокликер", self.buy_auto)
        self.card_factory = self.create_shop_item("🏭 Фабрика", self.buy_factory)

        # Перерождение
        self.rebirth_btn = ctk.CTkButton(
            self.right_panel, text="👑 ПЕРЕРОЖДЕНИЕ (5,000 очков)", 
            fg_color="#d29922", hover_color="#e3b341", font=ctk.CTkFont(weight="bold"),
            command=self.do_rebirth
        )
        self.rebirth_btn.pack(fill="x", padx=15, pady=20)

        self.auto_loop()
        self.update_ui()

    def create_shop_item(self, title, command):
        frame = ctk.CTkFrame(self.right_panel, fg_color="#21262d", corner_radius=10)
        frame.pack(fill="x", padx=15, pady=8)

        lbl = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold"))
        lbl.pack(side="left", padx=10, pady=10)

        btn = ctk.CTkButton(frame, text="Купить", width=90, fg_color="#238636", hover_color="#2ea043", command=command)
        btn.pack(side="right", padx=10, pady=10)
        
        frame.btn = btn
        return frame

    def on_click(self):
        val = int(self.click_power * (1 + self.crystals * 0.5))
        self.score += val
        self.update_ui()

    def buy_click_power(self):
        if self.score >= self.click_cost:
            self.score -= self.click_cost
            self.click_power += 1
            self.click_cost = int(self.click_cost * 1.5)
            self.update_ui()

    def buy_auto(self):
        if self.score >= self.auto_cost:
            self.score -= self.auto_cost
            self.auto_clickers += 1
            self.auto_cost = int(self.auto_cost * 1.6)
            self.update_ui()

    def buy_factory(self):
        if self.score >= self.factory_cost:
            self.score -= self.factory_cost
            self.factories += 1
            self.factory_cost = int(self.factory_cost * 1.7)
            self.update_ui()

    def do_rebirth(self):
        if self.score >= 5000:
            self.score = 0
            self.crystals += 5
            self.click_power = 1
            self.auto_clickers = 0
            self.factories = 0
            self.update_ui()

    def auto_loop(self):
        income = (self.auto_clickers * 1 + self.factories * 10) * (1 + self.crystals * 0.5)
        self.score += int(income)
        self.update_ui()
        self.after(1000, self.auto_loop)

    def update_ui(self):
        self.lbl_score.configure(text=f"Очки: {self.score}")
        self.lbl_crystals.configure(text=f"💎 Кристаллы: {self.crystals}")
        self.card_click.btn.configure(text=f"${self.click_cost}")
        self.card_auto.btn.configure(text=f"${self.auto_cost}")
        self.card_factory.btn.configure(text=f"${self.factory_cost}")

    def save_data(self):
        data = {"score": self.score, "crystals": self.crystals, "click_power": self.click_power}
        with open(self.save_file, "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    d = json.load(f)
                    self.score = d.get("score", 0)
                    self.crystals = d.get("crystals", 0)
                    self.click_power = d.get("click_power", 1)
            except Exception:
                pass

if __name__ == "__main__":
    app = CrystalClickerApp()
    app.mainloop()
