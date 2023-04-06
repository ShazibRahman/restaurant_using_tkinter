from tkinter import ttk, BooleanVar
from ttkthemes import ThemedTk, ThemedStyle
from functools import partial
import sqlite3
try:
    import kitchen.kitchen_main as km
except:
    import kitchen_main as km


class MainGUI:
    def __init__(self):
        self.view_bool = False
        self.get_data(False)
        self.main_init()

    def main_init(self):
        self.gui_main()

    def main_refresh(self, all=False):
        self.get_data(all)
        if self.order_details == {}:
            self.listbox.delete(*self.listbox.get_children())
            self.listbox.insert("", "end", text="--",
                                values=("All orders cleared!", ))
        else:
            simple_details = []
            for id in self.order_ids:
                string = ""
                for item in self.order_details.get(id):
                    string += f"{item[1]} {item[0]}, "
                simple_details.append(
                    [id, string[:40]+"..." if len(string) > 40 else string[:len(string)-2]])

            self.listbox.delete(*self.listbox.get_children())
            for simple_detail in simple_details:
                self.listbox.insert(
                    "", "end", text=simple_detail[0], values=(simple_detail[1], ))

    def gui_main(self):
        # Root Window Init
        self.window = ThemedTk(theme="radiance")
        self.window.geometry("435x340")
        self.window.title("Restaurant Management System")
        self.window.configure(background="#F6F4F2")
        self.window.resizable(0, 0)

        self.view_var = BooleanVar()

        # Heading
        ttk.Label(self.window, font=("default", 19, "bold"), text="Kitchen Manager").grid(
            row=0, column=0, sticky="w", padx=15)
        ttk.Separator(self.window, orient="horizontal").grid(
            row=1, columnspan=2, sticky="ew")

        # Tree View
        self.listbox = ttk.Treeview(self.window)
        self.listbox["columns"] = ("Details")
        self.listbox.heading("#0", text="Order No")
        self.listbox.heading("#1", text="Details")
        self.listbox.column("#0", minwidth=0, width=100)
        self.listbox.column("#1", minwidth=0, width=300)
        self.listbox.bind('<Double-1>', self.selectItem)
        ttk.Style().configure("Treeview", fieldbackground="#FEFEFE", background="#FEFEFE")

        self.main_refresh(self.view_bool)
        self.listbox.grid(row=2, column=0, sticky="nse", padx=15, pady=10)

        self.view_all = ttk.Checkbutton(self.window, text="View all orders", variable=self.view_var, command=self.cb).grid(
            row=3, column=0, sticky="w", padx=15)
        ttk.Button(self.window, text="Quit", command=self.window.destroy).grid(
            row=3, column=0, sticky="e", padx=15)
        self.window.mainloop()

    def cb(self):
        if self.view_var.get() == True:
            self.view_bool = True
        else:
            self.view_bool = False
        self.main_refresh(self.view_bool)

    def gui_details(self, id):
        # Open Details Window
        self.detail = ThemedTk(theme="radiance")
        self.detail.geometry("335x410")
        self.detail.title("Details")
        self.detail.configure(background="#F6F4F2")
        self.detail.resizable(0, 0)
        self.id = id

        # Heading
        ttk.Label(self.detail, font=("default", 19, "bold"), text="Orders").grid(
            row=0, column=0, sticky="w", padx=15)
        ttk.Separator(self.detail, orient="horizontal").grid(
            row=1, columnspan=2, sticky="ew", pady=(0, 5))

        # Create Default Lables
        ttk.Label(self.detail, font=("default", 10, "bold"), anchor="e",
                  width=18, text="Order ID             : ").grid(row=2, column=0)
        ttk.Label(self.detail, font=("default", 10, "bold"), anchor="e",
                  width=18, text="Customer Name : ").grid(row=3, column=0)

        # Create Buttons
        ttk.Button(self.detail, text="Mark Done", command=lambda: self.mark_done(
            self.id), width=33).grid(row=5, column=0, columnspan=2)
        ttk.Button(self.detail, text="Previous", command=lambda: self.refresh(
            self.detail, "prev", self.id)).grid(row=6, column=0, sticky="w", padx=15)
        ttk.Button(self.detail, text="Next", command=lambda: self.refresh(
            self.detail, "next", self.id)).grid(row=6, column=1, sticky="e", padx=15)

        self.tree = ttk.Treeview(self.detail)
        self.tree["columns"] = ("Quantity")
        self.tree.heading("#0", text="Name")
        self.tree.heading("#1", text="Quantity")
        self.tree.column("#0", minwidth=0, width=230)
        self.tree.column("#1", minwidth=0, width=70)

    def mark_done(self, id):
        conn = sqlite3.connect("login_db.db")
        query = f"UPDATE orders SET delivered=1 WHERE order_no={id};"
        conn.execute(query)
        conn.commit()
        self.detail.destroy()
        self.main_refresh(self.view_bool)

    def selectItem(self, a):
        curItem = self.listbox.focus()
        id = self.listbox.item(curItem).get("text")
        if id == "--":
            pass
        else:
            self.gui_details(id)
            self.refresh(self.detail, None, id)

    def refresh(self, detail, fun, id):
        # Determine Function of Refresh else do nothing
        orders = self.order_ids
        if fun == "next":
            # When at end, loop back to start
            if orders.index(id)+1 == len(orders):
                id = orders[0]
            else:
                id = orders[orders.index(id)+1]

        elif fun == "prev":
            id = orders[orders.index(id)-1]
        self.id = id

        # Create Changing Value Lables
        conn = sqlite3.connect("login_db.db")
        query = f"SELECT * FROM orders WHERE order_no={id}"
        items = conn.execute(query)
        converted_item = tuple(items)[0]
        ttk.Label(self.detail, anchor="w", width=18,
                  text=f"{converted_item[0]}").grid(row=2, column=1, padx=3)
        ttk.Label(self.detail, anchor="w", width=18,
                  text=f"{converted_item[1]}").grid(row=3, column=1, padx=3)

        self.tree.delete(*self.tree.get_children())
        for item in self.order_details.get(id):
            self.tree.insert("", "end", text=item[0], values=(item[1], ))

        for i in range(10):
            self.tree.insert("", "end", text="", values=("", ))

        self.tree.grid(row=4, column=0, columnspan=2, padx=15, pady=10)
        self.detail.mainloop()

    def get_data(self, all):
        self.order_details = km.db_retrieve(all)
        self.order_ids = km.order_ids(all)


def main():
    MainGUI()


if __name__ == "__main__":
    main()
