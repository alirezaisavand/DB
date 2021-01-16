import PySimpleGUI as sg
import restaurant_query_handeler


def order_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("order id: " + row[0] + " customer name: " + row[1] + " preparing time: " + str(row[2]) + " order time: " + str(row[3]) +
                 " price: " + str(row[4]) + " arriving time" + str(row[5]))
    return l

def food_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("food id: " + row[0] + " food name: " + row[1])
    return l

def set_ready(user_token):

    while True:
        orders = restaurant_query_handeler.get_restaurant_orders(user_token, False, False, True)
        rows = []
        for order in orders:
            rows.append(order[:-1])
        l = order_rows_to_list(rows)
        print(l)
        layout = [
            [sg.Listbox(values=l, size=(70, 12), key='-LIST-', enable_events=True)],
            [sg.Button("home page"), sg.Button("back")]]
        window = sg.Window("restaurant app", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "back":
            window.close()
            return
        elif event == "home page":
            window.close()
            home_page(user_token)
        elif event == "-LIST-":
            order_id = values["-LIST-"][0].split()[0]
            #  client_query_handler.b
            restaurant_query_handeler.food_is_ready(order_id)

def increase_food(user_token):
    while True:
        print("increase food page")
        rows = restaurant_query_handeler.get_restaurant_foods(user_token)
        l = food_rows_to_list(rows)
        layout = [
            [sg.Listbox(values=l, size = (70, 12), key = '-LIST', enable_events=True)],
            [sg.Text("enter increasing amount: "), sg.InputText()],
            [sg.Button("home page"), sg.Button("back")]
        ]
        window = sg.Window("restaurant app", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "back":
            window.close()
            return
        elif event == "home page":
            window.close()
            home_page(user_token)
        elif event == "-LIST-":
            food_id = values["-LIST-"][0].split()[0]
            amount = int(values[0])
            restaurant_query_handeler.increase_amount(food_id, amount)

def home_page(user_token):
    while True:
        print("welcome")
        user_data = restaurant_query_handeler.get_restaurant_info(user_token)
        # SELECT id,name,area,phone_number,balance
        layout = [
            [sg.Button("set ready", size=(20, 2))],
            [sg.Button("increase food", size=(20, 2))],
            [sg.Button("add new food", size=(20, 2))] ,
            [sg.Button("set delivery", size=(20, 2))],
            [sg.Button("my orders", size=(20, 2))],
            [sg.Button("back", size=(20, 2))]
        ]
        window = sg.Window("restaurant app", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "back":
            window.close()
            return

        elif event == "set ready":
            window.close()
            set_ready(user_token)
        elif event == "increase food":
            window.close()
            increase_food(user_token)


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
            [sg.Button('ok'), sg.Button("back")]]
        window = sg.Window("restaurant app", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "back":
            window.close()
            return
        elif event == "ok":
            restaurant_query_handeler.add_restaurant(values[0], values[1], values[2], values[3], values[4], values[5], values[6])
            window.close()
            initial_screen()

def initial_screen():
    wrong_info = 0
    while True:
        layout = [[sg.Text('Enter username'), sg.InputText()],
                  [sg.Text('Enter password'), sg.InputText()],
                  [sg.Button('ok', size=(10, 1)), sg.Button('sign up', size=(10, 1))]]
        if wrong_info:
            layout.append([sg.Text("Wrong information")])
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
initial_screen()