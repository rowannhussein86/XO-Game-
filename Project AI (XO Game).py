import tkinter as tk
from tkinter import messagebox

# Initialize board
board = [" " for _ in range(9)]
buttons = []

# Scores
player_x_score = 0
player_o_score = 0

# Timer variable
time_left = 30 # 30 seconds

# Colors & Style
btn_font = ("Helvetica", 32, "bold")
btn_bg = "#ffc0cb"          
btn_active_bg = "#add8e6"    
btn_disabled_bg = "#f8f0f8"  
player_color = "#ff69b4"    
ai_color = "#1f77b4"       

# Main window
root = tk.Tk()
root.title("XO Game - Player vs AI")
root.configure(bg="#ffffff")

# Score Label
score_label = tk.Label(root, text="Score - You (X): 0 || AI (O): 0", font=("Helvetica", 16), bg="#ffffff")
score_label.grid(row=3, column=0, columnspan=3, pady=(10, 0))

# Timer Label
timer_label = tk.Label(root, text="Time Left: 30", font=("Helvetica", 16), bg="#ffffff")
timer_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))

# Game logic
def winner(board, player):
    win_cond = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_cond:
        all_match = True
        for i in combo:
            if board[i] != player:
                all_match = False
                break
        if all_match:
            return True
    return False

def is_full(board):
    return " " not in board

def available_moves(board):
    return [i for i in range(len(board)) if board[i] == " "]

def minimax(board, is_maximizing):
    if winner(board, "O"):
        return 1
    elif winner(board, "X"):
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for move in available_moves(board):
            board[move] = "O"
            score = minimax(board, False)
            board[move] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in available_moves(board):
            board[move] = "X"
            score = minimax(board, True)
            board[move] = " "
            best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -float('inf')
    move = None
    for i in available_moves(board):
        board[i] = "O"
        score = minimax(board, False)
        board[i] = " "
        if score > best_score:
            best_score = score
            move = i
    return move

def update_score_label():
    score_label.config(text=f"Score - You (X): {player_x_score} | AI (O): {player_o_score}")

def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}")
        root.after(1000, update_timer)  # Call every 1000 ms (1 second)
    else:
        messagebox.showinfo("Game Over", "Time's up!")
        reset_game()

def on_click(i):
    global player_x_score, player_o_score
    if board[i] == " ":
        board[i] = "X"
        buttons[i].config(text="X", state="disabled", disabledforeground=player_color)

        if winner(board, "X"):
            player_x_score += 1
            update_score_label()
            messagebox.showinfo("Game Over", "You win!")
            reset_game()
            return
        elif is_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
            return

        ai = best_move()
        board[ai] = "O"
        buttons[ai].config(text="O", state="disabled", disabledforeground=ai_color)

        if winner(board, "O"):
            player_o_score += 1
            update_score_label()
            messagebox.showinfo("Game Over", "AI wins!")
            reset_game()
            return
        elif is_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()

def reset_game():
    global board, time_left
    board = [" " for _ in range(9)]
    time_left = 30  # Reset timer
    timer_label.config(text=f"Time Left: {time_left}")  # Reset timer label
    for btn in buttons:
        btn.config(text=" ", state="normal", bg=btn_bg)
    update_score_label()
    update_timer()  # Restart the timer

# Create grid buttons
for i in range(9):
    btn = tk.Button(
        root, text=" ", font=btn_font, width=4, height=2,
        bg=btn_bg, activebackground=btn_active_bg,
        command=lambda i=i: on_click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

# Start the timer
update_timer()

# Start GUI
root.mainloop()
