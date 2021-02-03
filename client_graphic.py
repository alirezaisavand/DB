# img_viewer.py
import threading
import time
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


def food_rows_to_list_in_order(rows):
    l = []
    for row in rows:
        l.append("name: " + row[0] + "-type: " + row[1] + "-price:" + str(row[2]) +
                 "-amount:" + str(row[3]) + "\n-your score:" + str(row[4]))
    return l


def basket_food_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("name: " + row[0] + "-amount: " + str(row[1]))
    return l


# cur.execute('''CREATE VIEW CusdiscountCode AS SELECT id,percentage,max,customer_id FROM discountCode ''')
def discount_rows_to_list(rows, total_price):
    l = []
    for row in rows:
        if total_price is None:
            l.append("code: " + row[0] + " - percentage:" + str(row[1]) + " -max: " + str(row[2]))
        else:
            l.append("code: " + row[0] + " - percentage:" + str(row[1]) + " -max: " + str(row[2]) + " -final price:"
                     + str(total_price - min(row[2], total_price * row[1])))
    return l


def order_rows_to_list(rows):
    l = []
    for row in rows:
        l.append("code: " + row[0] + "\nrestaurant: " + row[1] + "-time: " + str(row[2]) + "-price:" + str(row[3]))
    return l


def choose_restaurant_filter():
    by = []
    what = []
    types = client_query_handler.get_all_restaurant_specific_colum("type")
    areas = client_query_handler.get_all_restaurant_specific_colum("area")
    while True:
        layout = [
            [sg.Text('minimum score'), sg.InputText(), sg.Button("apply")],
            [sg.Text('choose restaurant area below')],
            [sg.Listbox(values=areas, size=(200, min(12, len(areas))), key='-area-', enable_events=True)],
            [sg.Text('choose restaurant type below')],
            [sg.Listbox(values=types, size=(200, min(12, len(types))), key='-type-', enable_events=True)],

            [sg.Button("apply filters"), sg.Button("<-back")]]

        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "<-back":
            return [[], []]

        elif event == "apply" and values[0] != "":
            by.append("score")
            what.append(values[0])

        elif event == "-type-" and len(types):
            by.append("type")
            what.append(values["-type-"][0][0])

        elif event == "-area-" and len(areas):
            by.append("area")
            what.append(values["-area-"][0][0])

        elif event == "apply filters":
            return [by, what]


def choose_food_filter():
    by = []
    what = []
    types = client_query_handler.get_all_food_specific_colum("type")
    while True:
        layout = [
            [sg.Text('minimum score'), sg.InputText(), sg.Button("apply1")],
            [sg.Text('minimum price'), sg.InputText(), sg.Button("apply2")],
            [sg.Text('maximum price'), sg.InputText(), sg.Button("apply3")],
            [sg.Text('choose food type below')],
            [sg.Listbox(values=types, size=(200, min(12, len(types))), key='-type-', enable_events=True)],

            [sg.Button("apply filters"), sg.Button("<-back")]]

        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "<-back":
            return [[], []]

        elif event == "apply1" and values[0] != "":
            by.append("score")
            what.append(values[0])

        elif event == "apply2" and values[1] != "":
            by.append("price")
            what.append(values[1])

        elif event == "apply3" and values[2] != "":
            by.append("price")
            what.append(-values[2])

        elif event == "-type-" and len(types):
            by.append("type")
            what.append(values["-type-"][0][0])


        elif event == "apply filters":
            return [by, what]


def choose_food(user_data, user_token, restaurant_name):
    restaurant_id = client_query_handler.searchـrestaurant(["name"], [restaurant_name])[0][0]
    by = ["restaurant_id"]
    what = [restaurant_id]

    while True:
        rows = client_query_handler.search_food(by, what)
        l = food_rows_to_list(rows)
        print(l)
        layout = [
            [sg.Button("more filter!")],
            [sg.Text('balance:' + str(user_data[4]))],
            [sg.Text(str(restaurant_name))],
            [sg.Listbox(values=l, size=(200, min(12, len(l))), key='-LIST-', enable_events=True)],
            [sg.Button("Done!"), sg.Button("home page"), sg.Button("<-back")]]

        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "<-back":
            return
        elif event == "home page":
            home_page(user_token)

        elif event == "more filter!":
            ss = choose_food_filter()
            by = ["restaurant_id"]
            what = [restaurant_id]
            by += ss[0]
            what += ss[1]

        elif event == "-LIST-" and len(l) != 0:
            food_name = values["-LIST-"][0].split()[1]
            # after enabling multisearch filter add restorant_id

            food_id = client_query_handler.search_food(by + ["name"], what + [food_name])[0][0]
            client_query_handler.order_food(user_token, restaurant_id, food_id)
        elif event == "Done!":
            home_page(user_token)


def my_basket(user_token, user_data):
    while True:
        rows = client_query_handler.get_customer_basket(user_token)
        l = basket_food_rows_to_list(rows)
        print(l)
        layout = [
            [sg.Text('balance:' + str(user_data[4]))],
            [sg.Text("order price:" + str(client_query_handler.get_basket_price(user_token)))],
            [sg.Listbox(values=l, size=(200, min(12, len(l))), key='-LIST-', enable_events=True)],
            [sg.Button("buy!"), sg.Button("home page"), sg.Button("use discount code"), sg.Button("<-back")]]

        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "<-back":
            return
        elif event == "use discount code":
            discount_code = my_discounts(user_token, client_query_handler.get_basket_price(user_token))
            order_id = client_query_handler.buy_basket_foods(user_token, discount_code)
        elif event == "home page":
            home_page(user_token)
        elif event == "buy!":
            order_id = client_query_handler.buy_basket_foods(user_token)


def choose_restaurant(user_data, user_token):
    by = ["area"]
    what = [user_data[2]]
    text = 'restaurant in your area'
    while True:
        rows = client_query_handler.searchـrestaurant(by, what)
        l = restaurant_rows_to_list(rows)
        print(l)
        layout = [
            [sg.Button("more filter!")],
            [sg.Text('balance:' + str(user_data[4]))],
            [sg.Text(text)],
            [sg.Listbox(values=l, size=(200, min(12, len(l))), key='-LIST-', enable_events=True)],
            [sg.Button("home page"), sg.Button("<-back")]]

        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "more filter!":
            ss = choose_restaurant_filter()
            by = ss[0]
            what = ss[1]
            text = "based on your filter"

        elif event == "<-back":
            return
        elif event == "home page":
            home_page(user_token)
        elif event == "-LIST-" and len(l) != 0:
            choose_food(user_data, user_token, values["-LIST-"][0].split()[2])


# cur.execute('''CREATE VIEW Cusorder AS SELECT id,restaurant_id,preparing_time,customer_id,order_time,discount_id, total_price FROM orderr ''')
# cur.execute('''CREATE VIEW Cussending AS SELECT order_id,delivery_id,score,arriving_time,cost FROM sending''')
def order_detail(order_id, user_token):
    while True:
        order_data = client_query_handler.get_order_data(order_id)[0]
        sending_data = client_query_handler.get_sending_data(order_id)[0]
        rows = client_query_handler.get_foods_of_order(order_id)

        l = food_rows_to_list_in_order(rows)
        layout = [[sg.Text("id:" + ("?" if order_data[0] is None else order_data[0]) +
                           "  preparing time:" + ("?" if order_data[2] is None else order_data[2]))],
                  [sg.Text("total price:" + ("?" if order_data[5] is None else order_data[5])
                           + "  ordering time:" + str("?" if order_data[4] is None else order_data[4]))],
                  [sg.Text("delivery id" + ("?" if sending_data[1] is None else sending_data[1]) +
                           "  arriving time:" + ("?" if sending_data[3] is None else sending_data[3]))],
                  [sg.Text("your score to delivery is :" + str(("?" if sending_data[2] is None else sending_data[2]))
                           + " chenge it here:")
                      , sg.InputText(), sg.Button("set")],
                  [sg.Listbox(values=l, size=(200, min(12, len(l))), key='-LIST-', enable_events=True)],
                  [sg.Text("your score to that food:"), sg.InputText()],
                  [sg.Button("home page"), sg.Button("<-back")]]

        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "<-back":
            return
        elif event == "home page":
            home_page(user_token)
        elif event == "set" and values[0] != "" and 5 >= int(values[0]) >= 0:
            client_query_handler.add_delivery_score(sending_data[0], int(values[0]))
        elif event == "-LIST-" and values[1] != "" and len(l) != 0 and 5 >= int(values[1]) >= 0:
            food_name = values["-LIST-"][0].split()[1]
            food_id = client_query_handler.find_food_id(order_id, food_name)
            client_query_handler.add_score(order_id, food_id, int(values[1]))


def my_orders(user_token):
    while True:
        rows = client_query_handler.get_customer_orders(user_token)
        l = order_rows_to_list(rows)
        print(l)
        layout = [
            [sg.Listbox(values=l, size=(200, min(12, len(l))), key='-LIST-', enable_events=True)],
            [sg.Button("home page"), sg.Button("<-back")]]
        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "<-back":
            return
        elif event == "home page":
            home_page(user_token)
        elif event == "-LIST-" and len(l) != 0:
            order_id = values["-LIST-"][0].split()[1]
            #  client_query_handler.b
            order_detail(order_id, user_token)


def my_discounts(user_token, total_price=None):
    while True:
        rows = client_query_handler.get_customer_discounts(user_token)
        l = discount_rows_to_list(rows, total_price)

        layout = [
            [sg.Listbox(values=l, size=(200, min(12, len(l))), key='-LIST-', enable_events=True)],
            [sg.Button("home page")]]

        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        if event == "-LIST-" and len(l) != 0:
            discount_id = values["-LIST-"][0].split()[1]
            return discount_id
        elif event == "home page":
            home_page(user_token)


def home_page(user_token):
    while True:
        print("welcome")
        user_data = client_query_handler.get_client_info(user_token)
        # SELECT id,name,area,phone_number,balance
        layout = [
            [sg.Text('balance:' + str(user_data[4]))],
            [sg.Text('charge account'), sg.InputText(), sg.Button("charge")],
            [sg.Button("order food"), sg.Button("buy basket"), sg.Button("my orders"), sg.Button("my discount"),
             sg.Button("<-back")]]
        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "my discount":
            my_discounts(user_token)
        elif event == "<-back":
            return
        elif event == "charge" and values[0] != "":
            client_query_handler.charge_account(user_token, int(values[0]))
            continue
        elif event == "order food":
            choose_restaurant(user_data, user_token)
        elif event == "my orders":
            my_orders(user_token)
        elif event == "buy basket":
            my_basket(user_token, user_data)


def sign_up():
    while True:
        layout = [
            [sg.Text('Enter username'), sg.InputText()],
            [sg.Text('Enter password'), sg.InputText()],
            [sg.Text('Enter name'), sg.InputText()],
            [sg.Text('Enter area'), sg.InputText()],
            [sg.Text('Enter phone_number'), sg.InputText()],
            [sg.Button('ok'), sg.Button("<-back")]]
        window = sg.Window("client app", layout)
        event, values = window.read()
        window.close()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        elif event == "<-back":
            window.close()
            return
        if values[0] != "" and values[1] != "" and values[2] != "" and values[3] != "" and values[4] != "":
            try:
                client_query_handler.add_customer(values[0], values[1], values[2], values[3], values[4])
                initial_screen()
            except:
                print("enter valid data")


def initial_screen():
    while True:
        layout = [[sg.Text('Enter username'), sg.InputText()],
                  [sg.Text('Enter password'), sg.InputText()],
                  [sg.Button('ok'), sg.Button('sign up'), sg.Button("<-back")]]

        window = sg.Window("client app", layout)
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit(0)
        if event == "ok" and values[0] != "" and values[1] != "":
            my_token = client_query_handler.check_user_pass(values[0], values[1])
            if my_token == -1:
                layout = [[sg.Text('wrong user pass')],
                          [sg.Text('Enter username'), sg.InputText()],
                          [sg.Text('Enter password'), sg.InputText()],
                          [sg.Button('ok'), sg.Button('sign up')]]
                window.close()
                window = sg.Window("client app", layout)
            else:
                window.close()
                home_page(my_token)
        elif event == "sign up":
            window.close()
            sign_up()
        elif event == "<-back":
            window.close()
            return


initial_screen()
