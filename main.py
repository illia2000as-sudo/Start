import tkinter as tk

class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Простой Кликер")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.clicks = 0

        # Заголовок
        self.title_label = tk.Label(root, text="Игра Кликер", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        # Счётчик
        self.score_label = tk.Label(root, text="Очки: 0", font=("Arial", 16))
        self.score_label.pack(pady=10)

        # Кнопка для кликов
        self.click_button = tk.Button(
            root, 
            text="КЛИКНИ МЕНЯ!", 
            font=("Arial", 14, "bold"), 
            bg="#4CAF50", 
            fg="white", 
            command=self.click
        )
        self.click_button.pack(pady=10, ipadx=10, ipady=5)

        # Кнопка сброса
        self.reset_button = tk.Button(root, text="Сбросить", command=self.reset)
        self.reset_button.pack(pady=5)

    def click(self):
        self.clicks += 1
        self.score_label.config(text=f"Очки: {self.clicks}")

    def reset(self):
        self.clicks = 0
        self.score_label.config(text="Очки: 0")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGame(root)
    root.mainloop()
