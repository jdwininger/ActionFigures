import mysql.connector
import subprocess
import random
import string
from guizero import App, Combo, Text, PushButton, info, TextBox

#// mysql database connection information. Yes that's a plain text password - yuck
mydb = mysql.connector.connect(
    host='your_host',
    password='your_password',
    user='your_username',
    database='your_database'
)

mycursor = mydb.cursor()

#// defining the select image routine when you press the select image button
def upload_image(title='Select image', folder='.', filetypes=[['PNG Image', '*.png'], ['JPEG Image', '*.jpeg']],
                 save=False, master=None):
    file_name.value = app.select_file()

#// defining what happens when you press the submit button. This is what actually enters the data into the mysql database.
def submit():
    sql: str = "INSERT INTO figures (figure_name, figure_line, figure_manufacturer, figure_notes, figure_photo_file) VALUES (%s, %s, %s, %s, %s)"
    val = (figure_name.value, figure_line.value, figure_manufacturer.value, figure_notes.value, file_name.value)
    mycursor.execute(sql, val)
    subprocess.run(['cp', '-av', file_name.value, '/var/www/html/images/'])
    info('success', 'your data has been submitted')
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

#// below is the layout for the app's window. eack row of input boxes and buttons are in their own block, it's fairly easy to tell what row each object is on
app: object = App(bg='gray', title='action figure database input', width='640', height='480', layout='grid')

figure_name_text: object = Text(app, text='Figure Name:        ', grid=[0, 0], align='left')
figure_name: object = TextBox(app, grid=[1, 0], width="24", align="left")

figure_line_text: object = Text(app, text='Product Line:', grid=[0, 1], align='left')
figure_line: object = Combo(app, options=['Marvel Legends', 'DC Multiverse', 'Other'], grid=[1, 1], width='20',
                            align='left')

figure_manfacturer_text: object = Text(app, text='Manufacturer:', grid=[0, 2], align='left')
figure_manufacturer: object = Combo(app, options=['Hasbro', 'McFarlane Toys', 'ToyBiz', 'Mattel'], grid=[1, 2],
                                    width='20', align='left')

figure_notes_text: object = Text(app, text='Additional Notes', grid=[0, 3], align='left')
figure_notes: object = TextBox(app, multiline='true', width='30', grid=[1, 3], height='5', align="left")

upload_image_text: object = Text(app, text='Upload Photos', grid=[0, 5], align='left')
upload_image_button = PushButton(app, command=upload_image, text='Select Image', grid=[1, 5], align='left')
file_name: object = Text(app, visible=0, grid=[2, 5])

empty_text: object = Text(app, text="", grid=[0, 9], align='left')
submit_button = PushButton(app, command=submit, text='Submit Entry', grid=[0, 10], align='left')

app.display()
