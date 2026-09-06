import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

from customer.customer import Customer
from delivery.delivery import Delivery
from menu.menu import MenuItem
from menu.menu import Menu
from order.order import Order
from payment.payment import Payment


#app dito

class ShakeShackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Burger Joint Ordering Kiosk")
        self.root.geometry("900x550")
        
        self.bg_color = "#F4F4F0"      
        self.shack_green = "#007A3B"    
        self.hover_green = "#005C2C"    
        self.text_color = "#111111"     
        
        self.root.configure(bg=self.bg_color)

        self.customer = Customer("C01", "Jane Doe", "jane@email.com", "555-0199", "42 Python Blvd")
        self.menu = Menu()
        self.menu.add_item(MenuItem("M1", "ShackBurger", "Cheeseburger with lettuce, tomato, ShackSauce", 6.89))
        self.menu.add_item(MenuItem("M2", "SmokeShack", "Cheeseburger with cherry pepper, bacon, ShackSauce", 8.39))
        self.menu.add_item(MenuItem("M3", "Crinkle Cut Fries", "Crispy crinkle cut potatoes", 3.19))
        self.menu.add_item(MenuItem("M4", "Shack-made Lemonade", "Signature fresh lemonade", 2.99))
        
        self.current_order = Order("ORD-1001", self.customer)
        self.order_counter = 1001
        
        self.create_widgets()

    def create_hover_button(self, parent, text, command):
        """Creates a custom button with a color-changing hover effect."""
        btn = tk.Button(
            parent, text=text, command=command,
            bg=self.shack_green, fg="white", 
            activebackground=self.hover_green, activeforeground="white",
            font=("Helvetica", 12, "bold"), relief="flat", cursor="hand2",
            padx=15, pady=8, bd=0
        )

        btn.bind("<Enter>", lambda e: btn.configure(bg=self.hover_green))
        btn.bind("<Leave>", lambda e: btn.configure(bg=self.shack_green))
        
        return btn

    def create_widgets(self):
        header_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        header_lbl = tk.Label(self.root, text="🍔 BURGER JOINT KIOSK", font=header_font, bg=self.bg_color, fg=self.text_color)
        header_lbl.pack(pady=(20, 10))

        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        menu_frame = tk.LabelFrame(main_frame, text=" OUR MENU ", font=("Helvetica", 12, "bold"), bg=self.bg_color, fg=self.text_color, bd=2)
        menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.menu_listbox = tk.Listbox(
            menu_frame, font=("Helvetica", 12), selectmode=tk.SINGLE, 
            bg="white", fg=self.text_color, selectbackground=self.shack_green,
            activestyle="none", bd=0, highlightthickness=1, highlightcolor="#DDDDDD"
        )
        self.menu_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        for item in self.menu.get_available_items():
            self.menu_listbox.insert(tk.END, f" {item.name} - ${item.price:.2f}")

        add_btn = self.create_hover_button(menu_frame, "Add to Order ➔", self.add_to_order)
        add_btn.pack(pady=(0, 15))

        order_frame = tk.LabelFrame(main_frame, text=" YOUR TRAY ", font=("Helvetica", 12, "bold"), bg=self.bg_color, fg=self.text_color, bd=2)
        order_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.receipt_text = tk.Text(
            order_frame, height=15, width=40, font=("Courier", 11), 
            state=tk.DISABLED, bg="#FFF9E6", fg=self.text_color, # Subtle yellow tint for receipt paper
            bd=0, highlightthickness=1, highlightcolor="#DDDDDD", padx=10, pady=10
        )
        self.receipt_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)


        checkout_btn = self.create_hover_button(order_frame, "💳 Pay & Checkout", self.checkout)
        checkout_btn.pack(pady=(0, 15))
        
        self.update_receipt()

    def add_to_order(self):
        selection = self.menu_listbox.curselection()
        if not selection:
            messagebox.showwarning("Hold up!", "Please select a delicious item from the menu first.")
            return
        
        selected_index = selection[0]
        available_items = self.menu.get_available_items()
        selected_item = available_items[selected_index]
        
        self.current_order.add_item(selected_item, 1) #[cite: 2]
        self.update_receipt()

    def update_receipt(self):
        self.receipt_text.config(state=tk.NORMAL)
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(tk.END, self.current_order.generate_receipt()) #[cite: 2]
        self.receipt_text.config(state=tk.DISABLED)

    def checkout(self):
        if not self.current_order.items:
            messagebox.showwarning("Empty Tray", "Your tray is empty! Add some food before checking out.")
            return
            

        payment = Payment(f"TXN-{self.order_counter}", self.current_order, self.current_order.total_amount, "Credit Card")
        success = payment.process_payment()
        
        if success:

            delivery = Delivery(f"DEL-{self.order_counter}", self.current_order)
            delivery.assign_driver("Shack Express Courier")
            

            summary = (f"🍔 Payment Successful! 🍔\n\n"
                       f"{payment.get_transaction_details()}\n\n"
                       f"Delivery Status:\n"
                       f"Driver: {delivery.driver_name}\n"
                       f"Status: {delivery.delivery_status}")
            
            messagebox.showinfo("Order Complete", summary)
            

            self.order_counter += 1
            self.current_order = Order(f"ORD-{self.order_counter}", self.customer)
            self.update_receipt()
        else:
            messagebox.showerror("Payment Failed", "Whoops! The transaction could not be completed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShakeShackGUI(root)
    root.mainloop()
