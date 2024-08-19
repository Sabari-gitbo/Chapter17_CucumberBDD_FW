from tkinter import *
import random
import os
import sys
from tkinter import messagebox
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def create_customer_database():

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('customer_database.db')
    c = conn.cursor()

    # Create a table
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

create_customer_database()

def add_customer(first_name, last_name, email, phone=None, address=None):
    conn = sqlite3.connect('customer_database.db')
    c = conn.cursor()

    try:
        c.execute('''
            INSERT INTO customers (first_name, last_name, email, phone, address)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, phone, address))

        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Customer with this email already exists.")
    finally:
        conn.close()

# Example usage
#add_customer('John', 'Doe', 'john.doe@example.com', '555-1234', '123 Elm Street')
#add_customer('Jane', 'Smith', 'jane.smith@example.com', '555-5678', '456 Oak Avenue')

def get_customers():
    conn = sqlite3.connect('customer_database.db')
    c = conn.cursor()

    c.execute('SELECT * FROM customers')
    customers = c.fetchall()

    conn.close()
    return customers

# Example usage
for customer in get_customers():
    print(customer)

def update_customer(customer_id, first_name=None, last_name=None, email=None, phone=None, address=None):
    conn = sqlite3.connect('customer_database.db')
    c = conn.cursor()

    if first_name:
        c.execute('UPDATE customers SET first_name = ? WHERE id = ?', (first_name, customer_id))
    if last_name:
        c.execute('UPDATE customers SET last_name = ? WHERE id = ?', (last_name, customer_id))
    if email:
        c.execute('UPDATE customers SET email = ? WHERE id = ?', (email, customer_id))
    if phone:
        c.execute('UPDATE customers SET phone = ? WHERE id = ?', (phone, customer_id))
    if address:
        c.execute('UPDATE customers SET address = ? WHERE id = ?', (address, customer_id))

    conn.commit()
    conn.close()

# Example usage
update_customer(1, phone='555-9999')

def delete_customer(customer_id):
    conn = sqlite3.connect('customer_database.db')
    c = conn.cursor()

    c.execute('DELETE FROM customers WHERE id = ?', (customer_id,))

    conn.commit()
    conn.close()

# Example usage
delete_customer(1)

# GUI functions
def refresh_customer_list():
    for row in tree.get_children():
        tree.delete(row)
    for customer in get_customers():
        tree.insert('', 'end', values=customer)

def add_customer_gui():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    address = entry_address.get()
    if not first_name or not last_name or not email:
        messagebox.showerror("Error", "First name, last name, and email are required.")
    else:
        add_customer(first_name, last_name, email, phone, address)
        refresh_customer_list()

def update_customer_gui():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a customer to update.")
        return
    customer_id = tree.item(selected_item[0], 'values')[0]
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    address = entry_address.get()
    if not first_name or not last_name or not email:
        messagebox.showerror("Error", "First name, last name, and email are required.")
    else:
        update_customer(customer_id, first_name, last_name, email, phone, address)
        refresh_customer_list()

def delete_customer_gui():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a customer to delete.")
        return
    customer_id = tree.item(selected_item[0], 'values')[0]
    delete_customer(customer_id)
    refresh_customer_list()

# Set up Tkinter window
from tkinter import *
customer= Tk()
customer.title("Customer Database")

# Create and place widgets
frame = tk.Frame()
frame.pack(padx=10, pady=10)

tk.Label(frame, text="First Name").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame, text="Last Name").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame, text="Email").grid(row=2, column=0, padx=5, pady=5)
tk.Label(frame, text="Phone").grid(row=3, column=0, padx=5, pady=5)
tk.Label(frame, text="Address").grid(row=4, column=0, padx=5, pady=5)

entry_first_name = tk.Entry(frame)
entry_last_name = tk.Entry(frame)
entry_email = tk.Entry(frame)
entry_phone = tk.Entry(frame)
entry_address = tk.Entry(frame)

entry_first_name.grid(row=0, column=1, padx=5, pady=5)
entry_last_name.grid(row=1, column=1, padx=5, pady=5)
entry_email.grid(row=2, column=1, padx=5, pady=5)
entry_phone.grid(row=3, column=1, padx=5, pady=5)
entry_address.grid(row=4, column=1, padx=5, pady=5)

tk.Button(frame, text="Add Customer", command=add_customer_gui).grid(row=5, column=0, padx=5, pady=5, columnspan=2)
tk.Button(frame, text="Update Customer", command=update_customer_gui).grid(row=6, column=0, padx=5, pady=5, columnspan=2)
tk.Button(frame, text="Delete Customer", command=delete_customer_gui).grid(row=7, column=0, padx=5, pady=5, columnspan=2)

# Create a Treeview widget to display customers
tree = ttk.Treeview(columns=("ID", "First Name", "Last Name", "Email", "Phone", "Address"), show='headings')
tree.heading("ID", text="ID")
tree.heading("First Name", text="First Name")
tree.heading("Last Name", text="Last Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")
tree.heading("Address", text="Address")
tree.pack(padx=10, pady=10, fill='both', expand=True)

# Refresh the customer list on startup
refresh_customer_list()


class Bill_App:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.configure(bg="#0A7CFF")
        self.root.title("Grocery Billing System - by Harini Software")
        title=Label(self.root,text="Grocery Billing System",bd=12,relief=RIDGE,font=("Arial Black",20),bg="#A569BD",fg="white").pack(fill=X)
        #===================================variables=======================================================================================
        self.Apple=IntVar()
        self.Orange=IntVar()
        self.Mango=IntVar()
        self.Grapes=IntVar()
        self.Banana=IntVar()
        self.Papaya=IntVar()
        self.Pomegranate=IntVar()
        self.Rice=IntVar()
        self.Wheat=IntVar()
        self.Ragi=IntVar()
        self.oil=IntVar()
        self.sugar=IntVar()
        self.dal=IntVar()
        self.tea=IntVar()
        self.soap=IntVar()
        self.shampoo=IntVar()
        self.lotion=IntVar()
        self.cream=IntVar()
        self.foam=IntVar()
        self.mask=IntVar()
        self.sanitizer=IntVar()
        self.total_sna=StringVar()
        self.total_gro=StringVar()
        self.total_hyg=StringVar()
        self.a=StringVar()
        self.b=StringVar()
        self.c=StringVar()
        self.c_name=StringVar()
        self.bill_no=StringVar()
        x=random.randint(1000,9999)
        self.bill_no.set(str(x))
        self.phone=StringVar()
        #==========================================customer details label frame=================================================
        details=LabelFrame(self.root,text="Customer Details",font=("Arial Black",12),bg="#A569BD",fg="white",relief=GROOVE,bd=10)
        details.place(x=0,y=80,relwidth=1)
        cust_name=Label(details,text="Customer Name",font=("Arial Black",14),bg="#A569BD",fg="white").grid(row=0,column=0,padx=15)

        cust_entry=Entry(details,borderwidth=4,width=30,textvariable=self.c_name).grid(row=0,column=1,padx=8)

        contact_name=Label(details,text="Contact No.",font=("Arial Black",14),bg="#A569BD",fg="white").grid(row=0,column=2,padx=10)

        contact_entry=Entry(details,borderwidth=4,width=30,textvariable=self.phone).grid(row=0,column=3,padx=8)

        bill_name=Label(details,text="Bill.No.",font=("Arial Black",14),bg="#A569BD",fg="white").grid(row=0,column=4,padx=10)

        bill_entry=Entry(details,borderwidth=4,width=30,textvariable=self.bill_no).grid(row=0,column=5,padx=8)
        #=======================================Fruits  Menu=================================================================
        fruits=LabelFrame(self.root,text="Fruits",font=("Arial Black",12),bg="#E5B4F3",fg="#6C3483",relief=GROOVE,bd=10)
        fruits.place(x=5,y=180,height=380,width=325)

        item1=Label(fruits,text="Apple",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=0,column=0,pady=11)
        item1_entry=Entry(fruits,borderwidth=2,width=15,textvariable=self.Apple).grid(row=0,column=1,padx=10)

        item2=Label(fruits,text="Orange",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=1,column=0,pady=11)
        item2_entry=Entry(fruits,borderwidth=2,width=15,textvariable=self.Orange).grid(row=1,column=1,padx=10)

        item3=Label(fruits,text="Mango",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=2,column=0,pady=11)
        item3_entry=Entry(fruits,borderwidth=2,width=15,textvariable=self.Mango).grid(row=2,column=1,padx=10)

        item4=Label(fruits,text="Grapes",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=3,column=0,pady=11)
        item4_entry=Entry(fruits,borderwidth=2,width=15,textvariable=self.Grapes).grid(row=3,column=1,padx=10)

        item5=Label(fruits,text="Banana",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=4,column=0,pady=11)
        item5_entry=Entry(fruits,borderwidth=2,width=15,textvariable=self.Banana).grid(row=4,column=1,padx=10)

        item6=Label(fruits,text="Papaya",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=5,column=0,pady=11)
        item6_entry=Entry(fruits,borderwidth=2,width=15,textvariable=self.Papaya).grid(row=5,column=1,padx=10)

        item7=Label(fruits,text="Pomegranate",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=6,column=0,pady=11)
        item7_entry=Entry(fruits,borderwidth=2,width=15,textvariable=self.Pomegranate).grid(row=6,column=1,padx=10)
        #=================================== "Grocery"" =====================================================================================
        grocery=LabelFrame(self.root,text="Grocery",font=("Arial Black",12),relief=GROOVE,bd=10,bg="#E5B4F3",fg="#6C3483")
        grocery.place(x=340,y=180,height=380,width=325)

        item8=Label(grocery,text="Ponni Rice",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=0,column=0,pady=11)
        item8_entry=Entry(grocery,borderwidth=2,width=15,textvariable=self.Rice).grid(row=0,column=1,padx=10)

        item9=Label(grocery,text="Wheat",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=1,column=0,pady=11)
        item9_entry=Entry(grocery,borderwidth=2,width=15,textvariable=self.Wheat).grid(row=1,column=1,padx=10)

        item10=Label(grocery,text="Ragi",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=2,column=0,pady=11)
        item10_entry=Entry(grocery,borderwidth=2,width=15,textvariable=self.Ragi).grid(row=2,column=1,padx=10)

        item11=Label(grocery,text="Coconut oil",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=3,column=0,pady=11)
        item11_entry=Entry(grocery,borderwidth=2,width=15,textvariable=self.oil).grid(row=3,column=1,padx=10)

        item12=Label(grocery,text="White Sugar",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=4,column=0,pady=11)
        item12_entry=Entry(grocery,borderwidth=2,width=15,textvariable=self.sugar).grid(row=4,column=1,padx=10)

        item13=Label(grocery,text="Toor Daal",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=5,column=0,pady=11)
        item13_entry=Entry(grocery,borderwidth=2,width=15,textvariable=self.dal).grid(row=5,column=1,padx=10)

        item14=Label(grocery,text="Premium Tea",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=6,column=0,pady=11)
        item14_entry=Entry(grocery,borderwidth=2,width=15,textvariable=self.tea).grid(row=6,column=1,padx=10)
        #========================================Beauty & Hygiene ===============================================================================
        hygine=LabelFrame(self.root,text="Beauty & Hygiene",font=("Arial Black",12),relief=GROOVE,bd=10,bg="#E5B4F3",fg="#6C3483")
        hygine.place(x=677,y=180,height=380,width=325)

        item15=Label(hygine,text="Orange",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=0,column=0,pady=11)
        item15_entry=Entry(hygine,borderwidth=2,width=15,textvariable=self.soap).grid(row=0,column=1,padx=10)

        item16=Label(hygine,text="Aloo Tikki Chaat",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=1,column=0,pady=11)
        item16_entry=Entry(hygine,borderwidth=2,width=15,textvariable=self.shampoo).grid(row=1,column=1,padx=10)

        item17=Label(hygine,text="Dahi Vada",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=2,column=0,pady=11)
        item17_entry=Entry(hygine,borderwidth=2,width=15,textvariable=self.lotion).grid(row=2,column=1,padx=10)

        item18=Label(hygine,text="Pav Bhaji",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=3,column=0,pady=11)
        item18_entry=Entry(hygine,borderwidth=2,width=15,textvariable=self.cream).grid(row=3,column=1,padx=10)

        item19=Label(hygine,text="Bhel Puri",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=4,column=0,pady=11)
        item19_entry=Entry(hygine,borderwidth=2,width=15,textvariable=self.foam).grid(row=4,column=1,padx=10)

        item20=Label(hygine,text="Soup",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=5,column=0,pady=11)
        item20_entry=Entry(hygine,borderwidth=2,width=15,textvariable=self.mask).grid(row=5,column=1,padx=10)

        item21=Label(hygine,text="Pokara",font=("Arial Black",11),bg="#E5B4F3",fg="#6C3483").grid(row=6,column=0,pady=11)
        item21_entry=Entry(hygine,borderwidth=2,width=15,textvariable=self.sanitizer).grid(row=6,column=1,padx=10)
        #=====================================================billarea==============================================================================
        billarea=Frame(self.root,bd=10,relief=GROOVE,bg="#E5B4F3")
        billarea.place(x=1010,y=188,width=330,height=372)

        bill_title=Label(billarea,text="Bill Area",font=("Arial Black",17),bd=7,relief=GROOVE,bg="#E5B4F3",fg="#6C3483").pack(fill=X)

        scrol_y=Scrollbar(billarea,orient=VERTICAL)
        self.txtarea=Text(billarea,yscrollcommand=scrol_y.set)
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH,expand=1)
        #=================================================billing menu=========================================================================================
        billing_menu=LabelFrame(self.root,text="Billing Summary",font=("Arial Black",12),relief=GROOVE,bd=10,bg="#A569BD",fg="white")
        billing_menu.place(x=0,y=560,relwidth=1,height=137)

        total_fruits=Label(billing_menu,text="Total Fruits Price",font=("Arial Black",11),bg="#A569BD",fg="white").grid(row=0,column=0)
        total_fruits_entry=Entry(billing_menu,width=30,borderwidth=2,textvariable=self.total_sna).grid(row=0,column=1,padx=10,pady=7)

        total_grocery=Label(billing_menu,text="Total Grocery Price",font=("Arial Black",11),bg="#A569BD",fg="white").grid(row=1,column=0)
        total_grocery_entry=Entry(billing_menu,width=30,borderwidth=2,textvariable=self.total_gro).grid(row=1,column=1,padx=10,pady=7)


        total_hygine=Label(billing_menu,text="Total Beauty & Hygeine Price",font=("Arial Black",11),bg="#A569BD",fg="white").grid(row=2,column=0)
        total_hygine_entry=Entry(billing_menu,width=30,borderwidth=2,textvariable=self.total_hyg).grid(row=2,column=1,padx=10,pady=7)

        tax_fruits=Label(billing_menu,text="Fruits Tax",font=("Arial Black",11),bg="#A569BD",fg="white").grid(row=0,column=2)
        tax_fruits_entry=Entry(billing_menu,width=30,borderwidth=2,textvariable=self.a).grid(row=0,column=3,padx=10,pady=7)

        tax_grocery=Label(billing_menu,text="Grocery Tax",font=("Arial Black",11),bg="#A569BD",fg="white").grid(row=1,column=2)
        tax_grocery_entry=Entry(billing_menu,width=30,borderwidth=2,textvariable=self.b).grid(row=1,column=3,padx=10,pady=7)


        tax_hygine=Label(billing_menu,text="Beauty & Hygeine Tax",font=("Arial Black",11),bg="#A569BD",fg="white").grid(row=2,column=2)
        tax_hygine_entry=Entry(billing_menu,width=30,borderwidth=2,textvariable=self.c).grid(row=2,column=3,padx=10,pady=7)

        button_frame=Frame(billing_menu,bd=7,relief=GROOVE,bg="#6C3483")
        button_frame.place(x=830,width=500,height=95)

        button_total=Button(button_frame,text="Total Bill",font=("Arial Black",15),pady=10,bg="#E5B4F3",fg="#6C3483",command=lambda:total(self)).grid(row=0,column=0,padx=12)
        button_clear=Button(button_frame,text="Clear Field",font=("Arial Black",15),pady=10,bg="#E5B4F3",fg="#6C3483",command=lambda:clear(self)).grid(row=0,column=1,padx=10,pady=6)
        button_exit=Button(button_frame,text="Exit",font=("Arial Black",15),pady=10,bg="#E5B4F3",fg="#6C3483",width=8,command=lambda:exit1(self)).grid(row=0,column=2,padx=10,pady=6)
        intro(self)


def total(self):
    if (self.c_name.get=="" or self.phone.get()==""):
        messagebox.showerror("Error", "Fill the complete Customer Details!!")
    self.Ap=self.Apple.get()*120
    self.Or=self.Orange.get()*40
    self.Ma=self.Mango.get()*10
    self.Gra=self.Grapes.get()*20
    self.Ba=self.Banana.get()*30
    self.Pa=self.Papaya.get()*60
    self.Po=self.Pomegranate.get()*15
    total_fruits_price=(
                self.Ap+
                self.Or+
                self.Ma+
                self.Gra+
                self.Ba+
                self.Pa+
                self.Po)
    self.total_sna.set(str(total_fruits_price)+" Rs")
    self.a.set(str(round(total_fruits_price*0.05,3))+" Rs")

    self.Ri=self.Rice.get()*42
    self.Wh=self.Wheat.get()*120
    self.oi=self.oil.get()*113
    self.ra=self.Ragi.get()*160
    self.su=self.sugar.get()*55
    self.te=self.tea.get()*480
    self.da=self.dal.get()*76
    total_grocery_price=(
        self.Ri+
        self.Wh+
        self.oi+
        self.ra+
        self.su+
        self.te+
        self.da)

    self.total_gro.set(str(total_grocery_price)+" Rs")
    self.b.set(str(round(total_grocery_price*0.01,3))+" Rs")

    self.so=self.soap.get()*30
    self.sh=self.shampoo.get()*180
    self.cr=self.cream.get()*130
    self.lo=self.lotion.get()*500
    self.fo=self.foam.get()*85
    self.ma=self.mask.get()*100
    self.sa=self.sanitizer.get()*20

    total_hygine_price=(
        self.so+
        self.sh+
        self.cr+
        self.lo+
        self.fo+
        self.ma+
        self.sa)

    self.total_hyg.set(str(total_hygine_price)+" Rs")
    self.c.set(str(round(total_hygine_price*0.10,3))+" Rs")
    self.total_all_bill=(total_fruits_price+
                total_grocery_price+
                total_hygine_price+
                (round(total_grocery_price*0.01,3))+
                (round(total_hygine_price*0.10,3))+
                (round(total_fruits_price*0.05,3)))
    self.total_all_bil=str(self.total_all_bill)+" Rs"
    billarea(self)
def intro(self):
    self.txtarea.delete(1.0,END)
    self.txtarea.insert(END,"\tWELCOME TO SUPER MARKET\n\tPhone-No.9876543210")
    self.txtarea.insert(END,f"\n\nBill no. : {self.bill_no.get()}")
    self.txtarea.insert(END,f"\nCustomer Name : {self.c_name.get()}")
    self.txtarea.insert(END,f"\nPhone No. : {self.phone.get()}")
    self.txtarea.insert(END,"\n====================================\n")
    self.txtarea.insert(END,"\nProduct\t\tQty\tPrice\n")
    self.txtarea.insert(END,"\n====================================\n")
def billarea(self):
    intro(self)
    if self.Apple.get()!=0:
        self.txtarea.insert(END,f"Apple\t\t {self.Apple.get()}\t{self.Ap}\n")
    if self.Orange.get()!=0:
        self.txtarea.insert(END,f"Orange\t\t {self.Orange.get()}\t{self.Or}\n")
    if self.Mango.get()!=0:
        self.txtarea.insert(END,f"Mango\t\t {self.Mango.get()}\t{self.Ma}\n")
    if self.Grapes.get()!=0:
        self.txtarea.insert(END,f"Grapes\t\t {self.Grapes.get()}\t{self.Gra}\n")
    if self.Banana.get()!=0:
        self.txtarea.insert(END,f"Banana\t\t {self.Banana.get()}\t{self.Ba}\n")
    if self.Papaya.get()!=0:
        self.txtarea.insert(END,f"Papaya\t\t {self.Papaya.get()}\t{self.Pa}\n")
    if self.Pomegranate.get()!=0:
        self.txtarea.insert(END,f"Pomegranate\t\t {self.Pomegranate.get()}\t{self.Po}\n")
    if self.Rice.get()!=0:
        self.txtarea.insert(END,f"Rice\t\t {self.Rice.get()}\t{self.Ri}\n")
    if self.Wheat.get()!=0:
        self.txtarea.insert(END,f"Wheat\t\t {self.Wheat.get()}\t{self.Wh}\n")
    if self.Ragi.get()!=0:
        self.txtarea.insert(END,f"Ragi\t\t {self.Ragi.get()}\t{self.ri}\n")
    if self.oil.get()!=0:
        self.txtarea.insert(END,f"Oil\t\t {self.oil.get()}\t{self.oi}\n")
    if self.sugar.get()!=0:
        self.txtarea.insert(END,f"Sugar\t\t {self.sugar.get()}\t{self.su}\n")
    if self.dal.get()!=0:
        self.txtarea.insert(END,f"Daal\t\t {self.dal.get()}\t{self.da}\n")
    if self.tea.get()!=0:
        self.txtarea.insert(END,f"Tea\t\t {self.tea.get()}\t{self.te}\n")
    if self.soap.get()!=0:
        self.txtarea.insert(END,f"Soap\t\t {self.soap.get()}\t{self.so}\n")
    if self.shampoo.get()!=0:
        self.txtarea.insert(END,f"Shampoo\t\t {self.shampoo.get()}\t{self.sh}\n")
    if self.lotion.get()!=0:
        self.txtarea.insert(END,f"Lotion\t\t {self.lotion.get()}\t{self.lo}\n")
    if self.cream.get()!=0:
        self.txtarea.insert(END,f"Cream\t\t {self.cream.get()}\t{self.cr}\n")
    if self.foam.get()!=0:
        self.txtarea.insert(END,f"Foam\t\t {self.foam.get()}\t{self.fo}\n")
    if self.mask.get()!=0:
        self.txtarea.insert(END,f"Mask\t\t {self.mask.get()}\t{self.ma}\n")
    if self.sanitizer.get()!=0:
        self.txtarea.insert(END,f"Sanitizer\t\t {self.sanitizer.get()}\t{self.sa}\n")

    self.txtarea.insert(END,f"------------------------------------\n")
    if self.a.get()!="0.0 Rs":
        self.txtarea.insert(END,f"Total Fruits Tax : {self.a.get()}\n")
    if self.b.get()!="0.0 Rs":
        self.txtarea.insert(END,f"Total Grocery Tax : {self.b.get()}\n")
    if self.c.get()!="0.0 Rs":
        self.txtarea.insert(END,f"Total Beauty&Hygine Tax : {self.c.get()}\n")
    self.txtarea.insert(END,f"Total Bill Amount : {self.total_all_bil}\n")
    self.txtarea.insert(END,f"------------------------------------\n")
def clear(self):
        self.txtarea.delete(1.0,END)
        self.Apple.set(0)
        self.Orange.set(0)
        self.Mango.set(0)
        self.Grapes.set(0)
        self.Banana.set(0)
        self.Papaya.set(0)
        self.Pomegranate.set(0)
        self.Rice.set(0)
        self.Wheat.set(0)
        self.Ragi.set(0)
        self.oil.set(0)
        self.sugar.set(0)
        self.dal.set(0)
        self.tea.set(0)
        self.soap.set(0)
        self.shampoo.set(0)
        self.lotion.set(0)
        self.cream.set(0)
        self.foam.set(0)
        self.mask.set(0)
        self.sanitizer.set(0)
        self.total_sna.set(0)
        self.total_gro.set(0)
        self.total_hyg.set(0)
        self.a.set(0)
        self.b.set(0)
        self.c.set(0)
        self.c_name.set(0)
        self.bill_no.set(0)
        self.bill_no.set(0)
        self.phone.set(0)

def exit1(self):
    self.root.destroy()

root=Tk()
obj=Bill_App(root)

# Run the Tkinter event loop
root.mainloop()
