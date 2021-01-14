import PySimpleGUI
# img_viewer.py

import PySimpleGUI as sg
import client_query_handler

layout = [[sg.Text('Enter username'), sg.InputText()],
          [sg.Text('Enter password'), sg.InputText()],
          [sg.Button('ok'), sg.Button('sing up')]]

window = sg.Window("client app", layout)
# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "ok":
        if client_query_handler.check_user_pass(values[0],values[1])==0:
            layout = [[sg.Text('Enter username'), sg.InputText()],
                      [sg.Text('Enter password'), sg.InputText()],
                      [sg.Button('ok'), sg.Button('sing up')]]

    elif event == "sing up":  # A file was chosen from the listbox
        try:

        except:
            pass

window.close()
