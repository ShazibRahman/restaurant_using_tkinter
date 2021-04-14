from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *
from ttkthemes import ThemedStyle 
import payment as p 
from platform import system
import time
import sqlite3 

if system()=='Linux':
    theme='scidmint'
else:
    theme='radiance'

totaling=False 

payment_tot=False 
already_payement=False 

# functions for validating the various test cases invloves in the triggering of payement like the user have ordered somwthing 
# or the payment for the session has already done
def payement():
    '''this vey function validate the payement gate whether the user has done totaling before pressing the payement button
    ,whether the user has already paid for the session and if all the condition satisfied it will open the payement gate'''
    global payment_tot,already_payement , recursion ,tot
    if not payment_tot :
       a= messagebox.askyesno('payement','totaling has not been done for the session do you want to totaling first ?')
       if a:
           total()
           if tot!=0.0:
                payement() 
          
            

    elif  already_payement:
       if  messagebox.askyesno('payment','payment for this session has already been done. do you want to place a new order ?'):
       
           resetf()
           messagebox.showinfo('New Order','Now you can place new order')
 
    elif  not already_payement:
        already_payement=True 
        cursor.execute(f'insert into payments values({order_no},"{usernam}","{tot}")')
        mydb1.commit()
        p.pay()
       
#saving the user name for autologin#  

file2=open('img//username')
usernam=file2.read().strip()

#creating the connection and creating the table

mydb1=sqlite3.connect('login_db.db')
cursor=mydb1.cursor()
cursor.execute('pragma foreign_key=on')
cursor.execute('''
create table if not exists orders ( order_no integer primary key autoincrement,name varchar(20),  cost float , gst float , total float, delivered integer default 0 )
'''
)

#normalizing the database for proper functioning 

cursor.execute('create table if not exists dosa( order_no integer ,dosa_type varchar(256), nos integer, foreign key (order_no) references orders(order_no))')
cursor.execute('create table if not exists idli ( order_no integer ,idli_type varchar(256), nos integer, foreign key (order_no) references orders(order_no))')
cursor.execute('create table if not exists french ( order_no integer ,french_type varchar(256), nos integer, foreign key (order_no) references orders(order_no))')
cursor.execute('create table if not exists biryani ( order_no integer ,biryani_type varchar(256), nos integer, foreign key (order_no) references orders(order_no))')
cursor.execute('create table if not exists fried ( order_no integer ,fried_type varchar(256), nos integer, foreign key (order_no) references orders(order_no))')
cursor.execute('create table if not exists drink  ( order_no integer ,company_name varchar(256), capacity varchar(20), foreign key (order_no) references orders(order_no))')
cursor.execute('create table if not exists noodles ( order_no integer ,noodles_type varchar(256), nos integer, foreign key (order_no) references orders(order_no))')
cursor.execute('create table if not exists payments (order_no integer , name varchar(20),total varchar(20), foreign key (order_no) references orders(order_no))')
mydb1.commit()

choices=['Null','200 ml','1 ltr','2 ltr']


     
class spinbox(Entry):
    '''
    return the spinbox widget using entry widget
    '''
    def __init__(self, master=None, **kw):

        Entry.__init__(self, master, "ttk::spinbox", **kw)
       


#fucntion for updating the time displaying on the label#

def set_label():
    global choices
    localtime=time.asctime()
    info['text']=localtime
    root.after(1,set_label)

#dic consisting of choices  and their price for OptionMenu

drink_price={'Null':0,'200 ml':20,'1 ltr':56,'2 ltr':108}
biryani_price={'Null':0,'veg biryani':100,'chicken biryani':200,'mutton biryani':250}
noodles_price={'Null':0,'veg noodles':50,'egg noodles':80,'chicken noodles':100 }
french_price={'Null':0,'small bowl fries':40, 'medium bowl fries':70,'large bowl fries':100}
fried_price={'Null':0,'veg fried rice':70,'egg fried rice':90,'chicken fried rice':110}
dosa_price={'Null':0,'plane dosa':30,'masala dosa':50}
idli_price={'Null':0,'idli sambhar':40, 'idli chutney':50}
drink_choice=['Null','cocacola','mountain dew','sprite ']

#functions generating total cost ,ac charge  and GST according to the order

def total():
    '''
    functions calculating the sum total and responsible for saving all detail in database and if the user has not order anything raise an messagebox
    saying user to order something first and if has twice press the total button then it will ask to pay for the current session as the totaling 
    has already been done.
    '''
    global payment_tot , totaling ,order_no ,tot,empty
    
    drink_c=drink_price[drinkvar.get()]
    biryani_c=float(biryani.get())*(biryani_price[biryanipopvar.get()])
    dosa_c=float(dosa.get())*(dosa_price[dosapopvar.get()])
    fried_c=float(fried.get())*(fried_price[friedpopvar.get()])
    noodles_c=float(noodles.get())*(noodles_price[noodlespopvar.get()])
    idli_c=float(idli.get())*(idli_price[idlipopvar.get()])
    french_c=float(french.get())*(french_price[frenchpopvar.get()])
    cost_=round(drink_c+biryani_c+dosa_c+fried_c+noodles_c+idli_c+french_c,3)
    
    ac_=round(0.02*cost_,3)
    subtotal_=cost_+ac_
    tax=round(.10*cost_,3)
    tot=round(tax+subtotal_,3)
    if totaling and not already_payement:
       a= messagebox.askyesno('totaling', 'totaling has already been done for this session. proceed to pay ?')
       if a:
           payement()
    elif totaling and already_payement:
        a= messagebox.askyesno('payment','payment has already been done fot this session . Do you want to place a new order ?')
        if a :
            resetf()
    
    elif tot!=0.0 : # if total is not equal to zero then it will trigger the database and saves all the entries
        if cost_>=1000:
            messagebox.showinfo('huraah','you got 10% off as you ordered for more than 1000 RS')
            tot=round(.9*tot,2)
        ac.set(str(ac_))
        totaling=True 
        payment_tot=True
        subtotalvar.set(str(subtotal_))
        totalvar.set(str(tot))
        gst.set(str(tax))
        costvar.set(str(cost_))
        cursor.execute(f'insert into orders (name ,cost , gst , total) values ("{usernam}",{cost_},{tax}, {tot})')
        cursor.execute('select max(order_no) from orders')
        order_no =cursor.fetchone()[0]
        
        order_v.set(order_no)
        cursor.execute(f'insert into dosa values ({order_no},"{dosapopvar.get().strip()}",{dosa.get().strip()})')
        mydb1.commit()
        cursor.execute(f'insert into idli values ({order_no},"{idlipopvar.get()}",{idli.get()});')
        mydb1.commit()
        cursor.execute(f'insert into french values ({order_no},"{frenchpopvar.get()}",{french.get()});')
        mydb1.commit()
        cursor.execute(f'insert into biryani values ({order_no},"{biryanipopvar.get()}",{biryani.get()});')
        mydb1.commit()
        cursor.execute(f'insert into fried values ({order_no},"{friedpopvar.get()}",{fried.get()});')
        mydb1.commit()
        cursor.execute(f'insert into drink values ({order_no},"{drinkpopvar.get()}","{drinkvar.get()}");')
        mydb1.commit()
        cursor.execute(f'insert into noodles values ({order_no},"{noodlespopvar.get()}",{noodles.get()});')
        mydb1.commit()
        file=open('img//orders.txt','w')
        file.write(f'ORDER NO : {order_no} \n\n')
        #iterating through all stringvar  by creating the stringvarlist

        for i , j in [(dosapopvar,dosa), (idlipopvar,idli), (frenchpopvar,french) ,(biryanipopvar,biryani),(friedpopvar,fried), (drinkpopvar,drinkvar),(noodlespopvar, noodles)]:

            if i.get()=='Null' or j.get()=='0' :

                pass
            elif i is drinkpopvar :
              if i.get()!='NUll' and j.get()!='Null':
                file.write(f'{drinkvar.get()} {drinkpopvar.get().strip().upper()}\n\n')
            else:
                file.write(f'{j.get()} plate/es {i.get().strip().upper()}\n\n')
        if cost_>=1000:
            file.write('hurrah you got 10% off as you ordered above 1000 RS,,Thank you\n\n')
        
        file.write(f'total: {tot} with included tax: {round(tax+ac_,2)}')
        
        file.close()
    
    elif tot==0.0:
        messagebox.showwarning('please','please order something first before pressing the total button')
          
        empty=True
      
# function calling to open kithen management interface

def kitchen_management():
    root.destroy()

    import kitchen.kitchen_gui as k
    k.MainGUI()

# function generating the tree for the item name and item count

def bill():
    '''this function is responsible for inlisting the item name and item count of the item hat has been selected by the current user in Tree view 
       and if the user has not ordered anything it will just show a window telling the user that it has not ordered anything
    '''
    global noorder 
    bill_tk=tk.Toplevel()
    
    
    noorder=tk.PhotoImage(file='img//noorders.gif')
    noorder=noorder.subsample(2,2)
    bill_tk.title('BILL')
    bill_=tk.Frame(bill_tk)
    lableq=tk.Label(bill_,text="Orders",font=("calibri",20,'italic'),fg='green')
    lableq.pack(padx=3,pady=3,ipady=3,ipadx=3)
    
    bill_.pack( padx=3,pady=3,ipady=3,ipadx=3)

    
    flag=0

    
    columns1=['one','two']
    
    treeview=Treeview(bill_,column=columns1,show='headings')
    treeview.column("one",minwidth=0,width=150) 
    treeview.column("two",minwidth=0,width=100)
    treeview.heading("one",text='Item Name')
    treeview.heading("two",text='Item count')
   
    for i , j in [(dosapopvar,dosa), (idlipopvar,idli), (frenchpopvar,french) , (friedpopvar,fried),(biryanipopvar,biryani), (drinkpopvar,drinkvar),(noodlespopvar, noodles)]:
        if i is not drinkpopvar and i.get()!="Null" and j.get()!='0':
                flag=1
                treeview.insert("","end",values=[i.get(),f'{j.get():>6}'])
        elif i is drinkpopvar and  i.get()!='Null' and j.get()!="Null":
                flag=1
                treeview.insert("","end",values=[j.get()+" "+i.get(),f'{" "*10}{"1"}'])
        
                
     
    if flag==0:
        
        lb=tk.Label(bill_, text='  YOU ORDERED NOTHING:',font=('calibri',20,'bold'),fg='red')
        noord=tk.Label(bill_,image=noorder)
        
        noord.pack()
        lb.pack(pady=10,ipady=10,padx=10)       
    else:
        treeview.pack()

#function to reset all the entry and optionMenu if and only if users want to reset it orders before doing totalling   
  
def resetf():
    global payment_tot , already_payement ,totaling 

    payment_tot=already_payement=totaling=False 
    drinkvar.set('Null')
    biryani.set('0')
    dosa.set('0')
    french.set('0')
    fried.set('0')
    idli.set('0')
    costvar.set('0')
    gst.set('0')
    ac.set('0')
    subtotalvar.set('0')
    totalvar.set('0')
    noodles.set('0')
    dosapopvar.set('Null')
    idlipopvar.set('Null')
    drinkpopvar.set('Null')
    biryanipopvar.set('Null')
    friedpopvar.set('Null')
    frenchpopvar.set('Null')
    noodlespopvar.set('Null')
    order_v.set('')

#           list of the yummy cousine served by our hotel 

def price():
    '''it is simply a GUI displaying the MENU of our restaurant'''
    pricetk=Toplevel()
  
    
    pricetk.resizable(0,0)
    pricetk.title('MENU')
    

    proce=tk.LabelFrame(pricetk,text='Menu', font=('calibri',20,'italic'),fg='green')
    proce.pack(padx=15 , pady=15, ipadx=15, ipady=15)

    lb00=tk.Label(proce, font=('aria' , 10 , 'bold'),text='Dosa ', fg='black', bd=10)
    lb00.grid(pady=10,row=0,column=0)
    lb01=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Masala Dosa RS. 50 ',fg='black' )
    lb01.grid(pady=10,row=0,column=1)
    lb01=tk.Label(proce, font=('aria' , 10 , 'italic'),text='plane Dosa RS. 30 ', fg='black', bd=10)
    lb01.grid(pady=10,row=1,column=1)
    

    lb10=tk.Label(proce, font=('aria' , 10 , 'bold'),text='French Fries ', fg='black', bd=10)
    lb10.grid(pady=10,row=2,column=0)
    lb11=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Small bowl 40 RS ', fg='black', bd=10)
    lb11.grid(pady=10,row=2,column=1)
    lb11=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Medium  bowl 70 RS ', fg='black', bd=10)
    lb11.grid(pady=10,row=3,column=1)
    lb11=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Large  bowl 100 RS ', fg='black', bd=10)
    lb11.grid(pady=10,row=4,column=1)

    lb20=tk.Label(proce, font=('aria' , 10 , 'bold'),text='Idli ', fg='black', bd=10)
    lb20.grid(pady=10,row=5,column=0)
    lb21=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Idli Sambhar 40 RS ', fg='black', bd=10)
    lb21.grid(pady=10,row=5,column=1)
    lb21=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Idli Chutney 50 RS ', fg='black', bd=10)
    lb21.grid(pady=10,row=6,column=1)
    
    lb30=tk.Label(proce, font=('aria' , 10 , 'bold'),text='Biryani ', fg='black', bd=10)
    lb30.grid(pady=10,row=7,column=0)
    lb31=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Veg. Biryani 100 RS ', fg='black', bd=10)
    lb31.grid(pady=10,row=7,column=1)
    lb31=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Chicken Biryani 200 RS ', fg='black', bd=10)
    lb31.grid(pady=10,row=8,column=1)
    lb31=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Mutton Biryani 250 RS ', fg='black', bd=10)
    lb31.grid(pady=10,row=9,column=1)

    lb40=tk.Label(proce, font=('aria' , 10 , 'bold'),text='Fried Rice ', fg='black', bd=10)
    lb40.grid(pady=10,row=0,column=2)
    lb41=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Veg Fried Rice 70 ', fg='black', bd=10)
    lb41.grid(pady=10,row=0,column=3)
    lb41=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Egg Fried Rice  RS 90', fg='black', bd=10)
    lb41.grid(pady=10,row=1,column=3)
    lb41=tk.Label(proce, font=('aria' , 10 , 'italic'),text='chicken Fried Rice RS 110 ', fg='black', bd=10)
    lb41.grid(pady=10,row=2,column=3)

    lb50=tk.Label(proce, font=('aria' , 10 , 'bold'),text='DRINKS ', fg='black', bd=10)
    lb50.grid(pady=10,row=3,column=2)
    lb51=tk.Label(proce, font=('aria' , 10 , 'italic'),text='200 ml : 20 RS  ', fg='black', bd=10)
    lb51.grid(pady=10,row=3,column=3)
    lb61=tk.Label(proce, font=('aria' , 10 , 'italic'),text='1 Ltr : 56 RS  ', fg='black', bd=10)
    lb61.grid(pady=10,row=4,column=3)
    lb71=tk.Label(proce, font=('aria' , 10 , 'italic'),text='2 Ltr : 106 RS  ', fg='black', bd=10)
    lb71.grid(pady=10,row=5,column=3)

    lb40=tk.Label(proce, font=('aria' , 10 , 'bold'),text='Noodles ', fg='black', bd=10)
    lb40.grid(pady=10,row=6,column=2)
    lb41=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Veg Noodles 50 RS ', fg='black', bd=10)
    lb41.grid(pady=10,row=6,column=3)
    lb41=tk.Label(proce, font=('aria' , 10 , 'italic'),text='Egg Noodles 80 RS ', fg='black', bd=10)
    lb41.grid(pady=10,row=7,column=3)
    lb41=tk.Label(proce, font=('aria' , 10 , 'italic'),text='chicken Noodles 100 RS ', fg='black', bd=10)
    lb41.grid(pady=10,row=8,column=3)

    proce.mainloop()

# Function checks if an admin has logged in. If yes, then it displayd Kitchen Mgmt button else displays orders button. 
# change this back if nessccary. Call kitchen_management() to open window from else where.
def admin(f1, infoimg, user):
    conn = sqlite3.connect("login_db.db")
    query = f"SELECT admin FROM signup WHERE name='{user}';"
    var = conn.execute(query)
    admin = tuple(var)[0][0]

    if admin==1:
        orders=Button(f1,width=14, text="KITCHEN MGMT.",command=kitchen_management ,image=infoimg,compound=LEFT  )  
        orders.grid(pady=12,row=9, column=4 ,padx=10 , ipady=5, ipadx=5)
        set_label()
        resetf()
    else:
        orders=Button(f1,width=14, text="ORDERS",command=bill ,image=infoimg,compound=LEFT  )  
        orders.grid(pady=12,row=9, column=4 ,padx=10 , ipady=5, ipadx=5)
        set_label()
        resetf()

#main GUI desinging starts from here
def main(user):
    '''the main function handles the gui part designed by shazib rahman
    and it contains all the frames , labels , buttons , optionmenu widgets ,  images '''
    global info , root
    root = Tk()
    roots=ThemedStyle(root)
    roots.set_theme(theme)
    messagebox.showinfo('Restaurant Management System','This project is designed and coded by Md Shazib Rahman ' ) 
    logo=PhotoImage(file='img//1.gif')#image on the top frame
    logo=logo.subsample(20,20) 
    
    root.title("Restaurant Management System")
    root.resizable(0,0)

    #Frames#
    
    Tops =Frame(root)
    Tops.pack(side=TOP,padx=10,pady=15)

    f1 = tk.Frame(root,height=700) 
    f1.pack(padx=20)
    #------------------TIME--------------

    localtime=time.asctime()
    #-----------------INFO TOP------------
    info = tk.Label(Tops, font=( 'aria' ,28, 'bold' ),text="    KHAO PIYO RESTAURANT          ",fg="green", pady=10)
    log=tk.Label(Tops,image=logo)
    log.grid(row=0, column=0,ipady=0,ipadx=0,padx=0,pady=0)
    info.grid(row=0,column=1)
    info = tk.Label(Tops, font=( 'aria' ,15,'italic' ),text=localtime,fg="steel blue", bd=10)
    info.grid(row=1,column=0,columnspan=2)

    #images on buttons
    totalimg=PhotoImage(file='img//total.gif').subsample(17,21)
    payimg=PhotoImage(file='img//pay.gif').subsample(15,15)
    infoimg=PhotoImage(file='img//orders.gif').subsample(5,7)
    resetimg=PhotoImage(file='img//reset.gif').subsample(12,12)
    menuimg=PhotoImage(file='img//menu.gif').subsample(8,10)
    
    #string variables used in entries and optionmenus
    global totalvar , subtotalvar , order_v , dosa, idli , biryani, fried, french, drinkvar , costvar , ac,gst , noodles, drinkpopvar,idlipopvar, noodlespopvar, biryanipopvar,dosapopvar,friedpopvar,friedpopvar, frenchpopvar
    totalvar=StringVar()
    subtotalvar=StringVar()
    order_v=StringVar()
    dosa=StringVar()
    idli=StringVar()
    biryani=StringVar()
    fried=StringVar()
    french=StringVar()
    drinkvar=StringVar()
    costvar=StringVar()
    ac=StringVar()
    gst=StringVar()
    noodles=StringVar()
    drinkpopvar=StringVar()
    idlipopvar=StringVar()
    noodlespopvar=StringVar()
    biryanipopvar=StringVar()
    dosapopvar=StringVar()
    friedpopvar=StringVar()
    frenchpopvar=StringVar()

   #labels entries and optionmenu

    order_no_label = tk.Label(f1, text="Order No." ,font=('aria' , 10 , 'bold'))
    
    order_no_label.grid(pady=10,row=0,column=0 )
    order_entry = Entry(f1, textvariable=order_v  )
    order_entry.grid(pady=10,row=0,column=1,columnspan=2)

    Dosa_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="Dosa ")
    Dosa_label.grid(pady=10,row=1,column=0)
    fries_pop=OptionMenu(f1,dosapopvar,*list(dosa_price.keys()))
    fries_pop.config(width=14)
    
    fries_pop.grid(pady=10,row=1,column=1)
    Dosaent =spinbox(f1, textvariable=dosa ,width=9,from_=0, to=10)
    Dosaent.grid(pady=10,row=1,column=2)

    idli_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="Idli")
    idli_label.grid(pady=10,row=2,column=0)
    idli_pop=OptionMenu(f1,idlipopvar,*list(idli_price.keys()))
    idli_pop.config(width=14)
    idli_pop.grid(pady=10,row=2,column=1)

    idlient = spinbox(f1, textvariable=idli  ,width=9, from_=0,to=10)
    idlient.grid(pady=10,row=2,column=2)


    burger_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="French Fries")
    burger_label.grid(pady=10,row=3,column=0)
    french_pop=OptionMenu(f1,frenchpopvar,*list(french_price.keys()))
    french_pop.config(width=14)
    french_pop.grid(pady=10,row=3,column=1)


    burger = spinbox(f1, textvariable=french  , width=9, from_=0,to=10)
    burger.grid(pady=10,row=3,column=2)
    
    Filet_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="Biryani")
    Filet_label.grid(pady=10,row=4,column=0)
    biryani_pop=OptionMenu(f1,biryanipopvar,*list(biryani_price.keys()))
    biryani_pop.config(width=14)
    biryani_pop.grid(pady=10,row=4, column=1)
    Filet = spinbox(f1, textvariable=biryani  ,width=9, from_=0,to=10)
    Filet.grid(pady=10,row=4,column=2)

    Cheese_burger_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="Fried Rice")
    Cheese_burger_label.grid(pady=10,row=5,column=0)
    fried_pop=OptionMenu(f1,friedpopvar,*list(fried_price.keys()))
    fried_pop.config(width=14)
    fried_pop.grid(pady=10,row=5,column=1)

    Cheese_burger = spinbox(f1, textvariable=fried  ,width=9, from_=0,to=10)
    Cheese_burger.grid(pady=10,row=5,column=2)
    drink = tk.Label(f1, font=('aria' , 10 , 'bold'), text="drink")
    drink.grid(pady=10,row=6,column=0)
    drink_pop=OptionMenu(f1,drinkpopvar,*drink_choice)
    drink_pop.config(width=14)
    drink_pop.grid(pady=10,row=6 , column=1)

    popupMenu = OptionMenu(f1, drinkvar, *choices)
    popupMenu.config(width=8)
    popupMenu.grid(pady=10,row=6, column=2)

    #-------------------2ND Part---------------------------

    Noodles_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="Noodles")
    Noodles_label.grid(pady=10,row=0,column=3)
    noodles_pop=OptionMenu(f1,noodlespopvar,*list(noodles_price.keys()))
    noodles_pop.config(width=14)
    noodles_pop.grid(pady=10,row=0,column=4)

    Noodles= spinbox(f1, textvariable=noodles  ,width=9, from_=0,to=10)
    Noodles.grid(pady=10,row=0,column=5)

    cost_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="cost")
    cost_label.grid(pady=10,row=1,column=3)
    cost = Entry(f1, textvariable=costvar  )
    cost.grid(pady=10,row=1,column=4, columnspan=2)

    Service_Charge_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="AC Charge")
    Service_Charge_label.grid(pady=10,row=2,column=3)
    Service_Charge = Entry(f1, textvariable=ac )
    Service_Charge.grid(pady=10,row=2,column=4,columnspan=2)
    
    Tax_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="GST")
    Tax_label.grid(pady=10,row=3,column=3)
    Tax = Entry(f1 ,textvariable=gst )
    Tax.grid(pady=10,row=3,column=4,columnspan=2)

    Subtotal_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="Subtotal")
    Subtotal_label.grid(pady=10,row=4,column=3)
    Subtotal = Entry(f1 ,textvariable=subtotalvar )
    Subtotal.grid(pady=10,row=4,column=4, columnspan=2)

    Total_label = tk.Label(f1, font=('aria' , 10 , 'bold'), text="Total")
    Total_label.grid(pady=10,row=5,column=3)
    Total_ent = Entry(f1 ,textvariable=totalvar )
    Total_ent.grid(pady=10,row=5,column=4,columnspan=2)


   #---buttons-----
    
    Price_b=Button(f1,width=14, text="MENU", command=price,image=menuimg,compound=LEFT)
    Price_b.grid(pady=20,row=9 ,column=0,padx=10 , ipady=5, ipadx=5)

    Total=Button(f1,width=14, text="TOTAL",image=totalimg,command=total, compound=LEFT)
    Total.grid(pady=10,row=9, column=1,padx=5, ipady=5)

    paybt=Button(f1,width=14, text="PAY",command=payement, image=payimg,compound=LEFT)
    paybt.grid(pady=20,row=9, column=2,padx=10 , ipady=5, ipadx=5)

    reset=Button(f1,width=14, text="RESET",command=resetf ,image=resetimg,compound=LEFT)
    reset.grid(pady=20,row=9, column=3,padx=10 , ipady=5, ipadx=5)
        
    admin(f1, infoimg, user) 
    root.mainloop()
if __name__=="__main__":
    main(usernam)