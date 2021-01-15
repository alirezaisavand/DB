# img_viewer.py

import PySimpleGUI as sg
import client_query_handler

def order_food(user_token):
    print("omadi")


def home_page(user_token):
    print("welcome")
    user_data=client_query_handler.get_client_info(user_token)

    layout = [
        [sg.Text('balance:'+str(user_data[4]))],
        [sg.Text('charge account'), sg.InputText(),sg.Button("charge")],
        [sg.Button("order food")]]
    window = sg.Window("client app", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            return
        elif event == "charge":
            client_query_handler.charge_account(user_token,int(values[0]))
            continue
        elif event == "order food":
            order_food(user_token)
        window.close()
        initial_screen()
        return


def sing_up():
    layout = [
        [sg.Text('Enter username'), sg.InputText()],
        [sg.Text('Enter password'), sg.InputText()],
        [sg.Text('Enter name'), sg.InputText()],
        [sg.Text('Enter area'), sg.InputText()],
        [sg.Text('Enter phone_number'), sg.InputText()],
        [sg.Button('ok')]]
    window = sg.Window("client app", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            return
        # Folder name was filled in, make a list of files in the folder
        client_query_handler.add_customer(values[0], values[1], values[2], values[3], values[4])
        window.close()
        initial_screen()
        return


def initial_screen():
    layout = [[sg.Text('Enter username'), sg.InputText()],
              [sg.Text('Enter password'), sg.InputText()],
              [sg.Button('ok'), sg.Button('sing up')]]

    window = sg.Window("client app", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            return
        if event == "ok":
            my_token = client_query_handler.check_user_pass(values[0], values[1])
            if my_token == -1:
                layout = [[sg.Text('wrong user pass')],
                          [sg.Text('Enter username'), sg.InputText()],
                          [sg.Text('Enter password'), sg.InputText()],
                          [sg.Button('ok'), sg.Button('sing up')]]
                window.close()
                window = sg.Window("client app", layout)
            else:
                window.close()
                home_page(my_token)
        elif event == "sing up":
            window.close()
            sing_up()


initial_screen()
