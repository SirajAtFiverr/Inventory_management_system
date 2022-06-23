# Creating Home Window of the Application

# Importing the necessary modules
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import datetime
import calendar
# import os

# from jmespath import search





class Main(Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("{0}x{1}+-10+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.resizable(False, False)
        icon  = PhotoImage(file="icons/icon.png")
        self.iconphoto(True, icon)
        self.configure(bg="white")
        
        # Adding menu frame
        frame = Frame(self, bg="red")
        frame.pack(side="right", fill="both", expand=True)

        # Adding side menu
        menu = SideMenu(self, frame)
        menu.pack(side="left", fill="y")

        self.mainloop()

class SideMenu(Frame):

    # Constants
    MENU_LABEL_TEXT = "Menu"
    MENU_NAMES = ("HOME", "MANAGE PRODUCTS", "DAILY SALE", "SALE STATS")

    def __init__(self, parent, menuFrame, width=300, bg="gray"):
        Frame.__init__(self, parent, width=width, bg=bg)  # Initializing the Frame

        self.menuFrame = menuFrame
        self.active_menu = None

        # Creating the Side Menu Label
        Label(self, text=self.MENU_LABEL_TEXT, font=("Helvetica", 30), bg="white", fg="black").pack(side="top", fill="x", padx=10, pady=10)
        
        self.add_menues(self.MENU_NAMES)

    def add_menues(self, menu_names):
        ICON_LIST = self.load_icons()
        for i, name in enumerate(menu_names):

            # Setting Home as the active menu
            if name == "HOME":
                label = Label(self, text=name, image=ICON_LIST[i], font=("Helvetica", 20), bg='white', compound=LEFT)
                self.active_menu = label
                Home(self.menuFrame)
            else:
                label = Label(self, text=name, image=ICON_LIST[i], font=("Helvetica", 20), bg='gray', compound=LEFT)
            
            label.image = ICON_LIST[i]
            label.pack(anchor="w", fill=BOTH, pady=10)
            label.bind("<Button-1>", lambda event, arg=label: self.menu_clicked(event, arg))

    def menu_clicked(self, event, label):
        self.active_menu.config(bg="gray")
        label.config(bg="white")

        label_txt = label.cget("text")

        for widget in self.menuFrame.winfo_children():
            widget.destroy()

        if label_txt == "HOME":
            Home(self.menuFrame)
        elif label_txt == "MANAGE PRODUCTS":
            ManageProduct(self.menuFrame)
        elif label_txt == "DAILY SALE":
            DailySale(self.menuFrame)
        elif label_txt == "SALE STATS":
            SalesStat(self.menuFrame)

        self.active_menu = label
    
    def  load_icons(self):
        return (ImageTk.PhotoImage(Image.open("icons/home.png")), ImageTk.PhotoImage(Image.open("icons/product.png")), ImageTk.PhotoImage(Image.open("icons/sale.png")), ImageTk.PhotoImage(Image.open("icons/stats.png")))

# Creating the Home Window
class Home:

    # Constants
    HOME_LABEL_TEXT = "Welcome to the Home Page"
    LABEL2_TXT = "Shop Inventory Management System"
    LABEL3_TXT = "Arman Electric \n & \n Electronics Store"
    LABEL4_TXT = "Created By: SIRAJ SHABBIR"
    LABEL5_TXT = "Version: 1.0"


    def __init__(self, master):
        self.master = master
        self.master.configure(background="white")

        # Creating the Home Label
        Label(self.master, text=self.HOME_LABEL_TEXT, font=("Helvetica", 36), bg="white", fg="RED").place(x=60, y=10)

        # Creating Label 2
        Label(self.master, text=self.LABEL2_TXT, font=("Helvetica", 18), bg="white", fg="green").place(x=175, y=60)

        # Creating Label 3
        Label(self.master, text=self.LABEL3_TXT, font=("roman", 60), bg="white", fg="blue").place(x=60, y=120)
        # Creating Label 4
        Label(self.master, text=self.LABEL4_TXT, font=("courier", 32), bg="white", fg="orange").place(x=20, y=440)
         # Creating Label 5
        Label(self.master, text=self.LABEL5_TXT, font=("Courier New", 60), bg="white", fg="green").place(x=60, y=550)

class ManageProduct:

    ENTRY_NAMES = ("Product Name:", "Cost Price:", "Selling Price:", "Product Quantity:")
    def __init__(self, master):
        self.master = master
        self.master.configure(background="white")

        self.db = DataBase()

        Label(self.master, text="Manage Products", font=("Helvetica", 36), bg="white", fg="RED").pack()

        frame = Frame(self.master, bg="white")
        frame.pack(fill="x")

        self.entries = []

        for i, name in enumerate(self.ENTRY_NAMES):
            Label(frame, text=name, font=("Helvetica", 16), bg="white", fg="black").grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entry = Entry(frame, font=("Helvetica", 16), bg="white", fg="black")
            entry.grid(row=i, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky="w")

            self.entries.append(entry)
        

        # Creating Buttons
        Button(self.master, text="Add", font=("Helvetica", 16), bg="white", fg="black", command=self.add_product).place(x=10, y=340, width=100, height=50)
        Button(self.master, text="Update", font=("Helvetica", 16), bg="white", fg="black", command=self.update_product).place(x=120, y=340, width=100, height=50)
        Button(self.master, text="Delete", font=("Helvetica", 16), bg="white", fg="black", command=self.delete_product).place(x=230, y=340, width=100, height=50)
        Button(self.master, text="Clear", font=("Helvetica", 16), bg="white", fg="black", command=self.clear).place(x=340, y=340, width=100, height=50)

        self.search_entry = Entry(self.master, font=("Helvetica", 16), bg="white", fg="black")
        self.search_entry.place(x=10, y=400, width=220, height=50)
        self.search_entry.bind("<KeyRelease>", self.on_key_pressed)

        Button(self.master, text="Search", font=("Helvetica", 16), bg="white", fg="black", command=self.search_product).place(x=240, y=400, width=100, height=50)
        
        self.product_list = ttk.Treeview(self.master, columns=("1", "2", "3", "4", "5"), show="headings", )
        self.product_list.place(x=10, y=460, relwidth=.97, relheight=.35)

        self.product_list.column("1", width=180)
        self.product_list.column("2", width=150, anchor=CENTER)
        self.product_list.column("3", width=150, anchor=CENTER)
        self.product_list.column("4", width=150, anchor=CENTER)
        self.product_list.column("5", width=180, anchor=CENTER)

        # Changing Font size
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14))

        self.product_list.heading('1', text='Product Name', anchor="w")
        self.product_list.heading('2', text='Cost Price', anchor=CENTER)
        self.product_list.heading('3', text='Selling Price', anchor=CENTER)
        self.product_list.heading('4', text='Sold Products', anchor=CENTER)
        self.product_list.heading('5', text='Remaining Products', anchor=CENTER)

        # Adding Scroll bar to product list
        yscrollbar = Scrollbar(self.product_list, orient="vertical", command=self.product_list.yview)
        xscrollbar = Scrollbar(self.product_list, orient="horizontal", command=self.product_list.xview)

        self.product_list.configure(yscrollcommand=yscrollbar.set)
        self.product_list.configure(xscrollcommand=xscrollbar.set)

        # Show/Hide Scroll bar
        self.product_list.bind("<Leave>", lambda event: self.hidescrollbars(xscrollbar, yscrollbar))
        self.product_list.bind("<Enter>", lambda event: self.showscrollbars(xscrollbar, yscrollbar))

        # Binding product list
        self.product_list.bind('<<TreeviewSelect>>', self.fill_entries)

        # Refresh Product List
        self.refreshList()

    def showscrollbars(self, xscrollbar, yscrollbar):
        xscrollbar.pack(side="bottom", fill="x")
        yscrollbar.pack(side="right", fill="y")
    
    
    def hidescrollbars(seld, xscrollbar, yscrollbar):
        xscrollbar.pack_forget()
        yscrollbar.pack_forget()

    def get_product_info(self):
        try:
            if not all([entry.get() for entry in self.entries]):raise AttributeError("Please fill all the entries")
            return [self.entries[0].get().lower(), float(self.entries[1].get()), float(self.entries[2].get()), int(self.entries[3].get())]
        except AttributeError:
            messagebox.showwarning("Error", "Please fill all the entries")
        except ValueError:
            messagebox.showwarning("Error", "Please enter valid values")
    
    def clear_list(self):
        for i in self.product_list.get_children():
            self.product_list.delete(i)
    
    def refreshList(self):
        products = self.db.readAllProductInfo()
        self.clear_list()
        if products:
            for product in products:
                sold_products = self.db.countSoldProducts(product[0])
                remaining_products = product[-1] - sold_products
                product = product[:-1] 
                product = product + (sold_products, remaining_products, )
                self.product_list.insert('', 'end', values=product)

    def add_product(self):
        product_info = self.get_product_info()
        if product_info:
            
            try:
                self.db.insertProduct(product_info)
                messagebox.showinfo("Product Added", "Product Added Successfully")
                self.refreshList()
                self.clear()
            except Exception as e:
                messagebox.showwarning("Error", e)
                messagebox.showwarning("Warning", "Product Already Exits")
            

    def update_product(self):
        product_info = self.get_product_info()
        if product_info:
            try:
                self.db.updateProduct(product_info)
                messagebox.showinfo("Product Updated", "Product Updated Successfully")
                self.refreshList()
                self.clear()
            except:
                messagebox.showerror("Product not found", "'{}' is not found in the database".format(product_info[0]))

    def delete_product(self):
        product_info = self.get_product_info()
        if product_info:
            if messagebox.askquestion("Delete Product", "Are you sure you want to delete this product?"):
                try:
                    if not self.db.countSoldProducts(product_info[0]):
                        self.db.deleteProduct(product_info[0])
                        messagebox.showinfo("Product Deleted", "Product Deleted Successfully")
                        self.refreshList()
                        self.clear()
                    else:
                        messagebox.showinfo("Product can't be deleted", "Product can't be deleted because product has sales.")
                except:
                    messagebox.showerror("Product Not Found", "'{}' is not found in the database".format(product_info[0]))
                
    def fill_entries(self, event):
        self.clear()
        info = self.product_list.item(self.product_list.focus())["values"]
        # Calculating total products
        info[-2] = info[-1] + info[-2]
        for i, entry in enumerate(self.entries):
            entry.insert(0, info[i])

    def clear(self):
        for entry in self.entries:
            entry.delete(0, END)


    def search_product(self):
        toSeacrch = self.search_entry.get().lower().strip()
        product = self.db.getProductInfo(toSeacrch)
        self.clear_list()
        if product:
            sold_products = self.db.countSoldProducts(product[0])
            remaining_products = product[-1] - sold_products
            product = product[:-1] 
            product = product + (sold_products, remaining_products, )

            self.product_list.insert('', 'end', values=product)
    
    def on_key_pressed(self, event):
        toSeacrch = self.search_entry.get().lower().strip()
        if len(toSeacrch) <= 1 and not event.char.isalnum():
            self.refreshList()
            return

        def filter_products(product):
            if toSeacrch in product[0]:
                return product[0]

        products = self.db.readAllProductInfo()

        products = filter(filter_products, products)
        self.clear_list()
        for product in products:
            sold_products = self.db.countSoldProducts(product[0])
            remaining_products = product[-1] - sold_products
            product = product[:-1] 
            product = product + (sold_products, remaining_products, )

            self.product_list.insert('', 'end', values=product)
        


class DailySale:
    ENTRIES_NAMES = ("Product Name:", "Price:", "Quantity:")
    def __init__(self, master):
        self.master = master
        self.master.configure(background="white")

        self.db = DataBase()

        Label(self.master, text="Manage Daily Sale", font=("Helvetica", 36), bg="white", fg="RED").pack()

        frame = Frame(self.master, bg="white")
        frame.pack(fill="x")

        self.entries = []

        for i, name in enumerate(self.ENTRIES_NAMES):
            Label(frame, text=name, font=("Helvetica", 16), bg="white", fg="black").grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entry = Entry(frame, font=("Helvetica", 16), bg="white", fg="black")
            entry.grid(row=i, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky="w")

            self.entries.append(entry)
        
        # Creating Buttons
        Button(self.master, text="Add Sale", font=("Helvetica", 16), bg="white", fg="black", command=self.add_sale).place(x=10, y=280, width=140, height=50)
        Button(self.master, text="Retutn Sale", font=("Helvetica", 16), bg="white", fg="black", command=self.return_sale).place(x=160, y=280, width=140, height=50)
        Button(self.master, text="Clear", font=("Helvetica", 16), bg="white", fg="black", command=self.clear).place(x=310, y=280, width=140, height=50)

        Label(self.master, text="Today's Sales", font=("Helvetica", 32), bg="white", fg="red").place(x=210, y=340)

        self.sale_list = ttk.Treeview(self.master, columns=("Product Name", "Sold Price", "Original Price", "Product Quantity", "Sale/Return"), show="headings", )
        self.sale_list.place(x=10, y=400, relwidth=.97, relheight=.32)

        self.sale_list.column("Product Name", width=180)
        self.sale_list.column("Sold Price", width=180, anchor=CENTER)
        self.sale_list.column("Original Price", width=150, anchor=CENTER)
        self.sale_list.column("Product Quantity", width=150, anchor=CENTER)
        self.sale_list.column("Sale/Return", width=150, anchor=CENTER)
        

        # Changing Font size
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14))

        self.sale_list.heading('Product Name', text='Product Name', anchor="w")
        self.sale_list.heading('Sold Price', text='Sold/Return Price')
        self.sale_list.heading('Original Price', text='Original Price')
        self.sale_list.heading('Product Quantity', text='Product Quantity')
        self.sale_list.heading('Sale/Return', text='Sale/Return')

        # Adding Scroll bar to product list
        yscrollbar = Scrollbar(self.sale_list, orient="vertical", command=self.sale_list.yview)
        xscrollbar = Scrollbar(self.sale_list, orient="horizontal", command=self.sale_list.xview)

        self.sale_list.configure(yscrollcommand=yscrollbar.set)
        self.sale_list.configure(xscrollcommand=xscrollbar.set)

        # Show/Hide Scroll bar
        self.sale_list.bind("<Leave>", lambda event: self.hidescrollbars(xscrollbar, yscrollbar))
        self.sale_list.bind("<Enter>", lambda event: self.showscrollbars(xscrollbar, yscrollbar))

        # Binding sale list
        self.sale_list.bind('<<TreeviewSelect>>', self.fill_entries)

        Label(self.master, text="Total Sale:", font=("Helvetica", 22), bg="white", fg="red").place(x=10, y=660)
        Label(self.master, text="Total Return:", font=("Helvetica", 22), bg="white", fg="red").place(x=320, y=660)

        self.sale_label = Label(self.master, text="Rs.0.0", font=("Helvetica", 18), bg="white", fg="black")
        self.sale_label.place(x=150, y=665)

        self.return_label = Label(self.master, text="Rs.0.0", font=("Helvetica", 18), bg="white", fg="black")
        self.return_label.place(x=490, y=665)

        # Refreshing sale list
        self.refreshList()

    def showscrollbars(self, xscrollbar, yscrollbar):
        xscrollbar.pack(side="bottom", fill="x")
        yscrollbar.pack(side="right", fill="y")
    
    def hidescrollbars(seld, xscrollbar, yscrollbar):
        xscrollbar.pack_forget()
        yscrollbar.pack_forget()
    
    def refreshSaleLabels(self, total_sale, total_return):
        self.sale_label.config(text="Rs.{}".format(total_sale - total_return))
        self.return_label.config(text="Rs.{}".format(total_return))

    def get_sale_info(self):
        try:
            if not all([entry.get() for entry in self.entries]):raise AttributeError("Please fill all the entries")
            return [self.entries[0].get().lower(), float(self.entries[1].get()), int(self.entries[2].get())]
        except AttributeError:
            messagebox.showwarning("Error", "Please fill all the entries")
        except ValueError:
            messagebox.showwarning("Error", "Please enter valid values")
    
    def clearList(self):
        for i in self.sale_list.get_children():
            self.sale_list.delete(i)
    
    def refreshList(self):
        sales = self.db.getTodaySales()
        self.clearList()
        if sales:
            total_sale = 0
            total_return = 0
            for sale in sales:
                product_name = sale[0]
                sold_price = sale[1]
                org_price = sale[2]
                product_quantity = abs(sale[3])
                returnSale = "Sale" if sale[3] > 0 else "Return"

                if returnSale == "Sale":
                    total_sale += sold_price
                else:
                    total_return += sold_price

                self.sale_list.insert("", "end", values=(product_name, sold_price, org_price, product_quantity, returnSale))

            self.refreshSaleLabels(total_sale, total_return)

    def add_sale(self):
        sale_info = self.get_sale_info()
        if not sale_info:
            return
        
        try:
            total_products = self.db.getProductInfo(sale_info[0])[-1]
            sold_products = self.db.countSoldProducts(sale_info[0])
            if total_products - sold_products < sale_info[2]:
                messagebox.showwarning("Error", "Not enough products to sell")
                return
        except (IndexError, TypeError):
            messagebox.showerror("Error", "Product not found")
            return
            
        sale_info.append(self.getDate())
        self.db.addSale(sale_info)
        messagebox.showinfo("Success", "Sale added successfully")
        self.refreshList()
        self.clear()
    
    def return_sale(self):
        sale_info = self.get_sale_info()
        if not sale_info:
            return

        if not self.db.getProductInfo(sale_info[0]):
            messagebox.showerror("Error", "Product not found")
            return
        
        sold_products = self.db.countSoldProducts(sale_info[0])
        if sold_products < sale_info[2]:
            messagebox.showwarning("Error", "Not enough products to return")
            return
            
        sale_info[-1] = -sale_info[-1]
        sale_info.append(self.getDate())
        self.db.addSale(sale_info)
        messagebox.showinfo("Success", "Sale returned successfully")
        self.refreshList()
        self.clear()
    
    def getDate(self):
        return datetime.date.today()
    def clear(self):
        for entry in self.entries:
            entry.delete(0, END)

    def fill_entries(self, event):
        self.clear()
        info = self.sale_list.item(self.sale_list.focus())["values"]
        product_name = info[0]
        sold_price = info[1]
        quantity = info[3]
        info = (product_name, sold_price, quantity)
        for i, entry in enumerate(self.entries):
            entry.insert(0, info[i])

class SalesStat:
    MONTH_NAMES = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    STARTINGDATE = datetime.date(2022, 6, 21)
    def __init__(self, master):
        self.master = master
        self.master.configure(background="white")

        self.db = DataBase()
        
        Label(self.master, text="Sale Stats", font=("Helvetica", 36), bg="white", fg="RED").pack()

        self.product = ttk.Combobox(self.master, font=("Helvetica", 16), state='readonly')
        self.product.place(x=10, y=80, width=190, height=50)
        self.product.set("Select Product")
        self.product["values"] = ["ALL", ] + [name[0] for name in self.db.getProductNames()]

        currentDate = datetime.date.today()
        daysInMonth= calendar.monthrange(currentDate.year, currentDate.month)[1]
        self.day = ttk.Combobox(self.master, text="Day", font=("Helvetica", 16), state='readonly')
        self.day.place(x=210, y=80, width=80, height=50)
        self.day.set("Day")
        self.day["values"] = ["ALL", ] + [i for i in range(1, daysInMonth+1)]
       

        self.month = ttk.Combobox(self.master, font=("Helvetica", 16), state='readonly')
        self.month.place(x=300, y=80, width=100, height=50)
        self.month.set("Month")
        self.month['values'] = ["ALL", ] + self.MONTH_NAMES
        self.month.bind("<<ComboboxSelected>>", self.refresh_days)
        

        self.year = ttk.Combobox(self.master, font=("Helvetica", 16), state='readonly')
        self.year.place(x=410, y=80, width=120, height=50)
        self.year.set("Year")
        self.year['values'] = ["ALL", ] + [i for i in range(self.STARTINGDATE.year, currentDate.year+1)]
        self.year.bind("<<ComboboxSelected>>", self.refresh_days)

        Button(self.master, text="Search", font=("Helvetica", 16), bg="white", fg="black", command=self.search).place(x=540, y=80, width=120, height=50)

        self.stat_list = ttk.Treeview(self.master, columns=("1", "2", "3", "4", "5", "6", "7", "8"), show="headings", )
        self.stat_list.place(x=10, y=150, relwidth=.97, relheight=.5)

        self.stat_list.column("1", width=180)
        self.stat_list.column("2", width=180, anchor=CENTER)
        self.stat_list.column("3", width=180, anchor=CENTER)
        self.stat_list.column("4", width=150, anchor=CENTER)
        self.stat_list.column("5", width=150, anchor=CENTER)
        self.stat_list.column("6", width=150, anchor=CENTER)
        self.stat_list.column("7", width=150, anchor=CENTER)
        self.stat_list.column("8", width=150, anchor=CENTER)
        

        # Changing Font size
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14))

        self.stat_list.heading('1', text='Product Name', anchor="w")
        self.stat_list.heading('2', text='Sold/Return Price')
        self.stat_list.heading('3', text='Original Sale Price')
        self.stat_list.heading('4', text='Cost Price')
        self.stat_list.heading('5', text='Quantity')
        self.stat_list.heading('6', text='Profit')
        self.stat_list.heading('7', text='Sale/Return')
        self.stat_list.heading('8', text='Date')

        # Adding Scroll bar to product list
        yscrollbar = Scrollbar(self.stat_list, orient="vertical", command=self.stat_list.yview)
        xscrollbar = Scrollbar(self.stat_list, orient="horizontal", command=self.stat_list.xview)

        self.stat_list.configure(yscrollcommand=yscrollbar.set)
        self.stat_list.configure(xscrollcommand=xscrollbar.set)

        # Show/Hide Scroll bar
        self.stat_list.bind("<Leave>", lambda event: self.hidescrollbars(xscrollbar, yscrollbar))
        self.stat_list.bind("<Enter>", lambda event: self.showscrollbars(xscrollbar, yscrollbar))

        Label(self.master, text="Total Sale:", font=("Helvetica", 26), bg="white", fg="red").place(x=45, y=560)
        Label(self.master, text="Total Return:", font=("Helvetica", 26), bg="white", fg="red").place(x=10, y=620)
        Label(self.master, text="Profit:", font=("Helvetica", 26), bg="white", fg="red").place(x=118, y=680)

        self.sale_label = Label(self.master, text="Rs.0.0", font=("Helvetica", 22), bg="white", fg="black")
        self.sale_label.place(x=220, y=565)

        self.return_label = Label(self.master, text="Rs.0.0", font=("Helvetica", 22), bg="white", fg="black")
        self.return_label.place(x=220, y=625)

        self.profit_label = Label(self.master, text="Rs.0.0", font=("Helvetica", 22), bg="white", fg="black")
        self.profit_label.place(x=220, y=685)

    
    def refresh_days(self, event):
        if self.year.get() != "ALL" and self.month.get() != "ALL":
            try:
                daysInMonth= calendar.monthrange(int(self.year.get()), self.MONTH_NAMES.index(self.month.get())+1)[1]
                self.day["values"] = ["ALL", ] + [i for i in range(1, daysInMonth+1)]
            except:
                pass

    def showscrollbars(self, xscrollbar, yscrollbar):
        xscrollbar.pack(side="bottom", fill="x")
        yscrollbar.pack(side="right", fill="y")
    
    def hidescrollbars(seld, xscrollbar, yscrollbar):
        xscrollbar.pack_forget()
        yscrollbar.pack_forget()
    
    def search(self):
        product = self.product.get()
        day = self.day.get()
        month = self.month.get()
        year = self.year.get()

        if product != "ALL":
            data = self.db.getProductStat(product)
        else:
            data = self.db.getAllProductStat()
        
        if year != "ALL":
            final_data = []
            for row in data:
                sale_year = row[-1].split("-")[0]
                if sale_year == year:
                    final_data.append(row)
            data = final_data

        if month != "ALL":
            final_data = []
            for row in data:
                sale_month = row[-1].split("-")[1]
                if int(sale_month) == self.MONTH_NAMES.index(month)+1:
                    final_data.append(row)
            data = final_data
        
        if day != "ALL":
            final_data = []
            for row in data:
                sale_day = row[-1].split("-")[2]
                if sale_day == day:
                    final_data.append(row)
            data = final_data
                
        self.stat_list.delete(*self.stat_list.get_children())
        profit_ = 0.0
        sale_ = 0.0
        return_ = 0.0
        for row in data:
            
            
            saleReturn = "Sale" if row[4] > 0 else "Return"

            if saleReturn == "Sale":
                sale_ += row[1]
                profit = row[1]*abs(row[4]) - row[3]*abs(row[4])
                profit_ += profit
            else:
                return_ += row[1]
                profit = 0
                profit_ -= row[1]*abs(row[4]) - row[3]*abs(row[4])

            self.stat_list.insert("", "end", values= list(row[:4]) + [abs(row[4]), profit, saleReturn, row[-1]])
        
        self.refresh_labels(sale_, return_, profit_)

    def refresh_labels(self, sale, return_, profit):
        self.sale_label.config(text="Rs.{}".format(sale))
        self.return_label.config(text="Rs.{}".format(return_))
        self.profit_label.config(text="Rs.{}".format(profit))

class DataBase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("data.db")
        self.c = self.conn.cursor()

        # Create table if not exists
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS PRODUCTS(
                PRODUCTNAME TEXT(60) NOT NULL,
                COSTPRICE FLOAT NOT NULL,
                SELLINGPRICE FLOAT NOT NULL,
                QUANTITY INTEGER NOT NULL,

                PRIMARY KEY (PRODUCTNAME)
                            );
                """)
        
        # Create table if not exists
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS SALES(
                PRODUCTNAME TEXT(60) NOT NULL,
                PRICE FLOAT NOT NULL,
                QUANTITY INTEGER NOT NULL,
                SALEDATE DATE NOT NULL
                                );
                """)

        self.conn.commit()

    def getProductInfo(self, product):
        self.c.execute("""
        SELECT * FROM PRODUCTS WHERE PRODUCTNAME=?;
        """,(product,))
        return self.c.fetchone()

    def insertProduct(self, info):
        self.c.execute("""
        INSERT INTO PRODUCTS
        VALUES (?, ?, ?, ?);
        
        """,info)
        self.conn.commit()

    def deleteProduct(self, productname):
        self.c.execute("""
        DELETE FROM PRODUCTS WHERE PRODUCTNAME=?;
        """,(productname,))
        self.conn.commit()
    
    def updateProduct(self, info):
        self.c.execute("""
        UPDATE PRODUCTS
        SET COSTPRICE=?, SELLINGPRICE=?, QUANTITY=?
        WHERE PRODUCTNAME=?;
        """,info[1:]+[info[0],])
        self.conn.commit()
    
    def readAllProductInfo(self):
        self.c.execute("""
            SELECT * FROM PRODUCTS;
        """)
        
        return self.c.fetchall()
    
    def countSoldProducts(self, productname):

        self.c.execute("""

            SELECT SUM(QUANTITY) FROM SALES WHERE PRODUCTNAME=?;
            
            """,(productname,))
        count = self.c.fetchone()
        if count[0] is None:
            return 0
        return count[0]
    
    def getTodaySales(self):
        date = datetime.date.today()
        self.c.execute("""
            SELECT SALES.PRODUCTNAME, SALES.PRICE, PRODUCTS.SELLINGPRICE,
            SALES.QUANTITY FROM SALES
            INNER JOIN PRODUCTS ON SALES.PRODUCTNAME=PRODUCTS.PRODUCTNAME
            WHERE SALEDATE=?;
        """, (date,))
        return self.c.fetchall()
    
    def addSale(self, info):
        self.c.execute("""
        INSERT INTO SALES
        VALUES (?, ?, ?, ?);
        """, (info))
        self.conn.commit()

    def getProductNames(self):
        self.c.execute("""
            SELECT PRODUCTNAME FROM PRODUCTS;
        """)
        return self.c.fetchall()


    def getAllProductStat(self):
        self.c.execute("""
            SELECT PRODUCTS.PRODUCTNAME, SALES.PRICE, PRODUCTS.SELLINGPRICE,
            PRODUCTS.COSTPRICE, SALES.QUANTITY, SALES.SALEDATE
            FROM PRODUCTS INNER JOIN SALES ON PRODUCTS.PRODUCTNAME=SALES.PRODUCTNAME
        """)
        return self.c.fetchall()

    def getProductStat(self, product):
        self.c.execute("""
            SELECT PRODUCTS.PRODUCTNAME, SALES.PRICE, PRODUCTS.SELLINGPRICE,
            PRODUCTS.COSTPRICE, SALES.QUANTITY, SALES.SALEDATE
            FROM PRODUCTS INNER JOIN SALES ON PRODUCTS.PRODUCTNAME=SALES.PRODUCTNAME
            WHERE PRODUCTS.PRODUCTNAME=?
            """, (product,))
        return self.c.fetchall()

if __name__ == '__main__':
    Main()