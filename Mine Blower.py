import tkinter
import random
import time

#The emojis!
death_expanded = u"\u2620\uFE0F"
death = "☠️"
warning_expanded = u"\u26A0\uFE0F"
warning = "⚠️"
clock = "⏱"

def update_clock():
    global timer_label
    global time_played
    time_played = time_played + 1
    timer_label.configure(text=clock +str(time_played))
    if not gameOver:
        window.after(1000, update_clock)

def init():
    global gameOver
    global score
    global squaresToClear
    global bombfield
    global time_played
    global first_click
    global bombs_left
    gameOver = False
    score = 0
    squaresToClear = 0
    time_played = 0
    first_click = True
    bombs_left = 0

def play_bombdodger():
    init()
    global window
    create_bombfield()
    window = tkinter.Tk()
    window.geometry("620x650")
    layout_window(window)
    window.after(1000, update_clock)
    window.mainloop()

def show_bombs_left():
    global bombs_label
    bombs_label.config(text="Bombs left " + str(bombs_left))

def create_bombfield():
    global squaresToClear
    global bombfield
    global bombs_left
    bombfield = []
    for row in range(0,10):
        rowList = []
        for column in range(0,10):
            if random.randint(1,100) < 20:
                rowList.append(1)
                bombs_left = bombs_left + 1

            else:
                rowList.append(0)
                squaresToClear = squaresToClear + 1
        bombfield.append(rowList)
    #printfield(bombfield)

def printfield(bombfield):
    for rowList in bombfield:
        print(rowList)

def restart():
    show("Restart!")
    window.destroy()
    play_bombdodger()
    window.mainloop()

def layout_window(window):

    global main_frame
    top_frame = tkinter.Frame(window)
    main_frame = tkinter.Frame(window)

    top_frame.grid(row=0, sticky="")
    main_frame.grid(row=1, sticky="nsew")

    global score_label
    score_label = tkinter.Label(top_frame, text="SCORE", fg="black", font=("Phosphate", 18))
    score_label.grid(row=0, column=0)

    global timer_label
    timer_label = tkinter.Label(top_frame, text="0", fg="black", font=("Phosphate", 18))
    timer_label.grid(row=0, column=1)

    global bombs_label
    bombs_label = tkinter.Label(top_frame, text="Bombs left", fg="black", font=("Phosphate", 18))
    bombs_label.grid(row=0, column=2)
    show_bombs_left()

    restart_button = tkinter.Button(top_frame, text ="Retry", command = restart)
    restart_button.grid(row=0, column=3)

    for rowNumber, rowList in enumerate(bombfield):
        for columnNumber, columEntry in enumerate(rowList):
            if random.randint(1,100) < 25:
                bgcolor = "darkgreen"
            elif random.randint(1,100) > 75:
                bgcolor = "seagreen"
            else:
                bgcolor = "green"
            square = tkinter.Label(main_frame, bg = bgcolor, height=4, width=8, font=("Arial", 12))
            square.grid(row = rowNumber, column = columnNumber)
            square.grid(row = rowNumber, column = columnNumber)
            square.bind("<Button-1>", on_click)
            square.bind("<Button-2>",on_right_click)

def show(text):
    score_label.config(text = text)

def on_click(event):
    global score
    global gameOver
    global squaresToClear
    global first_click
    global main_frame

    square = event.widget
    row = int(square.grid_info()["row"])
    column = int(square.grid_info()["column"])

    currentText = square.cget("text")

    if gameOver == False:
        if first_click:
            #Ensure first click is never a bomb!
            first_click = False
            while bombfield[row][column] == 1:
                 create_bombfield()


        if warning in currentText:
            pass
        elif bombfield[row][column] == 1:
            gameOver = True
            red = "#FF6040"
            for r in range(0,170):
                for c in range(0,10):
                    if bombfield[r][c] == 1:
                        #print("found bomb")
                        tk_square = main_frame.grid_slaves(row=r, column=c)[0]
                        if r == row and c == column:
                            bg = "red"
                        else:
                            bg = "#808080"
                        tk_square.config(bg = bg, text = death, height=1, width=1, font=("Arial", 28))
            show("Game Over! Your score was: " + str(score))

        elif currentText == "":
            square.config(bg = "light blue")
            totalBombs = 0

            if row < 9:
                if bombfield[row+1][column] == 1:
                    totalBombs = totalBombs + 1

            if row > 0:
                if bombfield[row-1][column] == 1:
                    totalBombs = totalBombs + 1

            if column > 0:
                if bombfield[row][column-1] == 1:
                    totalBombs =totalBombs + 1

            if column < 9:
                if bombfield[row][column+1] == 1:
                    totalBombs = totalBombs + 1

            if row > 0 and column > 0:
                if bombfield[row-1][column-1] == 1:
                    totalBombs = totalBombs + 1

            if row < 9 and column > 0:
                if bombfield[row+1][column-1] == 1:
                    totalBombs = totalBombs + 1
            if row > 0 and column < 9:
                if bombfield[row-1][column+1] == 1:
                    totalBombs = totalBombs +1

            if row < 9 and column < 9:
                if bombfield[row+1][column+1] == 1:
                    totalBombs = totalBombs + 1

            if totalBombs != 0:
                num_text = str(totalBombs)
            else:
                num_text = ""

            square.config(text = " " + num_text + " ")

            squaresToClear = squaresToClear - 1
            score = score + 1

            show("Score: " + str(score))

            if squaresToClear == 0:
                gameOver = True
                show("Congratulations! Your score was: " + str(score))

            if totalBombs == 0:
                print("should clear all squares around this")

def on_right_click(event):
    global bombs_left
    square = event.widget
    currentText = square.cget("text")

    if warning in currentText:
        square.config(bg = "green", text = "", height=4, width=8, font=("Arial", 12))
        bombs_left = bombs_left + 1
    elif currentText == "":
        row = int(square.grid_info()["row"])
        column = int(square.grid_info()["column"])
        square.config(bg = "white", height=1, width=1, text = warning, font=("Arial", 28))
        bombs_left = bombs_left - 1

    show_bombs_left()


play_bombdodger()
