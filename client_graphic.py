# img_viewer.py

import PySimpleGUI as sg
import client_query_handler


def restaurant_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("name : " + row[1] + "---type : " + row[4] + "---score : " + str(row[6]))
    return l


def food_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("name: " + row[1] + "-type: " + row[2] + "-remain: " + str(row[3]) + "-price:" + str(
            row[5]) + "-score:" + str(row[7]))
    return l

def basket_food_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("name: " + row[0] + "-amount: " + str(row[1]))
    return l

def after_set_restaurant(user_data, user_token, restaurant_name):
    restaurant_id = client_query_handler.searchـrestaurant("name", restaurant_name)[0][0]

    rows = client_query_handler.search_food("restaurant_id", restaurant_id)
    l = food_rows_to_list(rows)
    print(l)
    layout = [
        [sg.Text('balance:' + str(user_data[4]))],
        [sg.Text(str(restaurant_name))],
        [sg.Listbox(values=l, size=(70, 12), key='-LIST-', enable_events=True)],
        [sg.Button("Done!"),sg.Button("home page")]]

    window = sg.Window("client app", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "home page":
            window.close()
            home_page(user_token)
        elif event == "-LIST-":
            window.close()
            food_name = values["-LIST-"][0].split()[1]
            # after enabling multisearch filter add restorant_id
            food_id = client_query_handler.search_food("name", food_name)[0][0]
            client_query_handler.order_food(user_token, restaurant_id, food_id)
            after_set_restaurant(user_data,user_token,restaurant_name)
        elif event == "Done!":
            window.close()
            home_page(user_token)


def my_basket(user_token,user_data):
    rows=client_query_handler.get_customer_basket(user_token)
    l = basket_food_rows_to_list(rows)
    print(l)
    layout = [
        [sg.Text('balance:' + str(user_data[4]))],
        [sg.Listbox(values=l, size=(70, 12), key='-LIST-', enable_events=True)],
        [sg.Button("buy!"),sg.Button("home page")]]

    window = sg.Window("client app", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "home page":
            window.close()
            home_page(user_token)
        elif event == "buy!":
            print("client.buy")
          #  client_query_handler.b
            window.close()
            home_page(user_token)


def order_food(user_data, user_token):
    rows = client_query_handler.searchـrestaurant("area", user_data[2])
    l = restaurant_rows_to_list(rows)
    print(l)
    layout = [
        [sg.Text('balance:' + str(user_data[4]))],
        [sg.Text('restaurant in your area')],
        [sg.Listbox(values=l, size=(70, 12), key='-LIST-', enable_events=True)],
        [sg.Button("home page")]]

    window = sg.Window("client app", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "home page":
            window.close()
            home_page(user_token)
        elif event == "-LIST-":
            window.close()
            after_set_restaurant(user_data, user_token, values["-LIST-"][0].split()[2])
        window.close()
        home_page(user_token)
        return

def my_order(user_token):
    rows=client_query_handler.get_customer_orders()
    print("NOT ComPLiTED:(")

def home_page(user_token):
    print("welcome")
    user_data = client_query_handler.get_client_info(user_token)
    # SELECT id,name,area,phone_number,balance
    layout = [
        [sg.Text('balance:' + str(user_data[4]))],
        [sg.Text('charge account'), sg.InputText(), sg.Button("charge")],
        [sg.Button("order food"),sg.Button("buy basket"),sg.Button("my orders")]]
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
        elif event == "my orders":
            window.close()
            my_order(user_token)
        elif event == "buy basket":
            window.close()
            my_basket(user_token,user_data)
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
