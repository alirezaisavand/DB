import PySimpleGUI as sg
import restaurant_query_handeler

def check_complete(values):
    for i in range(len(values)):
        if values[i].strip() == '':
            return False
    return True

def delivery_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("Delivery Id: " + row[0] + " Name: " + row[1] + " Area: " + row[2])
    return l

def order_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("Order Id: " + row[0] + " Customer Name: " + row[1] + " Preparing Time: " + str(row[2]) + " Order Time: " + str(row[3]) +
                 " Price: " + str(row[4]) + " Arriving Time" + str(row[5]))
    return l

def food_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("Food Id: " + row[0] + " Food Name: " + row[1])
    return l

def order_details(user_token, order_id):

    while True:
        food_names = restaurant_query_handeler.get_order_food_names(order_id)
        show_number = min(len(food_names), 12)

        layout = [
            [sg.Listbox(values=food_names, size=(70, show_number), key='-LIST-', enable_events=False)],
            [sg.Button("Home Page", size=(10, 1)), sg.Button("Back", size=(10, 1))]
        ]
        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return
        elif event == "Home Page":
            window.close()
            home_page(user_token)

def my_orders(user_token):
    filter_ready = False
    filter_set = False
    filter_arrived = False
    while True:
        orders = restaurant_query_handeler.get_restaurant_orders(user_token, filter_arrived, filter_set, filter_ready)
        l = order_rows_to_list(orders)
        show_number = min(len(l), 12)
        print(l)
        layout = [
            [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
            [sg.Checkbox("Filter Ready", size=(20, 1), key="-READY-", enable_events=True, default=filter_ready)],
            [sg.Checkbox("Filter Arrived", size=(20, 1), key="-ARRIVED-", enable_events=True, default=filter_arrived)],
            [sg.Checkbox("Filter Set Delivery", size=(20, 1), key="-SET-", enable_events=True, default=filter_set)],
            [sg.Button("Home Page", size=(10, 1)), sg.Button("Back", size=(10, 1))]
        ]
        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return
        elif event == "Home Page":
            window.close()
            home_page(user_token)
        elif event == "-READY-":
            window.close()
            filter_ready = values["-READY-"]
        elif event == "-ARRIVED-":
            window.close()
            filter_arrived = values["-ARRIVED-"]
        elif event == "-SET-":
            window.close()
            filter_set = values["-SET-"]
        elif event == "-LIST-":
            if show_number > 0:
                order_id = values["-LIST-"][0].split()[2]
            #  client_query_handler.b
                window.close()
                order_details(user_token, order_id)

def set_ready(user_token):

    while True:
        orders = restaurant_query_handeler.get_restaurant_orders(user_token, False, False, True)
        l = order_rows_to_list(orders)
        show_number = min(len(l), 12)
        print(l)
        layout = [
            [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
            [sg.Button("Home Page", size=(10, 1)), sg.Button("Back", size=(10,1))]]
        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return
        elif event == "Home Page":
            window.close()
            home_page(user_token)
        elif event == "-LIST-":
            if show_number > 0:
                order_id = values["-LIST-"][0].split()[2]
            #  client_query_handler.b
                restaurant_query_handeler.food_is_ready(order_id)
                window.close()

def increase_food(user_tOKen):
    incomplete = 0
    while True:
        print("increase food page")
        rows = restaurant_query_handeler.get_restaurant_foods(user_tOKen)
        l = food_rows_to_list(rows)
        show_number = min(12, len(l))
        layout = []
        if incomplete:
            layout = [
                [sg.Text("Please Fill Inputs Correctly", text_color='red')],
                [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
                [sg.Text("Enter Increasing Amount: "), sg.InputText()],
                [sg.Button("Home Page", size=(10, 1)), sg.Button("Back", size=(10, 1))]
            ]
        else:
            layout = [
                [sg.Listbox(values=l, size = (70, show_number), key = '-LIST-', enable_events=True)],
                [sg.Text("Enter Increasing Amount: "), sg.InputText()],
                [sg.Button("Home page", size=(10, 1)), sg.Button("Back", size=(10,1))]
            ]

        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return
        elif event == "Home Page":
            incomplete = 0
            window.close()
            home_page(user_tOKen)
        elif event == "-LIST-":
            food_id = values["-LIST-"][0].split()[2]
            if not values[0].isnumeric():
                print("Incomplete")
                incomplete = 1
            else:
                incomplete = 0
                amount = int(values[0])
                print(amount, " :amount ")
                restaurant_query_handeler.increase_amount(food_id, amount)
            window.close()

def add_new_food(user_tOKen):
    incomplete = 0
    while True:
        layout = [
        [sg.Text('Enter Name', size=(20, 1)), sg.InputText()],
        [sg.Text('Enter Type', size=(20, 1)), sg.InputText()],
        [sg.Text('Enter Description', size=(20, 1)), sg.InputText()],
        [sg.Text('Enter Price', size=(20, 1)), sg.InputText()],
        [sg.Button('OK', size=(10, 1)), sg.Button("Back", size=(10,1))]
        ]
        if incomplete:
            layout.append([sg.Text('Please Fill Inputs', text_color='red')])
        window = sg.Window("Restaurant App", layout, auto_size_text=True, auto_size_buttons=True)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return
        elif event == "OK":
            print(values)
            if check_complete(values):
                incomplete = 0
                restaurant_query_handeler.add_food_to_restaurant(user_tOKen, values[0], values[1], values[2], values[3])
            else:
                incomplete = 1
            window.close()

def choose_delivery_for_order(user_token, order_id):
    while True:
        deliveries = restaurant_query_handeler.get_free_deliveries(user_token)
        l = delivery_rows_to_list(deliveries)
        show_number = min(len(l), 12)
        print(l)
        layout = [
            [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
            [sg.Button("Home Page", size=(10, 1)), sg.Button("Back", size=(10, 1))]]
        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return
        elif event == "Home Page":
            window.close()
            home_page(user_token)
        elif event == "-LIST-":
            if show_number > 0:
                delivery_id = values["-LIST-"][0].split()[2]
                #  client_query_handler.b
                restaurant_query_handeler.set_delivery_for_order(order_id, delivery_id)
                window.close()
                return


def set_delivery(user_token):
    while True:
        orders = restaurant_query_handeler.get_restaurant_orders(user_token, False, True, False)
        l = order_rows_to_list(orders)
        show_number = min(len(l), 12)
        print(l)
        layout = [
            [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
            [sg.Button("Home Page", size=(10, 1)), sg.Button("Back", size=(10,1))]]
        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return
        elif event == "Home Page":
            window.close()
            home_page(user_token)
        elif event == "-LIST-":
            if show_number > 0:
                order_id = values["-LIST-"][0].split()[2]
            #  client_query_handler.b
                window.close()
                choose_delivery_for_order(user_token, order_id)

def home_page(user_token):
    while True:
        print("welcome")
        user_data = restaurant_query_handeler.get_restaurant_info(user_token)
        # SELECT id,name,area,phone_number,balance
        layout = [
            [sg.Button("Set Ready", size=(20, 2))],
            [sg.Button("Increase Food", size=(20, 2))],
            [sg.Button("Add New Food", size=(20, 2))] ,
            [sg.Button("Set Delivery", size=(20, 2))],
            [sg.Button("My Orders", size=(20, 2))],
            [sg.Button("Back", size=(20, 2))]
        ]
        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return

        elif event == "Set Ready":
            window.close()
            set_ready(user_token)
        elif event == "Increase Food":
            window.close()
            increase_food(user_token)
        elif event == "Add New Food":
            window.close()
            add_new_food(user_token)
        elif event == "Set Delivery":
            window.close()
            set_delivery(user_token)
        elif event == "My Orders":
            window.close()
            my_orders(user_token)

def sign_up():
    incomplete = 0
    while True:
        layout = [
            [sg.Text('Enter Username',size=(20, 1)), sg.InputText()],
            [sg.Text('Enter Password',size=(20, 1)), sg.InputText()],
            [sg.Text('Enter Name',size=(20, 1)), sg.InputText()],
            [sg.Text('Enter Area',size=(20, 1)), sg.InputText()],
            [sg.Text('Enter Phone Number',size=(20, 1)), sg.InputText()],
            [sg.Text('Enter Type',size=(20, 1)), sg.InputText()],
            [sg.Text('Enter Min Order',size=(20, 1)), sg.InputText()],
            [sg.Button('OK',size=(10, 1)), sg.Button("Back",size=(10, 1))]]
        if incomplete:
            layout.append([sg.Text('Please Fill Inputs', text_color='red')])
        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "Back":
            window.close()
            return
        elif event == "OK":
            if check_complete(values):
                incomplete = 0
                restaurant_query_handeler.add_restaurant(values[0], values[1], values[2], values[3], values[4], values[5], values[6])
                window.close()
                initial_screen()
            else:
                incomplete = 1
                window.close()


def initial_screen():
    wrong_info = 0
    while True:
        layout = [[sg.Text('Enter Username',size=(20, 1)), sg.InputText()],
                  [sg.Text('Enter Password',size=(20, 1)), sg.InputText()],
                  [sg.Button('OK', size=(10, 1)), sg.Button('Sign Up', size=(10, 1))]]
        if wrong_info:
            layout.append([sg.Text("Wrong Information", text_color='red')])
        window = sg.Window("Restaurant App", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        if event == "OK":
            my_tOKen = restaurant_query_handeler.check_user_pass(values[0], values[1])
            if my_tOKen == -1:
                print("wrong Information")
                wrong_info = 1
            else:
                wrong_info = 0
                window.close()
                home_page(my_tOKen)
            window.close()
        elif event == "Sign Up":
            wrong_info = 0
            window.close()
            sign_up()
sg.theme('DarkTeal9')
initial_screen()