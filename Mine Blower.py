import tkinter
import random
import time
import platform

#The emojis!
warning_expanded = u"\u26A0\uFE0F"
warning = "⚠️"
death_expanded = u"\u2620\uFE0F"
death = "☠️"
clock = "⏱"

def square_to_widget(row, column):
    global main_frame
    
    widget = main_frame.grid_slaves(row, column)[0]
    return widget

def square_open(r, c, text, auto=True):
    global first_mine
    
    tk_square = square_to_widget(r, c)
    if text == death:
        square_text = tk_square.cget("text")
        if auto == False:
            bg = "red"
        elif warning in square_text:
            bg = "light blue"
        else:
            bg = "#808080"
    else:
        bg = "light blue"
    if text == death and first_mine:
        # Avoid tkinter (3.7.3) on windows bug
        # when displaying skull with emoji variant selector.
        # Displaying warning (with variant selector) first, avoids the issue.
        first_mine = False
        tk_square.config(bg = bg, text = warning, height=1, width=2)
    tk_square.config(bg = bg, text = text, height=1, width=2)

def update_clock():
    global timer_label
    global time_played
    global timer
    if not gameOver:
        timer_label.configure(text=clock +str(time_played))
        time_played = time_played + 1
        timer = window.after(1000, update_clock)

def init():
    global gameOver
    global time_played
    global first_click
    global first_mine
    global timer
    gameOver = False
    time_played = 0
    first_click = True
    first_mine = True
    timer = None

def play_bombdodger():
    global window
    init()
    create_bombfield()
    window = tkinter.Tk()
    window.geometry("620x650")
    layout_window(window)
    window.mainloop()

def show_bombs_left():
    global bombs_label
    global bombs_left
    global first_click

    if first_click:
        # Never change number upon first click
        number = "??"
    else:
        number = bombs_left
        
    bombs_label.config(text="Bombs left " + str(number))

def create_bombfield():
    global squares_left
    global bombfield
    global bombs_left

    bombs_left = 0
    squares_left = 0
    bombfield = []
    
    for row in range(0,10):
        rowList = []
        for column in range(0,10):
            if random.randint(1,100) < 20:
                rowList.append(1)
                bombs_left = bombs_left + 1
            else:
                rowList.append(0)
            squares_left = squares_left + 1
        bombfield.append(rowList)
    #printfield(bombfield)

def printfield(bombfield):
    for rowList in bombfield:
        print(rowList)

def restart():
    global timer
    if timer:
        window.after_cancel(timer)
    window.destroy()
    play_bombdodger()
    window.mainloop()

def layout_window(window):

    global main_frame
    top_frame = tkinter.Frame(window)
    main_frame = tkinter.Frame(window)

    top_frame.grid(row=0, sticky="")
    main_frame.grid(row=1, sticky="nsew")

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
            square = tkinter.Label(main_frame, relief="raised", bg = bgcolor, height=1, width=2, font=("Arial", 20))
            square.grid(row = rowNumber, column = columnNumber)
            square.grid(row = rowNumber, column = columnNumber)
            square.bind("<Button-1>", on_click)
            square.bind("<Control-Button-1>", on_right_click)
            if platform.system() == "Darwin":
                square.bind("<Button-2>", on_right_click)
            else:
                square.bind("<Button-2>", on_click)
                square.bind("<Button-3>", on_right_click)

def check_game_over():
    global squares_left
    global gameOver
    
    if squares_left == 0:
        gameOver = True

def surrounding_squares(row, column):
    max_row = 9
    max_col = 9

    squares = []

    if row < max_row:
        squares.append((row+1, column))
    if row > 0:
        squares.append((row-1, column))
    if column > 0:
        squares.append((row, column-1))
    if column < max_col:
        squares.append((row, column+1))
    if row > 0 and column > 0:
        squares.append((row-1, column-1))
    if row < max_row and column > 0:
        squares.append((row+1, column-1))
    if row > 0 and column < max_col:
        squares.append((row-1, column+1))
    if row < max_row and column < max_col:
        squares.append((row+1, column+1))

    return squares

def on_click(event):
    square = event.widget
    click(square)
    
def click(square, auto=False, click_flag=False):
    global gameOver
    global squares_left
    global first_click
    global main_frame

    row = int(square.grid_info()["row"])
    column = int(square.grid_info()["column"])

    currentText = square.cget("text")

    if gameOver == False:
        if first_click:
            #Ensure first click is never a bomb!
            first_click = False
            while bombfield[row][column] == 1:
                 create_bombfield()
            show_bombs_left()
            update_clock()

        if warning in currentText:
            if click_flag==True:
                right_click(square)
                click(square)
        elif bombfield[row][column] == 1:
            gameOver = True
            red = "#FF6040"
            for r in range(0,10):
                for c in range(0,10):
                    if bombfield[r][c] == 1:
                        square_open(r, c, text=death, auto = (r != row or c != column))

        elif currentText == "":
            totalBombs = 0
            
            squares_around = surrounding_squares(row, column)
            for r,c in squares_around:
                totalBombs += bombfield[r][c]

            if totalBombs != 0:
                num_text = str(totalBombs)
            else:
                num_text = ""
                
            square_open(row, column, text = " " + num_text + " ", auto=False)   

            squares_left = squares_left - 1

            check_game_over()

            if totalBombs == 0:
                for r,c in squares_around:
                    tk_square = square_to_widget(r, c)
                    click(tk_square, auto=True, click_flag=True)
        elif auto == False:  # clicking on a number
            squares_around = surrounding_squares(row, column)
            flag_count = 0
            for r,c in squares_around:
                tk_square = square_to_widget(r, c)
                square_text = tk_square.cget("text")
                if warning in square_text:
                    flag_count = flag_count + 1   
            if int(currentText) == flag_count:
                for r,c in squares_around:
                    tk_square = square_to_widget(r, c)
                    click(tk_square, auto=True)
                    
                    
def on_right_click(event):
    square = event.widget
    right_click(square)

def right_click(square):
    global bombs_left
    global squares_left
    global first_click
    
    currentText = square.cget("text")

    if warning in currentText:
        square.config(bg = "green", text = "", height=1, width=2)
        bombs_left = bombs_left + 1
        squares_left = squares_left + 1
    elif currentText == "" and not first_click and bombs_left > 0:
        row = int(square.grid_info()["row"])
        column = int(square.grid_info()["column"])
        square.config(bg = "light blue", height=1, width=2, text = warning)
        bombs_left = bombs_left - 1
        squares_left = squares_left - 1
        check_game_over()
        
    show_bombs_left()


play_bombdodger()
