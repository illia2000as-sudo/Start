import customtkinter as ctk
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
            self.sidebar, text="💎 Clicker\nLauncher", 
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
