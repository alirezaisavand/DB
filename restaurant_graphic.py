import PySimpleGUI as sg
import restaurant_query_handeler

def home_page(user_token):
    while True:



def sign_up():
    while True:
        layout = [
            [sg.Text('Enter username'), sg.InputText()],
            [sg.Text('Enter password'), sg.InputText()],
            [sg.Text('Enter name'), sg.InputText()],
            [sg.Text('Enter area'), sg.InputText()],
            [sg.Text('Enter phone number'), sg.InputText()],
            [sg.Text('Enter type'), sg.InputText()],
            [sg.Text('Enter min order'), sg.InputText()],
            [sg.Button('ok'), sg.Button("<-back")]]
        window = sg.Window("restaurant app", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "<-back":
            window.close()
            return
        elif event == "ok":
            restaurant_query_handeler.add_restaurant(values[0], values[1], values[2], values[3], values[4], values[5], values[6])
            window.close()
            initial_screen()

def initial_screen():
    wrong_info = 0
    while True:
        if not wrong_info:
            layout = [[sg.Text('Enter username'), sg.InputText()],
                  [sg.Text('Enter password'), sg.InputText()],
                  [sg.Button('ok'), sg.Button('sign up'), sg.Button("<-back")]]
        else:
            layout = [[sg.Text('Enter username'), sg.InputText()],
                      [sg.Text('Enter password'), sg.InputText()],
                      [sg.Button('ok'), sg.Button('sign up'), sg.Button("<-back")],
                      [sg.Text("Wrong information")]]
        window = sg.Window("restaurant app", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        if event == "ok":
            my_token = restaurant_query_handeler.check_user_pass(values[0], values[1])
            if my_token == -1:
                print("wrong Information")
                wrong_info = 1
            else:
                wrong_info = 0
                window.close()
                home_page(my_token)
        elif event == "sign up":
            wrong_info = 0
            window.close()
            sign_up()
        elif event == "<-back":
            wrong_info = 0
            window.close()
            return

initial_screen()