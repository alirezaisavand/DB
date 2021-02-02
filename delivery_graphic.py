import PySimpleGUI as sg
import delivery_query_handeler

def check_complete(values):
    for i in range(len(values)):
        if values[i].strip() == '':
            return False
    return True

def basket_rows_to_list (basket):
    l = []

    for row in basket:
        l.append("order id: " + row[0])

    return l

def my_current_order (id):
    error = False
    while True:
        basket = delivery_query_handeler.find_delivery_basket(id, True, True)
        l = basket_rows_to_list(basket)

        show_number = min(len(l), 12)

        if error:
            layout = [
                [sg.Text("You don't have any order for Arriving", text_color='red')],
                [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
                [sg.Button("Back", size=(20, 1)), sg.Button("Order Arrived", size=(20, 1))]
            ]
        else:
            layout = [
                [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
                [sg.Button("Back", size=(20, 1)), sg.Button("Order Arrived", size=(20, 1))]
            ]

        window = sg.Window("Delivery App", layout)

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)

        if event == "Back":
            window.close()
            return

        if event == "Order Arrived":
            rows = delivery_query_handeler.get_my_order(id)

            if len(rows) == 0:
                error = True
                window.close()
            else:
                delivery_query_handeler.my_order_arrived(id)
                error = False


def my_basket_history (id):
    not_arrived = False
    while True:
        basket = delivery_query_handeler.find_delivery_basket(id, True, not_arrived)
        l = basket_rows_to_list(basket)

        show_number = min(len(l), 12)


        layout = [
            [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
            [sg.Checkbox("Filter Not Arrived", size=(20, 1), key="-NOTARRIVED-", enable_events=True, default=not_arrived)],
            [sg.Button("Back", size = (20, 1))]
        ]

        window = sg.Window("Delivery App", layout)

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)

        if event == "Back":
            window.close()
            return

        if event == "-NOTARRIVED-":
            not_arrived = values["-NOTARRIVED-"]
            window.close()

def order_information_to_list (info):
    l = []

    for row in info:
        l.append("id: " + row[0] + "  restaurant id: " + row[1] + "  preparing time: " + row[2]
                + "  customer id: " + row[3] + "  order time: " + row[4] + "  total price: " + row[5])

    return l

def show_information (order_id):
    info = delivery_query_handeler.get_order_information(order_id)
    l = order_information_to_list(info)
    show_number = 1

    layout = [
        [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
        [sg.Button("Back", size=(20, 1))]
    ]

    if event == "Exit" or event == sg.WIN_CLOSED:
        exit(0)

    if event == "Back":
        window.close()
        return


def orders_information (id):
    not_arrived = False
    mine = False
    while True:
        basket = delivery_query_handeler.find_delivery_basket(id, mine, not_arrived)
        l = basket_rows_to_list(basket)

        show_number = min(len(l), 12)

        layout = [
            [sg.Listbox(values=l, size=(70, show_number), key='-LIST-', enable_events=True)],
            [sg.Checkbox("Filter Mine", size=(20, 1), key="-MINE-", enable_events=True, default=mine)],
            [sg.Checkbox("Filter Not Arrived", size=(20, 1), key="-NOTARRIVED-", enable_events=True, default=not_arrived)],
            [sg.Button("Back", size = (20, 1))]
        ]

        window = sg.Window("Delivery App", layout)

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)

        if event == "Back":
            window.close()
            return

        if event == "-MINE-":
            mine = values["-MINE-"]
            window.close()


        if event == "-NOTARRIVED-":
            not_arrived = values["-NOTARRIVED-"]
            window.close()

        if event == "-LIST-":
            if show_number > 0:
                order_id = values["-LIST-"][0].split()[0]
                window.close()
                show_information(order_id)
            window.close()




def home_page(id):
    while True:
        layout = [
            [sg.Button("My Current Order", size=(20, 1))],
            [sg.Button("My Basket History", size=(20, 1))],
            [sg.Button("Orders Information", size=(20, 1))],
            [sg.Button("Back", size=(20, 1))]
        ]

        window = sg.Window("Delivery App", layout)

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)

        if event == "Back":
            window.close()
            return

        if event == "My Current Order":
            window.close()
            my_current_order(id)

        if event == "My Basket History":
            window.close()
            my_basket_history(id)

        if event == "Orders Information":
            window.close()
            orders_information(id)



def sign_up():
    incomplete = False
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
                incomplete = False
                delivery_query_handeler.add_new_delivery(values[0], values[1], values[2])
                print("Delivery Added")
                window.close()
                return
            else:
                incomplete = True
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