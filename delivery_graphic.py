import PySimpleGUI as sg

def initial_screen():
    wrong_info = 0
    while True:
        layout = [[sg.Text('Enter Username',size=(20, 1)), sg.InputText()],
                  [sg.Text('Enter Password',size=(20, 1)), sg.InputText()],
                  [sg.Button('OK', size=(10, 1)), sg.Button('Sign Up', size=(10, 1))]]

        if wrong_info:
            layout.append([sg.Text("Wrong Information", text_color='red')])

        window = sg.Window("Delivery App", layout)

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