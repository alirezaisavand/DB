import PySimpleGUI as sg
import delivery_query_handeler

def check_complete(values):
    for i in range(len(values)):
        if values[i].strip() == '':
            return False
    return True

def my_orders (id):
    while True:
        layout = [
            [sg.Button("Back", size = (20, 1))]
        ]

        window = sg.Window("Delivery App", layout)

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)

        if event == "Back":
            window.close()
            return

def home_page(id):
    while True:
        layout = [
            [sg.Button("My Orders", size=(20, 1))],
            [sg.Button("Back", size=(20, 1))]
        ]

        window = sg.Window("Delivery App", layout)

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)

        if event == "Back":
            window.close()
            return

        if event == "My Orders":
            window.close()
            my_orders(id)



def sign_up():
    incomplete = 0
    while True:
        layout = [
            [sg.Text('Enter Name',size=(20, 1)), sg.InputText()],
            [sg.Text('Enter Salary',size=(20, 1)), sg.InputText()],
            [sg.Text('Enter Area',size=(20, 1)), sg.InputText()],
            [sg.Button('OK',size=(10, 1)), sg.Button("Back",size=(10, 1))]
        ]

        if incomplete:
            layout.append([sg.Text('Please Fill Inputs', text_color='red')])

        window = sg.Window("Delivery App", layout)

        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)

        elif event == "Back":
            window.close()
            return

        elif event == "OK":
            if check_complete(values):
                incomplete = 0
                delivery_query_handeler.add_new_delivery(values[0], values[1], values[2])
                print("Delivery Added")
                window.close()
                return
            else:
                incomplete = 1
            window.close()

def initial_screen():
    wrong_info = 0
    while True:
        layout = [[sg.Text('Enter Name',size=(20, 1)), sg.InputText()],
                  [sg.Button('OK', size=(10, 1)), sg.Button('Sign Up', size=(10, 1))]]

        if wrong_info:
            layout.append([sg.Text("Wrong Information", text_color='red')])

        window = sg.Window("Delivery App", layout)

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)

        if event == "OK":
            my_token = delivery_query_handeler.check_name(values[0])
            if my_token == -1:
                print("Wrong Information")
                wrong_info = 1
            else:
                wrong_info = 0
                window.close()
                home_page(my_token)
            window.close()
        elif event == "Sign Up":
            wrong_info = 0
            window.close()
            sign_up()

sg.theme('DarkTeal9')
initial_screen()