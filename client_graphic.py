# img_viewer.py

import PySimpleGUI as sg
import client_query_handler


def restaurant_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("name : " + row[1] + "---type : " + row[4] + "---score : " + row[6])
    return l


def food_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("name : " + row[1] + "---type : " + row[4] + "---score : " + row[6])
    return l


def after_set_restaurant(user_data, user_token, restaurant_name):
    print("injash monde!")


def order_food(user_data, user_token):
    rows = client_query_handler.searchـrestaurant("area", user_data[2])
    l = restaurant_rows_to_list(rows)
    layout = [
        [sg.Text('balance:' + str(user_data[4]))],
        [sg.Text('restaurant in your area')],
        [sg.Listbox(values=l, size=(20, 12), key='-LIST-', enable_events=True)],
        [sg.Button("best restaurant")]]

    window = sg.Window("client app", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "":
            client_query_handler.charge_account(user_token, int(values[0]))
            continue
        elif event == "order food":
            order_food(user_data, user_token)
        window.close()
        home_page(user_token)
        return


def home_page(user_token):
    print("welcome")
    user_data = client_query_handler.get_client_info(user_token)
    # SELECT id,name,area,phone_number,balance
    layout = [
        [sg.Text('balance:' + str(user_data[4]))],
        [sg.Text('charge account'), sg.InputText(), sg.Button("charge")],
        [sg.Button("order food")]]
    window = sg.Window("client app", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "charge":
            client_query_handler.charge_account(user_token, int(values[0]))
            window.close()
            home_page(user_token)
        elif event == "order food":
            window.close()
            order_food(user_data, user_token)
        window.close()
        home_page(user_token)
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
            exit(0)
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
            exit(0)
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
