import tkinter as tk
import math

# ---------------- CONSTANTS ---------------- #
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLACK = "#333333"
FONT_NAME = "Courier"

reps = 0
timer = None
pulse_scale = 1.0
scale_direction = 1

# ---------------- RESET ---------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pomodoro", fg=GREEN)
    check_marks.config(text="")
    global reps
    reps = 0

# ---------------- START ---------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Pauză lungă", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Pauză scurtă", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Lucrează!", fg=GREEN)

# ---------------- COUNTDOWN ---------------- #
def count_down(count):
    minutes = math.floor(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"

    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = "✔" * (reps // 2)
        check_marks.config(text=marks)

# ---------------- PULSE ANIMATION ---------------- #
def pulse():
    global pulse_scale, scale_direction
    if pulse_scale >= 1.05:
        scale_direction = -1
    elif pulse_scale <= 0.95:
        scale_direction = 1
    pulse_scale += 0.005 * scale_direction
    canvas.scale("tomato", 100, 110, pulse_scale, pulse_scale)
    canvas.after(100, pulse)

# ---------------- UI ---------------- #
window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = tk.Label(text="Pomodoro", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
title_label.grid(column=1, row=0)

canvas = tk.Canvas(width=200, height=240, bg=YELLOW, highlightthickness=0)

# Corpul roșiei
canvas.create_oval(50, 70, 150, 170, fill=RED, outline="", tags="tomato")

# Frunzulițele verzi (stea simplificată)
canvas.create_polygon(100, 60, 110, 75, 90, 75, fill=GREEN, outline="", tags="tomato")
canvas.create_polygon(85, 65, 115, 65, 100, 80, fill=GREEN, outline="", tags="tomato")

# Față zâmbitoare :)
canvas.create_oval(80, 110, 90, 120, fill=BLACK, outline="", tags="tomato")  # ochi stâng
canvas.create_oval(110, 110, 120, 120, fill=BLACK, outline="", tags="tomato")  # ochi drept
canvas.create_arc(85, 115, 115, 135, start=0, extent=-180, style="arc", outline=BLACK, width=2, tags="tomato")  # zâmbet

# Timer text
timer_text = canvas.create_text(100, 200, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = tk.Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
check_marks.grid(column=1, row=3)

pulse()

window.mainloop()
