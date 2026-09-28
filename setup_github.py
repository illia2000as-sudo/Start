import os
import subprocess

# 1. Содержимое файла requirements.txt
REQUIREMENTS_CONTENT = """customtkinter
Pillow
"""

# 2. Содержимое launcher.py (Crystal Clicker Launcher)
LAUNCHER_CONTENT = '''import customtkinter as ctk
import urllib.request
import subprocess
import os
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

GITHUB_USER = "YOUR_USERNAME"  # Замени на свой GitHub никнейм
GITHUB_REPO = "YOUR_REPO"      # Замени на название репозитория
GAME_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/main.py"
GAME_FILE = "main.py"

class CrystalLauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Clicker Launcher — Crystal Clicker")
        self.geometry("900x550")
        self.configure(fg_color="#0d1117")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Боковая панель
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#161b22")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="💎 Clicker\\nLauncher", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#58a6ff"
        )
        self.logo_label.pack(pady=(30, 20), padx=20)

        self.btn_main = ctk.CTkButton(self.sidebar, text="🏠 Главная", fg_color="#21262d", hover_color="#30363d", anchor="w")
        self.btn_main.pack(fill="x", padx=15, pady=5)

        self.btn_play = ctk.CTkButton(self.sidebar, text="🎮 Играть", fg_color="transparent", hover_color="#21262d", anchor="w")
        self.btn_play.pack(fill="x", padx=15, pady=5)

        self.btn_shop = ctk.CTkButton(self.sidebar, text="🛒 Магазин", fg_color="transparent", hover_color="#21262d", anchor="w")
        self.btn_shop.pack(fill="x", padx=15, pady=5)

        self.btn_settings = ctk.CTkButton(self.sidebar, text="⚙️ Настройки", fg_color="transparent", hover_color="#21262d", anchor="w")
        self.btn_settings.pack(fill="x", padx=15, pady=5)

        # Правый контент
        self.main_content = ctk.CTkFrame(self, fg_color="#0d1117")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.banner_card = ctk.CTkFrame(self.main_content, fg_color="#161b22", corner_radius=12)
        self.banner_card.pack(fill="x", pady=(0, 15), ipady=20)

        self.game_title = ctk.CTkLabel(
            self.banner_card, text="Crystal Clicker", 
            font=ctk.CTkFont(size=26, weight="bold"), text_color="#f0f6fc"
        )
        self.game_title.pack(pady=(10, 2))

        self.game_desc = ctk.CTkLabel(
            self.banner_card, text="Собирай очки, покупай прокачки, используй кристаллы и стань сильнее!", 
            font=ctk.CTkFont(size=12), text_color="#8b949e"
        )
        self.game_desc.pack(pady=(0, 15))

        self.action_btn = ctk.CTkButton(
            self.banner_card, text="ПРОВЕРКА...", 
            font=ctk.CTkFont(size=16, weight="bold"), fg_color="#238636", hover_color="#2ea043",
            height=45, width=200, corner_radius=8
        )
        self.action_btn.pack()

        self.status_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.status_frame.pack(fill="x", pady=10)

        self.card1 = self.create_status_card(self.status_frame, "☁️ Скачать игру", "Автозагрузка обновлений")
        self.card1.pack(side="left", expand=True, fill="both", padx=5)

        self.card2 = self.create_status_card(self.status_frame, "🛡️ Проверка файлов", "Целостность соблюдена")
        self.card2.pack(side="left", expand=True, fill="both", padx=5)

        self.card3 = self.create_status_card(self.status_frame, "⚙️ Обновления", "Версия v3.0 готова")
        self.card3.pack(side="left", expand=True, fill="both", padx=5)

        self.progress = ctk.CTkProgressBar(self.main_content, height=8, progress_color="#58a6ff")
        self.progress.pack(fill="x", pady=15)
        self.progress.set(1.0)

        self.check_files()

    def create_status_card(self, parent, title, subtitle):
        card = ctk.CTkFrame(parent, fg_color="#161b22", corner_radius=10)
        t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color="#c9d1d9")
        t.pack(anchor="w", padx=10, pady=(8, 2))
        sub = ctk.CTkLabel(card, text=subtitle, font=ctk.CTkFont(size=10), text_color="#8b949e")
        sub.pack(anchor="w", padx=10, pady=(0, 8))
        return card

    def check_files(self):
        if os.path.exists(GAME_FILE):
            self.action_btn.configure(text="▶ ИГРАТЬ", command=self.launch_game, state="normal")
        else:
            self.action_btn.configure(text="📥 СКАЧАТЬ ИГРУ", command=self.start_download, state="normal")

    def start_download(self):
        self.action_btn.configure(state="disabled", text="СКАЧИВАНИЕ...")
        threading.Thread(target=self.download_thread, daemon=True).start()

    def download_thread(self):
        try:
            urllib.request.urlretrieve(GAME_URL, GAME_FILE)
            self.check_files()
        except Exception:
            self.action_btn.configure(text="ОШИБКА", state="normal")

    def launch_game(self):
        subprocess.Popen(["python", GAME_FILE])
        self.destroy()

if __name__ == "__main__":
    app = CrystalLauncherApp()
    app.mainloop()
'''

# 3. Содержимое main.py (Crystal Clicker)
MAIN_CONTENT = '''import customtkinter as ctk
import json
import os

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

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Левая панель
        self.left_panel = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=15)
        self.left_panel.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.score_card = ctk.CTkFrame(self.left_panel, fg_color="#21262d", corner_radius=10)
        self.score_card.pack(fill="x", padx=15, pady=15)

        self.lbl_score = ctk.CTkLabel(self.score_card, text=f"Очки: {self.score}", font=ctk.CTkFont(size=24, weight="bold"), text_color="#3fb950")
        self.lbl_score.pack(pady=5)

        self.lbl_crystals = ctk.CTkLabel(self.score_card, text=f"💎 Кристаллы: {self.crystals}", font=ctk.CTkFont(size=14), text_color="#58a6ff")
        self.lbl_crystals.pack(pady=2)

        self.click_btn = ctk.CTkButton(
            self.left_panel, text="💎\\nКЛИК!", font=ctk.CTkFont(size=28, weight="bold"),
            fg_color="#1f6beb", hover_color="#388bfd", corner_radius=100, width=180, height=180,
            command=self.on_click
        )
        self.click_btn.pack(expand=True, pady=20)

        # Правая панель (Магазин)
        self.right_panel = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=15)
        self.right_panel.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(self.right_panel, text="🛒 Магазин Crystal Clicker", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        self.card_click = self.create_shop_item("✊ Сила клика", self.buy_click_power)
        self.card_auto = self.create_shop_item("⚙️ Автокликер", self.buy_auto)
        self.card_factory = self.create_shop_item("🏭 Фабрика", self.buy_factory)

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
'''

def write_files():
    print("📝 Создание файлов проекта...")
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(REQUIREMENTS_CONTENT)
    print("✅ requirements.txt сохранён.")

    with open("launcher.py", "w", encoding="utf-8") as f:
        f.write(LAUNCHER_CONTENT)
    print("✅ launcher.py сохранён.")

    with open("main.py", "w", encoding="utf-8") as f:
        f.write(MAIN_CONTENT)
    print("✅ main.py сохранён.")

def push_to_github():
    print("\n🚀 Отправка изменений на GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Переименование в Crystal Clicker + CustomTkinter интерфейс"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("\n🎉 ВСЁ ГОТОВО! Изменения успешно отправлены на GitHub.")
    except Exception as e:
        print(f"\n⚠️ Не удалось автоматически выполнить push через git: {e}")
        print("Запусти вручную в терминале: git add . && git commit -m 'update' && git push")

if __name__ == "__main__":
    write_files()
    push_to_github()
