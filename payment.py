from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from ttkthemes import ThemedStyle
import tkinter as tk
import smtplib
import sqlite3 
from platform import system
from tkcalendar import DateEntry
if system()=='Linux':
    theme='scidgreen'
else:
    theme='radiance'

#from login import w

mydb1=sqlite3.connect('login_db.db')
cursor=mydb1.cursor()
def finalpay():
     '''this mailing  funtions is done by shazib rahman using smtplib package
     this funcitons mail the user about what they ordered and the sum total including taxes
     '''

     file1=open('img//username')
     q=file1.read()
     file1.close()
     
    
     cursor.execute(f'select emaid , adress from signup where name ="{q}"')
     a=cursor.fetchone()
     print(a)
     msg=f'subject: orders dispatched \n\nuser {q.upper()}\nyour orders have been dispatched to your location:\n{a[1].upper()}\n\n'
     file=open('img//orders.txt')
     messagebox.showinfo('succes','your transaction is succesful please wait for server response you will be redirected in a few seconds')
     for i in file.read():
         msg+=i
     file.close()
     b=False 
     try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        server.starttls()
        server.login(gmail_id, pasword)
        server.sendmail('gmail',a[0], msg)
        server.close()

        b=True 
     except:
        messagebox.showinfo('INTERNET ISSUE',f'{msg}')
    

     global onlinepay , debt , payroot
     try:
        debt.destroy()       
     except:
        try:
             onlinepay.destroy()            
        except:
            pass
     if b:
         messagebox.showinfo('mail','your order detail has been sent to your email ')
     payroot.destroy()
    

def cashpay():
    messagebox.showinfo('success','Please hand over money to the cashier and check your email')

    try:
        onlinepay.destroy()
        debt.destroy()
        payroot.destroy()
    except:
        pass
def debtpayment():
    '''manages the gui part for debit card payement'''
    try:
        onlinepay.destroy()
    except:
        pass
    global debt
    debt=Toplevel()
    debt.title('Debit paygate')
    debts=ThemedStyle(debt)
    debts.set_theme(theme)
    
    debtlabelframe=tk.LabelFrame(debt,text="DEBIT PAYEMENT METHOD", font=('calibri',10,'italic'))
    debtlabelframe.pack( padx=15, pady=15)
    cardno=Label(debtlabelframe,text='Card Number:' , )
    cardno.grid(row=0, column=0 , padx=10 , pady=10)
    cardnoent=Entry(debtlabelframe)
    cardnoent.grid(row=0, column=1, padx=10 , pady=10)
    expdate=Label(debtlabelframe,text='Expiry Date:' , )
    expdate.grid(row=1, column=0, padx=10 , pady=10)
    expdateent=DateEntry(debtlabelframe,width=18)
    expdateent.grid(row=1, column=1, padx=10 , pady=10)
    cardno=Label(debtlabelframe,text='CVV :' , )
    cardno.grid(row=2, column=0, padx=10 , pady=10)
    cardnoent1=Entry(debtlabelframe)
    cardnoent1.config(show='•')
    cardnoent1.grid(row=2, column=1 , padx=10 , pady=10)
    cardno=Label(debtlabelframe,text='Cardholder Name :' , )
    cardno.grid(row=3, column=0, padx=10 , pady=10)
    cardnoent=Entry(debtlabelframe)
    cardnoent.bind("<Return>",lambda x : finalpay())
    cardnoent.grid(row=3, column=1 , padx=10 , pady=10)
    paybt=Button(debtlabelframe,width=10 , text="PAY",command=finalpay)
    paybt.grid(row=4 , column=0  , padx=10 , pady=10)
    cancel=Button(debtlabelframe ,width=10, text="CANCEL", command=debt.destroy)
    cancel.grid(row=4, column=1,  padx=10 , pady=10)
    debt.mainloop()

def onlinepayment():
    '''manages the gateway for online banking '''
    try:
        debt.destroy()
    except:
        pass
    global onlinepay
    onlinepay=Toplevel()
    onlines=ThemedStyle(onlinepay)
    onlines.set_theme('scidgreen')
    onllabelframe=tk.LabelFrame(onlinepay,text="NET BANKING",font=('calibri',20,'italic'),fg='blue')
    onllabelframe.pack(padx=20, pady=20 , ipady=10 , ipadx=10)
    userno=Label(onllabelframe,text='User Id:' , )
    userno.grid(row=0, column=0 , padx=10 , pady=10)
    usernoent=Entry(onllabelframe)
    usernoent.grid(row=0, column=1 , padx=10 , pady=10)
    userpass=Label(onllabelframe,text='User Password:' , )
    
    userpass.grid(row=1, column=0, padx=10 , pady=10)
    userpassent=Entry(onllabelframe)
    userpassent.config(show='•')
    userpassent.bind("<Return>",lambda x :finalpay() )
    userpassent.grid(row=1, column=1,padx=10 , pady=10)
    paybt=Button(onllabelframe ,width=10, text="PAY",command=finalpay)
    paybt.grid(row=3 , column=0, padx=10 , pady=10)
    cancel=Button(onllabelframe ,width=10, text="CANCEL", command=onlinepay.destroy)
    cancel.grid(row=3, column=1,padx=10 , pady=10)
    onlinepay.mainloop()
 
def pay_check():
    
    a=pay_var.get()
    if a==0:
        debtpayment()
    elif a==1:
       onlinepayment()
    elif a==2:
        cashpay()
        
def pay():
    '''this functions manages the payroot gui where the payment gates are there
    '''
    global payroot , debpic , onlinepic , cashpic
    payroot=Toplevel()
    paroot=ThemedStyle(payroot)
    paroot.set_theme(theme)
    
    global pay_var
    pay_var=IntVar()

    debpic=PhotoImage(file='img//visa.gif')
    onlinepic=PhotoImage(file='img//sbi.gif')
    cashpic=PhotoImage(file='img//rs.gif')

    payroot.title('Payment Methods')
    paylabelframe=tk.LabelFrame(payroot,text='Payment',font=('calibri',20,'italic'), fg='green')
    paylabelframe.pack(padx=20, pady=20 ,ipadx=10, ipady=10)
    debit=Radiobutton(paylabelframe,variable=pay_var, text='DEBIT/CREDIT CARD', value=0)
    debit.grid(row=0,column=0)
    deblabel=Label(paylabelframe,image=debpic)
    deblabel.grid(row=0, column=1, padx=10)
    sbionline=Radiobutton(paylabelframe,variable=pay_var, text='NET BANKING          ', value=1)
    sbionline.grid(row=1,column=0)
    sbilabel=Label(paylabelframe,image=onlinepic)
    sbilabel.grid(row=1, column=1,ipady=10, padx=10)
    cash=Radiobutton(paylabelframe,variable=pay_var, text='CASH                       ', value=2)
    cash.grid(row=2,column=0, padx=10)
    cashlabel=Label(paylabelframe,image=cashpic)
    cashlabel.grid(row=2, column=1,ipady=10,pady=10)
    proceed=Button(paylabelframe ,width=10, text="PROCEED",command=pay_check)
    proceed.grid(row=3 , column=0,padx=10 ,ipady=3, ipadx=3)
    cancel=Button(paylabelframe  ,width=10, text="CANCEL",  command=payroot.destroy)
    cancel.grid(row=3, column=1,padx=10 , ipady=3,ipadx=3)

    payroot.mainloop()


if __name__=="__main__":
    pay()
