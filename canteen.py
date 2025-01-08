from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta, date

root = Tk()
user_id = ''
#CLASS  For Database overriding commands

class MySQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                                  database=self.database)
        self.cursor = self.connection.cursor()

    def close(self):
        if self.connection:
            self.connection.close()

    def execute(self, query, par=None):
        self.connect()
        if par:
            self.cursor.execute(query, par)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.close()
        return result

    def insert(self, query, par=None):
        self.connect()
        if par:
            self.cursor.execute(query, par)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        self.close()

#Class for Customer Interface

class Canteen:
    def __init__(self, can_root):
        self.root = can_root
        self.root.title("CanteenEase:Simplifying canteen ordering system ")
        self.root.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.database = MySQL("localhost", "root", "Ankush@24", "canteens")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry("1200x600")
        self.root.resizable(False, False)
        self.new_window = None
        self.img = Image.open('images.jpg')
        self.resize = self.img.resize((1200, 600), Image.LANCZOS)
        self.background_img = ImageTk.PhotoImage(self.resize)
        self.background = Label(self.root, image=self.background_img)
        self.background.place(relwidth=1, relheight=1)
        self.img1 = Image.open('food.jpg')
        self.tk_image1 = ImageTk.PhotoImage(self.img1)
        self.food = Button(self.root, image=self.tk_image1, width=90, borderwidth=2, height=73, command=self.food_page)
        self.food.place(x=550, y=318)
        self.img2 = Image.open('drinks.jpg')
        self.tk_image2 = ImageTk.PhotoImage(self.img2)
        self.bill = Button(self.root, image=self.tk_image2, width=87, height=73, command=self.bill)
        self.bill.place(x=670, y=318)
        self.history = Button(self.root, text="History", bg="#FFE0BD", command=self.hist)
        self.history.place(x=1100, y=20)
        self.table = Button(self.root, text="Table Reservation", bg="#FFE0BD", command=self.tab)
        self.table.place(x=1100, y=50)
        self.current = Button(self.root, text="Current Orders ", bg="#FFE0BD", command=self.status)
        self.current.place(x=1100, y=80)

    def tab(self):
        self.new_window = Toplevel(self.root)
        t = Table(self.new_window)

    def bill(self):
        self.new_window = Toplevel(self.root)
        c = BillPaymentApp(self.new_window)

    def food_page(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Select Canteen")
        self.new_window.geometry("700x600")
        self.new_window.configure(bg="lightblue")
        self.nim_img = Image.open('nim.jpg')
        self.tk_nim = ImageTk.PhotoImage(self.nim_img)
        self.nim_button = Button(self.new_window, image=self.tk_nim, command=lambda: self.order("nim", "Nimbalkar"))
        self.nim_button.place(x=70, y=150)
        self.chai_img = Image.open('chaibar.png')
        self.tk_chai = ImageTk.PhotoImage(self.chai_img)
        self.chai_button = Button(self.new_window, image=self.tk_chai, command=lambda: self.order("chai", "ChaiBar"))
        self.chai_button.place(x=70, y=350)
        self.ann_img = Image.open('ann.jpg')
        self.tk_ann = ImageTk.PhotoImage(self.ann_img)
        self.ann_button = Button(self.new_window, image=self.tk_ann, command=lambda: self.order("ann", "Annapurna"))
        self.ann_button.place(x=370, y=150)
        self.caf_img = Image.open('burgerbuddy.jpeg')
        self.tk_caf = ImageTk.PhotoImage(self.caf_img)
        self.caf_button = Button(self.new_window, image=self.tk_caf, command=lambda: self.order("caf", "Cafe"))
        self.caf_button.place(x=370, y=350)

        # self.button = Button(self.new_window, text="Go Back", command=self.back)
        # self.button.place(x=10, y=0)

    def order(self, cant, name):
        self.window = Toplevel(self.new_window)
        # self.new_window.protocol("WM_DELETE_WINDOW", self.closing)
        self.window.title("Menu")
        self.window.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.window.geometry("500x500")
        self.records = self.database.execute("SELECT * FROM " + cant + ";")
        self.menu_listbox = Listbox(self.window, selectmode=MULTIPLE, height=15, width=50)
        for index, item, price in self.records:
            self.menu_listbox.insert(END, f"{index} \t\t {item} \t\t {price}")
        self.menu_listbox.pack()
        order_button = Button(self.window, text="Place Order", command=lambda: self.place_order(name))
        order_button.pack()

    def place_order(self, cant):
        selected_index = self.menu_listbox.curselection()
        selected_items = [self.records[index] for index in selected_index]
        items = ''
        price = 0
        for item in selected_items:
            items += item[1] + ", "
            price += int(item[2])
        ent = (user_id, cant, items[:-2], price, "PREPARING", date.today())
        query = "INSERT INTO ORDERS ( USER_ID, CANTEEN, ITEMS, PRICE, STATUS, DOO) VALUES(%s, %s, %s, %s, %s, %s);"
        self.database.insert(query, ent)
        ent1 = (user_id, cant, items[:-2], price, date.today())
        query = ("INSERT INTO HISTORY ( USER_ID, CANTEEN, ITEMS, PRICE, STATUS, DOO) VALUES(%s, %s, %s, %s, 'UNPAID', "
                 "%s);")
        self.database.insert(query, ent1)
        messagebox.showinfo("Placed", "Order Placed Successfully")
        self.window.destroy()
        self.new_window.destroy()

    def status(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Order Summary")
        self.new_window.geometry("700x600")
        global user_id
        user = user_id
        self.records = self.database.execute("SELECT * FROM ORDERS WHERE USER_ID= '" + user + "' AND( STATUS = "
                                                                                              "'PREPARING' OR  STATUS"
                                                                                              " = 'PREPARED');")
        if self.records != []:
            self.menu_listbox = Listbox(self.new_window, selectmode=MULTIPLE, height=20, width=50)
            for ID, index, Can, item, price, status, doo in self.records:
                self.menu_listbox.insert(END, f"{ID}  \t  {Can} \t {item} \t {price} \t  {status} {doo}")

            self.menu_listbox.pack()
            self.curr_button = Button(self.new_window, text="Confirm", command=self.conf)
            self.curr_button.pack()
        else:
            messagebox.showinfo("Empty", "No Past Orders")
            self.new_window.destroy()

    def conf(self):
        selected_order_index = self.menu_listbox.curselection()
        if not selected_order_index:
            messagebox.showerror("Error", "Please select a order to change status.")
            return

        selected_order_id = self.menu_listbox.get(selected_order_index[0]).split()[0]
        selected_status = self.menu_listbox.get(selected_order_index[0]).split()[4]
        selected_status = selected_status.upper()
        confirm = messagebox.askyesno("Confirm ", f"Did you collect your order ID {selected_order_id}?")
        if confirm and selected_status != "PREPARING":
            messagebox.showinfo("Success", f"Status for Order ID {selected_order_id} successful.")
            self.database.insert(f"UPDATE orders SET status='Delivered' WHERE ORDER_id={selected_order_id}")
            # self.populate_bill_list()
            self.new_window.destroy()
        else:
            messagebox.showerror("Error", "Please select a order that’s prepared")

            # self.window.destroy()

    def hist(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Order History")
        self.new_window.geometry("700x600")
        global user_id
        user = user_id
        self.records = self.database.execute("SELECT * FROM HISTORY WHERE USER_ID= '" + user + "';")
        if self.records != []:
            self.menu_listbox = Listbox(self.new_window, selectmode=MULTIPLE, height=20, width=50)
            a = 0
            for ID, index, Can, item, price, status, doo in self.records:
                a += 1
                self.menu_listbox.insert(END, f"{a}  \t  {Can} \t {item} \t {price} \t  {status} {doo}")
            a = 0
            self.menu_listbox.pack()
        else:
            messagebox.showinfo("Empty", "No Past Orders")
            self.new_window.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
#Class for Billing

class BillPaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Payment System")
        self.root.geometry("400x300")

        # Connect to MySQL database
        # Create Listbox to display bills
        self.bill_listbox = Listbox(self.root, width=50, height=10)
        self.bill_listbox.pack(pady=10)
        self.database = MySQL("localhost", "root", "Ankush@24", "canteens")
        # Populate Listbox with bills
        self.populate_bill_list()

        # Create Pay button
        self.pay_button = Button(self.root, text="Pay", command=self.pay_bill)
        self.pay_button.pack()

    def populate_bill_list(self):
        self.bill_listbox.delete(0, END)
        bills = self.database.execute("SELECT * FROM history where status = 'UNPAID';")
        if bills != []:
            for bill in bills:
                self.bill_listbox.insert(END, f"Bill ID: {bill[0]} - Amount: Rs. {bill[4]}")
        else:
            messagebox.showinfo("No Bills", "No Pending bills")

    def pay_bill(self):
        selected_bill_index = self.bill_listbox.curselection()
        if not selected_bill_index:
            messagebox.showerror("Error", "Please select a bill to pay.")
            return

        selected_bill_id = self.bill_listbox.get(selected_bill_index[0]).split()[2]
        confirm_pay = messagebox.askyesno("Confirm Payment", f"Do you want to pay bill ID {selected_bill_id}?")
        if confirm_pay:
            self.window = Toplevel(self.root)
            # Perform payment operation here (e.g., update database)
            self.cash = Button(self.window, text="Cash", command=lambda: self.cash_message(selected_bill_id))
            self.cash.pack()
            self.upi = Button(self.window, text="Online", command=lambda: self.online(selected_bill_id))
            self.upi.pack()

    def online(self, id):
        self.new_window = Toplevel(self.window)
        self.pay_img = Image.open('GooglePay_QR.jpeg')
        self.tk_pay = ImageTk.PhotoImage(self.pay_img)
        self.pay_Label = Label(self.new_window, image=self.tk_pay)
        self.pay_Label.pack()
        self.done = Button(self.new_window, text="Done", command=lambda: self.message(id))
        self.done.pack()

    def cash_message(self, selected_bill_id):
        messagebox.showinfo("Success", f"Payment for bill ID {selected_bill_id} successful.")
        self.database.insert(f"UPDATE history SET status='PAID' WHERE ORDER_id={selected_bill_id}")
        # self.populate_bill_list()
        # self.new_window.destroy()
        self.window.destroy()
        self.root.destroy()

    def message(self, selected_bill_id):
        messagebox.showinfo("Success", f"Payment for bill ID {selected_bill_id} successful.")
        self.database.insert(f"UPDATE history SET status='PAID' WHERE ORDER_id={selected_bill_id}")
        # self.populate_bill_list()
        self.new_window.destroy()
        self.window.destroy()
        self.root.destroy()
#Class for Table Reservation

class Table:
    def __init__(self, root):
        self.root = root
        self.root.title(" Table Reservation")
        self.root.geometry("400x700")
        self.root.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.root.configure(bg="navajo white")
        # Connect to MySQL database
        self.database = MySQL("localhost", "root", "Ankush@24", "canteens")

        # Create reservation table if not exists
        self.create_reservation_table()

        # Create buttons for each table
        self.create_table_buttons()

    def create_reservation_table(self):
        self.database.insert("""
            CREATE TABLE IF NOT EXISTS reservations (
                table_number INT PRIMARY KEY,
                reserved_until DATETIME, 
                user_id VARCHAR(256)
            )
        """)

    def create_table_buttons(self):
        for i in range(1, 11):  # Assuming 10 tables are available
            button = Button(self.root, text=f"Table {i}", command=lambda table=i: self.reserve_table(table))
            button.pack(pady=5)

    def reserve_table(self, table_number):
        # Check if the table is already reserved
        reservation = self.database.execute("SELECT * FROM reservations WHERE table_number = %s", (table_number,))
        if reservation != []:
            reserved_until = reservation[0][1]
            if reserved_until > datetime.now():
                messagebox.showerror("Error", f"Table {table_number} is already reserved by  {reservation[0][2]}.")
                self.root.destroy()
                return

        # Reserve the table for half an hour
        reserved_until = datetime.now() + timedelta(minutes=30)
        global user_id
        self.database.insert(
            "REPLACE INTO reservations (table_number, reserved_until, user_id) VALUES (%s, %s, '" + user_id + "')",
            (table_number, reserved_until))
        messagebox.showinfo("Success", f"Table {table_number} reserved until {reserved_until} ")
        self.root.destroy()

    def run(self):
        self.root.mainloop()

#Class for Login Interface
class Login:
    def __init__(self, log_root, type):
        self.type = type
        self.root = log_root
        self.root.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.database = MySQL("localhost", "root", "Ankush@24", "canteens")
        self.root.geometry("500x500")
        self.root.title(f"{self.type.capitalize()} Login Page")
        self.root.protocol("WM_DELETE_WINDOW", self.root_closing)
        self.temp_root = None
        self.user = None
        self.password = None
        self.user_label = None
        self.password_label = None
        self.submit_button = None
        self.back_button = None
        self.img1 = Image.open('zcoer-gif1.gif')
        self.tk_image = ImageTk.PhotoImage(self.img1)
        self.name = Label(self.root, image=self.tk_image)
        self.name.place(x=20, y=20)
        self.login_button = Button(self.root, text="Login", width=10, command=self.log_in)
        self.login_button.place(x=230, y=340)
        self.sign_in_button = Button(self.root, text="Sign Up", width=10, command=self.sign_up)
        self.sign_in_button.place(x=230, y=310)
        self.back_button = Button(self.temp_root, text="Go Back", width=10, command=self.backtype)
        self.back_button.place(x=220, y=390)

    def root_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def log_in(self):
        self.root.destroy()
        self.temp_root = Tk()
        self.temp_root.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.database = MySQL("localhost", "root", "Ankush@24", "canteens")
        self.temp_root.geometry("500x500")
        self.temp_root.title("Login page")
        self.temp_root.protocol("WM_DELETE_WINDOW", self.sign_closing)
        self.user = Entry(self.temp_root, width=20)
        self.user.place(x=230, y=210)
        self.user_label = Label(self.temp_root, text="User ID")
        self.user_label.place(x=185, y=210)
        self.password = Entry(self.temp_root, width=20)
        self.password.place(x=230, y=240)
        self.password_label = Label(self.temp_root, text="Password")
        self.password_label.place(x=172, y=240)
        self.submit_button = Button(self.temp_root, text="Submit",
                                    command=lambda: self.check(self.user.get(), self.password.get()))
        self.submit_button.place(x=220, y=260)
        self.back_button = Button(self.temp_root, text="Go Back", width=10, command=self.back)
        self.back_button.place(x=220, y=290)

    def sign_closing(self):
        if messagebox.askokcancel("Quit", "Do you want tp quit?"):
            self.temp_root.destroy()

    def check(self, user, password):
        record = self.database.execute(
            "SELECT * FROM " + self.type + " WHERE USER_ID ='" + user + "' AND PASSWORD = '" + password + "';")
        if not record:
            messagebox.showinfo("No user found", "Incorrect details")
            self.user.delete(0, END)
            self.password.delete(0, END)
        else:
            global user_id
            user_id = user
            self.temp_root.destroy()
            new_root = Tk()
            if self.type == "CUSTOMER":
                app = Canteen(new_root)
            if self.type == "MANAGER":
                app = Manager(new_root)
            # app.__init__(new_root)

    def sign_up(self):
        self.root.destroy()
        self.temp_root = Tk()
        self.temp_root.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.database = MySQL("localhost", "root", "Ankush@24", "canteens")
        self.temp_root.geometry("500x500")
        self.temp_root.title("Sign Up page")
        self.temp_root.protocol("WM_DELETE_WINDOW", self.sign_closing)
        self.user = Entry(self.temp_root, width=20)
        self.user.place(x=230, y=210)
        self.user_label = Label(self.temp_root, text="User ID")
        self.user_label.place(x=185, y=210)
        self.password = Entry(self.temp_root, width=20)
        self.password.place(x=230, y=240)
        self.password_label = Label(self.temp_root, text="Password")
        self.password_label.place(x=172, y=240)
        self.submit_button = Button(self.temp_root, text="Submit",
                                    command=lambda: self.sign(self.user.get(), self.password.get()))
        self.submit_button.place(x=220, y=260)
        self.back_button = Button(self.temp_root, text="Go Back", width=10, command=self.back)
        self.back_button.place(x=220, y=290)

    def sign(self, user, password):
        record = self.database.execute(
            "SELECT * FROM " + self.type + " WHERE USER_ID ='" + user + "' AND PASSWORD = '" + password + "';")
        if not record:
            query = "INSERT INTO " + self.type + " (USER_ID, PASSWORD) VALUES ('" + user + "', '" + password + "');"
            self.database.insert(query)
            global user_id
            user_id = user
            self.temp_root.destroy()
            new_root = Tk()
            if self.type == "CUSTOMER":
                app = Canteen(new_root)
            if self.type == "MANAGER":
                app = Manager(new_root)
            # app.__init__(new_root)
        else:
            messagebox.showinfo(" Already User ", "Already a User please try  to login ")
            self.user.delete(0, END)
            self.password.delete(0, END)

    def back(self):
        self.temp_root.destroy()
        log_root = Tk()
        self.__init__(log_root, self.type)

    def backtype(self):
        self.root.destroy()
        log_root = Tk()
        a = Main(log_root)

#Class for Main Page
class Main:
    def __init__(self, main_root):
        self.root = main_root
        self.root.iconbitmap(r"C:\Users\kaila\PycharmProjects\Canteen Ordering system\ZEAL_Education_Society_Logo.ico")
        self.database = MySQL("localhost", "root", "Ankush@24", "canteens")
        self.root.geometry("500x500")
        self.root.title("User Type Page")
        # self.root.protocol("WM_DELETE_WINDOW", self.root_closing)
        self.img1 = Image.open('ZEAL_Education_Society_Logo.ico')
        self.tk_image = ImageTk.PhotoImage(self.img1)
        self.name = Label(self.root, image=self.tk_image)
        self.name.place(x=20, y=20)
        self.login_button = Button(self.root, text="Manager", width=10, command=self.man)
        self.login_button.place(x=230, y=340)
        self.sign_in_button = Button(self.root, text="Customer", width=10, command=self.cust)
        self.sign_in_button.place(x=230, y=310)

    def man(self):
        self.root.destroy()
        self.temp_root = Tk()
        self.a = Login(self.temp_root, "MANAGER")

    def cust(self):
        self.root.destroy()
        self.temp_root = Tk()
        self.a = Login(self.temp_root, "CUSTOMER")



#Class for Manager Interface
class Manager:
    def __init__(self, can_root):
        self.new_item = None
        self.can = None
        self.exists = None
        self.new_window = None
        self.root = can_root
        self.root.title("CanteenEase:Simplifying canteen ordering system ")
        self.root.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.database = MySQL("localhost", "root", "Ankush@24", "canteens")
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry("1200x600")
        self.root.resizable(False, False)
        self.img = Image.open('bg.jpg')
        self.resize = self.img.resize((1200, 600), Image.LANCZOS)
        self.background_img = ImageTk.PhotoImage(self.resize)
        self.background = Label(self.root, image=self.background_img)
        self.background.place(relwidth=1, relheight=1)
        self.update_button = Button(self.root, text="Update Menu", command=self.update, width=20, height=10, bg="cyan")
        self.update_button.place(x=60, y=40)
        self.add_button = Button(self.root, text="Add Item", command=self.add_item, width=20, height=10, bg="cyan")
        self.add_button.place(x=250, y=40)
        self.stat_button = Button(self.root, text="Pending Orders", command=self.prep_item, width=20, height=10,
                                  bg="cyan")
        self.stat_button.place(x=60, y=250)

    def add_item(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("CanteenEase:Simplifying canteen ordering system ")
        self.new_window.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.new_window.geometry("500x300")
        self.can = Entry(self.new_window, width=20)
        self.can.place(x=170, y=40)
        self.cant = Label(self.new_window, text="Canteen Name")
        self.cant.place(x=170, y=20)
        self.item_name = Entry(self.new_window, width=20)
        self.item_name.place(x=170, y=60)
        self.ite = Label(self.new_window, text="New Item Name")
        self.ite.place(x=170, y=80)
        self.pr_item = Entry(self.new_window, width=20)
        self.pr_item.place(x=170, y=100)
        self.new_pri = Label(self.new_window, text="New Price Name")
        self.new_pri.place(x=170, y=120)
        self.add = Button(self.new_window, text="Add", width=5,
                          command=lambda: self.check(self.can.get(), self.item_name.get(), self.pr_item.get()))
        self.add.place(x=170, y=140)

    def check(self, can, new, price):
        try:
            # Query to check if table exists
            query = f"SHOW TABLES LIKE '{can}'"
            result = self.database.execute(query)
            if result:
                present = self.database.execute("SELECT * FROM " + can + " WHERE ITEM = '" + new + "';")
                if not present:
                    ent = (new, price)
                    self.database.insert("INSERT INTO " + can + " (ITEM, PRICE) VALUES(%s, %s);", ent)
                    messagebox.showinfo("Success", "Item Added Successfully")
                    # self.window.destroy()
                else:
                    messagebox.showerror("Error", " Item Already exists try re-entering")
                    self.item_name.delete(0, END)
                    self.pr_item.delete(0, END)
                    self.can.delete(0, END)
            else:
                messagebox.showerror("Table Existence", f"The table {can} does not exist.")
                self.item_name.delete(0, END)
                self.pr_item.delete(0, END)
                self.can.delete(0, END)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("CanteenEase:Simplifying canteen ordering system ")
        self.new_window.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.new_window.geometry("500x300")
        self.item_name = Button(self.new_window, text="Update Item name", width=15, height=5, command=self.item)
        self.item_name.place(x=80, y=20)
        self.item_price = Button(self.new_window, text="Update Item price", width=15, height=5, command=self.price)
        self.item_price.place(x=280, y=20)

    def item(self):
        self.window = Toplevel(self.new_window)
        self.window.title("CanteenEase:Simplifying canteen ordering system ")
        self.window.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.window.geometry("500x300")
        self.can = Entry(self.window, width=20)
        self.can.place(x=170, y=40)
        self.cant = Label(self.window, text="Canteen Name")
        self.cant.place(x=170, y=20)
        self.exists = Entry(self.window, width=20)
        self.exists.place(x=170, y=60)
        self.exist = Label(self.window, text="Existing Item Name")
        self.exist.place(x=170, y=80)
        self.new_item = Entry(self.window, width=20)
        self.new_item.place(x=170, y=100)
        self.new = Label(self.window, text="New Item Name")
        self.new.place(x=170, y=120)

        self.ubut = Button(self.window, text="Update", width=10,
                           command=lambda: self.it(self.exists.get(), self.new_item.get(), self.can.get()))
        self.ubut.place(x=200, y=140)

    def it(self, item_n, new, can):
        try:
            # Query to check if table exists
            query = f"SHOW TABLES LIKE '{can}'"
            result = self.database.execute(query)
            if result:
                present = self.database.execute("SELECT * FROM " + can + " WHERE ITEM = '" + item_n + "';")
                if present != []:
                    self.database.insert("UPDATE " + can + " SET ITEM = '" + new + "' WHERE ITEM = '" + item_n + "'")
                    messagebox.showinfo("Success", "Item Updated Successfully")
                    self.window.destroy()
                else:
                    messagebox.showerror("Error", " Couldn't find such an item try re-entering")
                    self.exists.delete(0, END)
                    self.new_item.delete(0, END)
                    self.can.delete(0, END)
            else:
                messagebox.showerror("Table Existence", f"The table {can} does not exist.")
                self.exists.delete(0, END)
                self.new_item.delete(0, END)
                self.can.delete(0, END)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def price(self):
        self.window = Toplevel(self.new_window)
        self.window.title("CanteenEase:Simplifying canteen ordering system ")
        self.window.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.window.geometry("500x300")
        self.can = Entry(self.window, width=20)
        self.can.place(x=170, y=20)
        self.cant = Label(self.window, text="Canteen Name")
        self.cant.place(x=170, y=40)
        self.exists = Entry(self.window, width=20)
        self.exists.place(x=170, y=60)
        self.exist = Label(self.window, text=" Item Name")
        self.exist.place(x=170, y=80)
        self.new_item = Entry(self.window, width=20)
        self.new_item.place(x=170, y=100)
        self.new = Label(self.window, text="New Price")
        self.new.place(x=170, y=120)

        self.ubut = Button(self.window, text="Update", width=10,
                           command=lambda: self.pr(self.exists.get(), self.new_item.get(), self.can.get()))
        self.ubut.place(x=170, y=140)

    def pr(self, item_n, new, can):
        try:
            # Query to check if table exists
            query = f"SHOW TABLES LIKE '{can}'"
            result = self.database.execute(query)
            if result:
                present = self.database.execute("SELECT * FROM " + can + " WHERE ITEM = '" + item_n + "';")
                if present != []:
                    self.database.insert("UPDATE " + can + " SET Price = '" + new + "' WHERE ITEM = '" + item_n + "'")
                    messagebox.showinfo("Success", "Item Updated Successfully")
                    self.window.destroy()
                else:
                    messagebox.showerror("Error", " Couldn't find such an item try re-entering")
                    self.exists.delete(0, END)
                    self.new_item.delete(0, END)
                    self.can.delete(0, END)
            else:
                messagebox.showerror("Table Existence", f"The table {can} does not exist.")
                self.exists.delete(0, END)
                self.new_item.delete(0, END)
                self.can.delete(0, END)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def prep_item(self):
        self.window = Toplevel(self.root)
        self.window.title("CanteenEase:Simplifying canteen ordering system ")
        self.window.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.window.geometry("500x300")
        self.can = Entry(self.window, width=20)
        self.can.place(x=170, y=20)
        self.cant = Label(self.window, text="Canteen Name")
        self.cant.place(x=170, y=40)
        self.ubut = Button(self.window, text="Update", width=10, command=lambda: self.prep_it(self.can.get()))
        self.ubut.place(x=170, y=140)

    def prep_it(self, can):
        self.new_window = Toplevel(self.root)
        self.new_window.title("CanteenEase:Simplifying canteen ordering system ")
        self.new_window.iconbitmap("ZEAL_Education_Society_Logo.ico")
        self.new_window.geometry("500x300")
        self.pend_listbox = Listbox(self.new_window, width=50, height=10)
        self.pend_listbox.pack(pady=10)
        self.pend_listbox.delete(0, END)
        print(can)
        orders = self.database.execute(
            "SELECT * FROM orders where status = 'PREPARING'  and CANTEEN = '" + can[1:] + "';")
        print(orders)
        if orders != []:
            for order in orders:
                self.pend_listbox.insert(END, f"Order ID: {order[0]} - Items: . {order[3]}")

            self.pay_button = Button(self.new_window, text="Confirm", command=self.conf)
            self.pay_button.pack()
        else:
            messagebox.showinfo("No Orders", "No Pending Orders")

    def conf(self):
        selected_order_index = self.pend_listbox.curselection()
        if not selected_order_index:
            messagebox.showerror("Error", "Please select a order to change status.")
            return

        selected_order_id = self.pend_listbox.get(selected_order_index[0]).split()[2]
        confirm = messagebox.askyesno("Confirm ", f"Do you want to Change Status for Order ID {selected_order_id}?")
        if confirm:
            messagebox.showinfo("Success", f"Status for Order ID {selected_order_id} successful.")
            self.database.insert(f"UPDATE orders SET status='PREPARED' WHERE ORDER_id={selected_order_id}")
            # self.populate_bill_list()
            self.new_window.destroy()
            self.window.destroy()


a = Main(root)
root.mainloop()
