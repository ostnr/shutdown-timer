import tkinter as tk
from tkinter import ttk
import subprocess
import time
import threading
import tkinter.messagebox as messagebox

class ShutdownTimer:
    def __init__(self, master):
        self.master = master
        master.title("Shutdown Timer")
        master.geometry("500x400")
        master.configure(bg='#000000')

        self.time_remaining = tk.IntVar(value=40 * 60)
        self.force_shutdown = tk.BooleanVar(value=True)
        self.test_mode = tk.BooleanVar(value=False)
        self.timer_running = False
        self.timer_paused = False

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 16), padding=10, background='#1a1a1a', foreground='white')
        style.map('TButton', background=[('active', '#2a2a2a')])
        style.configure('TCheckbutton', font=('Arial', 14), background='#000000', foreground='white')
        style.map('TCheckbutton', background=[('active', '#000000')])

        # Custom button styles with colorful borders
        style.configure('Start.TButton', bordercolor='#00ff00', borderwidth=2)
        style.configure('Add.TButton', bordercolor='#0000ff', borderwidth=2)
        style.configure('Sub.TButton', bordercolor='#ff0000', borderwidth=2)
        style.configure('Shutdown.TButton', bordercolor='#ff00ff', borderwidth=2)

        self.time_label = tk.Label(self.master, text=self.format_time(self.time_remaining.get()), 
                                   font=('Arial', 48), bg='#000000', fg='white')
        self.time_label.pack(pady=30)

        self.start_pause_button = ttk.Button(self.master, text="Start Timer", command=self.toggle_timer, style='Start.TButton')
        self.start_pause_button.pack(pady=15)

        button_frame = tk.Frame(self.master, bg='#000000')
        button_frame.pack(pady=15)

        self.add_button = ttk.Button(button_frame, text="+10 min", command=lambda: self.adjust_time(10), style='Add.TButton')
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.sub_button = ttk.Button(button_frame, text="-10 min", command=lambda: self.adjust_time(-10), style='Sub.TButton')
        self.sub_button.pack(side=tk.LEFT, padx=10)

        self.shutdown_button = ttk.Button(self.master, text="Shutdown Now", command=self.shutdown_now, style='Shutdown.TButton')
        self.shutdown_button.pack(pady=15)

        self.force_checkbox = ttk.Checkbutton(self.master, text="Force Shutdown", variable=self.force_shutdown)
        self.force_checkbox.pack(pady=10)

        self.test_checkbox = ttk.Checkbutton(self.master, text="Test Mode", variable=self.test_mode)
        self.test_checkbox.pack(pady=10)

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def toggle_timer(self):
        if not self.timer_running:
            self.start_timer()
        else:
            self.pause_timer()

    def start_timer(self):
        self.timer_running = True
        self.timer_paused = False
        self.start_pause_button.config(text="Pause")
        threading.Thread(target=self.countdown, daemon=True).start()

    def pause_timer(self):
        self.timer_running = False
        self.timer_paused = True
        self.start_pause_button.config(text="Continue")

    def countdown(self):
        while self.time_remaining.get() > 0 and self.timer_running:
            time.sleep(1)
            self.time_remaining.set(self.time_remaining.get() - 1)
            self.time_label.config(text=self.format_time(self.time_remaining.get()))
        if self.timer_running:
            self.shutdown()

    def adjust_time(self, minutes):
        new_time = max(0, self.time_remaining.get() + minutes * 60)
        self.time_remaining.set(new_time)
        self.time_label.config(text=self.format_time(new_time))

    def shutdown_now(self):
        self.shutdown()

    def shutdown(self):
        if self.test_mode.get():
            messagebox.showinfo("Test Mode", "Shutdown simulated. Your PC would have been shut down now.")
        else:
            force = "/f" if self.force_shutdown.get() else ""
            subprocess.run(f"shutdown /s /t 1 {force}", shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownTimer(root)
    root.mainloop()