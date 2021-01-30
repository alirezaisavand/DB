import PySimpleGUI as sg
import delivery_query_handeler

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
            my_tOKen = delivery_query_handeler.check_name(values[0])
            if my_tOKen == -1:
                print("wrong Information")
                wrong_info = 1
            else:
                print("Hi")
            #    wrong_info = 0
            #    window.close()
            #    home_page(my_tOKen)
            window.close()
        elif event == "Sign Up":
            wrong_info = 0
            window.close()
            sign_up()

sg.theme('DarkTeal9')
initial_screen()