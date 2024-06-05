from tkinter import *
from tkinter import messagebox
import winsound
import keyboard
from decimal import Decimal
import math

root = Tk()
root.geometry("390x377")
root.resizable(0, 0)
root.title("KALKULATOR")

# Kolory do trybów
light_mode_colors = {
    "bg": "#FFFFFF",
    "fg": "#000000",
    "btn_bg": "#EEEEEE",
    "btn_fg": "#000000"
}

dark_mode_colors = {
    "bg": "#000000",
    "fg": "#FFFFFF",
    "btn_bg": "#222222",
    "btn_fg": "#FFFFFF"
}

# Na początku jasny
current_colors = light_mode_colors

messagebox.showinfo("Witaj!", "To jest kalkulator, jest on w stanie wykonywać podstawowe obliczenia i przeliczać liczby na system binarny w kodzie U2 lub znak-moduł.")
expression = ""
input_text = StringVar()
def show_info():
    messagebox.showinfo("Witaj!",
                        "To jest kalkulator, jest on w stanie wykonywać podstawowe obliczenia i przeliczać liczby na system binarny w kodzie U2 lub znak-moduł.")
def play_sound():
    winsound.PlaySound("klik.wav", winsound.SND_ASYNC)


def btn_click(item):
    global expression
    if len(expression) > 0 and expression[-1] in ['+', '-', '*', '/', '.']:
        if item in ['+', '-', '*', '/', '.']:
            return

    expression += str(item)
    input_text.set(expression)
    play_sound()

def btn_backspace():
    global expression
    expression = expression[:-1]
    input_text.set(expression)
    play_sound()

def btn_clear():
    global expression
    expression = ""
    input_text.set("")
    play_sound()

def btn_equal():
    global expression
    try:
        expression_decimal = expression.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ')
        parts = expression_decimal.split()
        decimal_expression = ' '.join(['Decimal("' + part + '")' if part.replace('.', '', 1).isdigit() else part for part in parts])
        result = str(eval(decimal_expression))
        input_text.set(result)
        expression = result
        play_sound()
    except ZeroDivisionError:
        input_text.set("Nie dziel przez zero!")
        messagebox.showerror("Ostrzeżenie", "Nie dziel przez zero!")
        expression = ""
        play_sound()
    except Exception as e:
        input_text.set("Błąd")
        expression = ""
        play_sound()

def to_binary_u2(decimal_num, num_bits):
    if decimal_num >= 0 and decimal_num <= 127:
        binary_num = bin(decimal_num)[2:].zfill(num_bits)
        play_sound()
    elif decimal_num <= 0 and decimal_num >= -128:
        binary_num = bin(decimal_num & int("1"*num_bits, 2))[2:]
        binary_num = binary_num.zfill(num_bits-1)
        play_sound()
    else:
        messagebox.showerror("Ostrzeżenie", "Kalkulator korzysta z 8-bitowych liczb binarnych kod U2 (zakres od -128 do 127)")
        binary_num = "Nieprawidłowy zakres"
        play_sound()
    return binary_num

def to_binary_znak_modul(decimal_num, num_bits):
    if 0 <= decimal_num <= 127:
        binary_num = bin(decimal_num)[2:].zfill(num_bits)
        play_sound()
    elif 0 >= decimal_num >= -127:
        binary_num = bin(-decimal_num)[2:].zfill(num_bits)
        binary_num = "1" + binary_num[1:]
        play_sound()
    else:
        messagebox.showerror("Ostrzeżenie", "Kalkulator korzysta z 8-bitowych liczb binarnych znak-moduł (zakres od -127 do 127)")
        binary_num = "Nieprawidłowy zakres"
        play_sound()
    return binary_num

def convert_to_u2():
    global expression
    try:
        decimal_num = eval(expression)
        binary_u2 = to_binary_u2(decimal_num, 8)  # wynik w 8 bitach
        input_text.set(binary_u2)
        expression = ""
        play_sound()
    except:
        input_text.set("Error")
        expression = ""
        play_sound()

def convert_to_znak_modul():
    global expression
    try:
        decimal_num = eval(expression)
        binary_znak_modul = to_binary_znak_modul(decimal_num, 8)  # wynik w 8 bitach
        input_text.set(binary_znak_modul)
        expression = ""
        play_sound()
    except:
        input_text.set("Error")
        expression = ""
        play_sound()

def toggle_mode():
    global current_colors
    if current_colors == light_mode_colors:
        current_colors = dark_mode_colors
        play_sound()
    else:
        current_colors = light_mode_colors
        play_sound()
    apply_color_scheme()

def apply_color_scheme():
    root.configure(bg=current_colors["bg"])
    for widget in btns_frame.winfo_children():
        if isinstance(widget, Button):
            widget.configure(bg=current_colors["btn_bg"], fg=current_colors["btn_fg"])

def calculate_sqrt():
    global expression
    try:
        result = str(math.sqrt(eval(expression)))
        input_text.set(result)
        expression = result
        play_sound()
    except Exception as e:
        input_text.set("Błąd")
        expression = ""
        play_sound()

keyboard.add_hotkey('1', lambda: btn_click(1))
keyboard.add_hotkey('2', lambda: btn_click(2))
keyboard.add_hotkey('3', lambda: btn_click(3))
keyboard.add_hotkey('4', lambda: btn_click(4))
keyboard.add_hotkey('5', lambda: btn_click(5))
keyboard.add_hotkey('6', lambda: btn_click(6))
keyboard.add_hotkey('7', lambda: btn_click(7))
keyboard.add_hotkey('8', lambda: btn_click(8))
keyboard.add_hotkey('9', lambda: btn_click(9))
keyboard.add_hotkey('0', lambda: btn_click(0))
keyboard.add_hotkey('.', lambda: btn_click("."))
keyboard.add_hotkey(',', lambda: btn_click("."))
keyboard.add_hotkey('/', lambda: btn_click("/"))
keyboard.add_hotkey('*', lambda: btn_click("*"))
keyboard.add_hotkey('-', lambda: btn_click("-"))
keyboard.add_hotkey('+', lambda: btn_click("+"))
keyboard.add_hotkey('Enter', lambda: btn_equal())
keyboard.add_hotkey('Backspace', lambda: btn_backspace())
keyboard.add_hotkey('C', lambda: btn_clear())
keyboard.add_hotkey('Ctrl+1', lambda: convert_to_znak_modul())
keyboard.add_hotkey('Ctrl+2', lambda: convert_to_u2())
keyboard.add_hotkey('S', lambda: calculate_sqrt())
keyboard.add_hotkey('(', lambda: btn_click("("))
keyboard.add_hotkey(')', lambda: btn_click(")"))

# Ramka do działań
input_frame = Frame(root, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
input_frame.pack(side=TOP)

# Czcionka i readonly żeby przypadkiem nie popsuć
input_field = Entry(input_frame, font=('arial', 18, 'bold'), textvariable=input_text, width=50, bg="#eee", bd=0, justify=RIGHT, state="readonly")
input_field.grid(row=0, column=0)
input_field.pack(ipady=10)

btns_frame = Frame(root, width=312, height=272.5, bg="grey")
btns_frame.pack()

clear = Button(btns_frame, text="Czyść", fg="black", width=21, height=3, bd=0, bg="#eee", cursor="hand2", command=btn_clear)
clear.grid(row=0, column=1, columnspan=2, padx=1, pady=1)

divide = Button(btns_frame, text="/", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("/"))
divide.grid(row=0, column=3, padx=1, pady=1)

convert_u2_btn = Button(btns_frame, text="U2", fg="black", width=21, height=3, bd=0, bg="#eee", cursor="hand2", command=convert_to_u2)
convert_u2_btn.grid(row=6, column=2, columnspan=2, padx=1, pady=1)

convert_znak_modul_btn = Button(btns_frame, text="Znak-moduł", fg="black", width=21, height=3, bd=0, bg="#eee", cursor="hand2", command=convert_to_znak_modul)
convert_znak_modul_btn.grid(row=6, column=0, columnspan=2, padx=1, pady=1)

backspace_btn = Button(btns_frame, text="⌫", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=btn_backspace)
backspace_btn.grid(row=6, column=4, padx=1, pady=1)

sqrt_btn = Button(btns_frame, text="√", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=calculate_sqrt)
sqrt_btn.grid(row=0, column=4, padx=1, pady=1)

# Dodanie przycisków nawiasów
left_parenthesis = Button(btns_frame, text="(", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("("))
left_parenthesis.grid(row=1, column=4, padx=1, pady=1)

right_parenthesis = Button(btns_frame, text=")", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click(")"))
right_parenthesis.grid(row=2, column=4, padx=1, pady=1)

info = Button(btns_frame, text="Info", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: show_info())
info.grid(row=3, column=4, padx=1, pady=1)

seven = Button(btns_frame, text="7", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(7))
seven.grid(row=1, column=0, padx=1, pady=1)
eight = Button(btns_frame, text="8", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(8))
eight.grid(row=1, column=1, padx=1, pady=1)
nine = Button(btns_frame, text="9", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(9))
nine.grid(row=1, column=2, padx=1, pady=1)
multiply = Button(btns_frame, text="*", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("*"))
multiply.grid(row=1, column=3, padx=1, pady=1)

four = Button(btns_frame, text="4", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(4))
four.grid(row=2, column=0, padx=1, pady=1)
five = Button(btns_frame, text="5", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(5))
five.grid(row=2, column=1, padx=1, pady=1)
six = Button(btns_frame, text="6", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(6))
six.grid(row=2, column=2, padx=1, pady=1)
minus = Button(btns_frame, text="-", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("-"))
minus.grid(row=2, column=3, padx=1, pady=1)

one = Button(btns_frame, text="1", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(1))
one.grid(row=3, column=0, padx=1, pady=1)
two = Button(btns_frame, text="2", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(2))
two.grid(row=3, column=1, padx=1, pady=1)
three = Button(btns_frame, text="3", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(3))
three.grid(row=3, column=2, padx=1, pady=1)
plus = Button(btns_frame, text="+", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("+"))
plus.grid(row=3, column=3, padx=1, pady=1)

zero = Button(btns_frame, text="0", fg="black", width=21, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(0))
zero.grid(row=4, column=0, columnspan=2, padx=1, pady=1)
point = Button(btns_frame, text=".", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("."))
point.grid(row=4, column=2, padx=1, pady=1)
equals = Button(btns_frame, text="=", fg="black", width=21, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_equal())
equals.grid(row=4, column=3, columnspan=2, padx=1, pady=1)

mode_toggle_btn = Button(btns_frame, text="Tryb ciemny", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=toggle_mode)
mode_toggle_btn.grid(row=0, column=0, padx=1, pady=1)

apply_color_scheme()
root.mainloop()
