import customtkinter as ctk


class ConsoleOutput(ctk.CTkFrame):
    LEVEL_COLORS = {
        "info":    "#D4D4D4",
        "success": "#4EC9B0",
        "error":   "#F44747",
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.console_text = ctk.CTkTextbox(
            self, font=("Consolas", 10), height=150, state="disabled"
        )
        self.console_text.pack(fill="both", expand=True)

    def write(self, message: str, level: str = "info"):
        self.console_text.configure(state="normal")
        color = self.LEVEL_COLORS.get(level, self.LEVEL_COLORS["info"])
        self.console_text.insert("end", f"> {message}\n")
        self.console_text.tag_add(level, "end-2l", "end-1l")
        self.console_text.tag_config(level, foreground=color)
        self.console_text.configure(state="disabled")
        self.console_text.see("end")

    def clear(self):
        self.console_text.configure(state="normal")
        self.console_text.delete("1.0", "end")
        self.console_text.configure(state="disabled")
