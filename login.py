from tkinter import *
import tkinter as tk
from restaurant import main
from tkinter import messagebox
import sqlite3
from ttkthemes import ThemedStyle
from tkinter.ttk import *
from platform import system
if system() == 'Linux':
    theme = 'scidgreen'
else:
    theme = 'radiance'

gender = ["select", "   Male", "   Female", "Others"]
# connection with the database

mydb = sqlite3.connect('login_db.db')
cursor = mydb.cursor()
cursor.execute("""create table if not exists signup(name varchar(20) unique
                  ,emaid varchar(50) , phone_no varchar(14), password varchar(10) ,
                  gender varchar(10) , adress varchar(256), admin integer default 0 )""")
a = 0
mydb.commit()
k = 0


def loginf():

    global u, v, login
    try:
        sign.destroy()
    except:
        pass
    login = Tk()
    logins = ThemedStyle(login)
    logins.set_theme(theme)
    u = StringVar()
    v = StringVar()
    login.resizable(0, 0)
    login.title(' Login')
    fr = Frame(login)
    fr.pack(side=TOP)
    labinfo = tk.Label(fr, text='Restaurant login page', font=(
        'calibri', 12, 'italic'), justify='center')
    labinfo.pack(padx=10, pady=10)
    lbframe = tk.LabelFrame(login, text='Login', font=(
        'calibri', 20, 'italic'), fg='green')
    lbframe.pack(padx=10, pady=10, ipadx=10, ipady=10)
    lb1 = Label(lbframe, text=' ID')
    lb2 = Label(lbframe, text='Password')
    user_ent = Entry(lbframe, textvariable=u, )
    pass_ent = Entry(lbframe, textvariable=v)
    lb1.grid(padx=10, pady=10, row=0, column=0)
    lb2.grid(padx=10, pady=10, row=1, column=0)
    user_ent.grid(padx=10, pady=10, row=0, column=1)
    pass_ent.config(show="•")
    pass_ent.grid(padx=10, pady=10, row=1, column=1)
    pass_ent.bind("<Return>", lambda x: login_())
    signupbt = Button(lbframe, text='signup', command=signup)
    signupbt.grid(padx=10, pady=10, row=2, column=0)
    loginbt = Button(lbframe, text='login', command=login_)
    loginbt.grid(padx=10, pady=10, row=2, column=1)
    login.mainloop()


def signup():
    global w, x, y1, y2, y3, y4, sign
    try:
        login.destroy()
    except:
        pass

    sign = Tk()
    signs = ThemedStyle(sign)
    signs.set_theme(theme)

    w = StringVar()
    x = StringVar()
    y1 = StringVar()
    y2 = StringVar()
    y3 = StringVar()
    y3.set('select')
    y4 = StringVar()
    sign.resizable(0, 0)
    sign.title('Signup')
    fr = Frame(sign)
    fr.pack(side=TOP)
    labinfo = Label(fr, text='Khao Piyo Restaurant')
    labinfo.pack()
    lbframe = tk.LabelFrame(sign, text='Sign up', font=(
        'calibri', 20, 'italic'), fg='green')
    lbframe.pack(padx=10, pady=10, ipadx=10, ipady=10)
    lb1 = Label(lbframe, text='user name')
    lb2 = Label(lbframe, text='user email')
    lb3 = Label(lbframe, text='user phone_no')
    lb4 = Label(lbframe, text='user password')
    lb5 = Label(lbframe, text=' gender ')
    lb6 = Label(lbframe, text='user adresss')
    user_ent = Entry(lbframe, textvariable=w)
    email_ent = Entry(lbframe, textvariable=x)
    phone_ent = Entry(lbframe, textvariable=y1)
    pass_ent = Entry(lbframe, textvariable=y2)
    pass_ent.config(show='●')
    gender_ent = OptionMenu(lbframe, y3, *gender)
    gender_ent.config(width=18)
    adress_ent = Entry(lbframe, textvariable=y4)
    lb1.grid(padx=10, pady=10, row=0, column=0)
    lb2.grid(padx=10, pady=10, row=1, column=0)
    lb3.grid(padx=10, pady=10, row=2, column=0)
    lb4.grid(padx=10, pady=10, row=3, column=0)
    lb5.grid(padx=10, pady=10, row=4, column=0)
    lb6.grid(padx=10, pady=10, row=5, column=0)
    user_ent.grid(padx=10, pady=10, row=0, column=1)
    email_ent.grid(padx=10, pady=10, row=1, column=1)
    phone_ent.grid(padx=10, pady=10, row=2, column=1)
    pass_ent.grid(padx=10, pady=10, row=3, column=1)
    gender_ent.grid(padx=10, pady=10, row=4, column=1)
    adress_ent.grid(padx=10, pady=10, row=5, column=1)
    adress_ent.bind("<Return>", lambda x: sign_())
    signupbt = Button(lbframe, text='signup', command=sign_)
    signupbt.grid(padx=10, pady=10, row=6, column=0)
    loginbt = Button(lbframe, text='login', command=loginf)

    loginbt.grid(padx=10, pady=10, row=6, column=1)

    sign.mainloop()


def login_():
    global a
    global k
    global user

    try:
        cursor.execute('select  name  , password from signup')
        b = cursor.fetchall()
        file = open('img//username', 'w')
        file.write(f'{u.get().strip()}')
        file.close()
    except:
        messagebox.showinfo('fail', 'can\'t read database')
    flag = 0

    for i, l in b:
        if i == u.get().strip() and l == v.get().strip():
            flag = 1
    if flag == 1:
        messagebox.showinfo(
            'succes', f'your are logged in as {u.get().strip()}')
        user = u.get().strip()
        login.destroy()

        a = 1
    elif flag == 0 and k < 2:
        k += 1
        messagebox.showwarning(
            'fail', 'try again User id/password is incorrect')

    elif flag == 0 and k == 2:

        messagebox.showerror('blocked ', 'Operation is terminated')

        login.destroy()

        import sys
        sys.exit()


def sign_():
    global w, x, y1, y2, y3, y4
    arr = [w, x, y1, y2, y3, y4]
    for i in arr:
        if i.get() == '' or i.get() == 'select' or i.get() == 'null':
            flag = False
            break
        else:
            flag = True
    if flag:
        cursor.execute(
            f'insert into signup values("{w.get().strip()}","{x.get().strip()}","{y1.get().strip()}","{y2.get().strip()}","{y3.get().strip()}","{y4.get().strip()}", 0) ')
        mydb.commit()
        sign.destroy()
        loginf()
    else:
        messagebox.showinfo('nope', 'all feilds are required')


def ch():
    cursor.execute('select * from signup')
    b = cursor.fetchall()

    if b == []:
        signup()

    else:
        loginf()


ch()
mydb.close()
if a == 1:
    main(user)
# developed using high cohesion and least coupling  and the coupling method used is control coupling i.e. data from one module is used to trigger data of 2nd module
