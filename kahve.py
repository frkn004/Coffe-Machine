import customtkinter as ctk
import threading
import time
from PIL import Image, ImageTk
import json
from datetime import datetime

class ModernCoffeeMachine:
    def __init__(self):
        # Main window setup
        self.app = ctk.CTk()
        self.app.title("Modern Coffee Machine")
        self.app.geometry("1200x800")

        # Theme settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Basic variables
        self.water_level = 2000  # ml
        self.coffee_beans = 1000  # g
        self.milk_level = 2000   # ml
        self.caramel_syrup = 1000  # ml
        self.vanilla_syrup = 1000  # ml
        self.chocolate_sauce = 1000  # ml
        self.whipped_cream = 1000  # ml
        self.money = 0.0
        self.is_brewing = False
        self.temperature = 90
        self.total_sales = 0
        self.drinks_sold = {}
        self.recent_orders = []
        self.max_recent_orders = 5

        # Daily specials
        self.daily_specials = {
            "Monday": {"drink": "Caramel Latte", "discount": 20},
            "Tuesday": {"drink": "Mocha", "discount": 15},
            "Wednesday": {"drink": "Cappuccino", "discount": 20},
            "Thursday": {"drink": "Vanilla Latte", "discount": 15},
            "Friday": {"drink": "Espresso", "discount": 25},
            "Saturday": {"drink": "Americano", "discount": 20},
            "Sunday": {"drink": "All Drinks", "discount": 10}
        }

        # Coffee menu with prices and ingredients
        self.coffee_menu = {
            "Espresso": {
                "price": 15,
                "water": 30,
                "coffee": 18,
                "milk": 0,
                "description": "Strong coffee brewed by forcing hot water through finely-ground coffee beans"
            },
            "Americano": {
                "price": 20,
                "water": 170,
                "coffee": 18,
                "milk": 0,
                "description": "Espresso diluted with hot water"
            },
            "Cappuccino": {
                "price": 25,
                "water": 30,
                "coffee": 18,
                "milk": 120,
                "description": "Equal parts espresso, steamed milk, and milk foam"
            },
            "Latte": {
                "price": 25,
                "water": 30,
                "coffee": 18,
                "milk": 150,
                "description": "Espresso with steamed milk and a small layer of milk foam"
            },
            "Mocha": {
                "price": 30,
                "water": 30,
                "coffee": 18,
                "milk": 150,
                "description": "Espresso with chocolate, steamed milk and milk foam"
            }
        }

        # Size options with price multipliers
        self.size_options = {
            "Small": 0.8,
            "Medium": 1.0,
            "Large": 1.2
        }

        # Extra options with prices
        self.extras = {
            "Extra Shot": {"price": 5, "coffee": 18},
            "Caramel Syrup": {"price": 3, "syrup": 30},
            "Vanilla Syrup": {"price": 3, "syrup": 30},
            "Chocolate Sauce": {"price": 3, "sauce": 30},
            "Whipped Cream": {"price": 2, "cream": 30}
        }

        # Coffee tips and facts
        self.coffee_tips = [
            "☕ Fresh coffee beans produce the best flavor",
            "🌡️ Ideal water temperature is 90-96°C",
            "⏰ Espresso should take 20-30 seconds to brew",
            "🥛 Steam milk between 60-70°C for best results",
            "✨ Clean your coffee machine regularly",
            "💡 Store beans in an airtight container",
            "🌿 Arabica beans are known for their smooth taste",
            "📝 Try different roast levels to find your preference"
        ]

        self.setup_gui()
        self.start_clock_update()
        self.start_tip_rotation()
        
    def setup_gui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.app)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left panel - Controls
        self.left_panel = ctk.CTkFrame(self.main_frame, width=400)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=10)

        # Right panel
        self.right_panel = ctk.CTkFrame(self.main_frame, width=400)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10)

        # Create all sections
        self.create_status_section()
        self.create_payment_section()
        self.create_coffee_selection()
        self.create_size_selection()
        self.create_extras_selection()
        self.create_temperature_control()
        self.create_brew_button()
        self.create_right_panel_content()

    def create_status_section(self):
        status_frame = ctk.CTkFrame(self.left_panel)
        status_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(status_frame, text="MACHINE STATUS", 
                    font=("Arial", 16, "bold")).pack(pady=5)

        # Resource levels with progress bars
        resources_frame = ctk.CTkFrame(status_frame)
        resources_frame.pack(fill="x", pady=5)

        # Water level
        water_frame = ctk.CTkFrame(resources_frame)
        water_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(water_frame, text="Water Level:").pack(side="left", padx=5)
        self.water_progress = ctk.CTkProgressBar(water_frame)
        self.water_progress.pack(side="left", fill="x", expand=True, padx=5)
        self.water_progress.set(self.water_level/2000)
        ctk.CTkButton(water_frame, text="Refill", 
                     command=lambda: self.refill_resource("Water"),
                     width=60).pack(side="right", padx=5)

        # Coffee beans level
        coffee_frame = ctk.CTkFrame(resources_frame)
        coffee_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(coffee_frame, text="Coffee Beans:").pack(side="left", padx=5)
        self.coffee_progress = ctk.CTkProgressBar(coffee_frame)
        self.coffee_progress.pack(side="left", fill="x", expand=True, padx=5)
        self.coffee_progress.set(self.coffee_beans/1000)
        ctk.CTkButton(coffee_frame, text="Refill", 
                     command=lambda: self.refill_resource("Coffee"),
                     width=60).pack(side="right", padx=5)

        # Milk level
        milk_frame = ctk.CTkFrame(resources_frame)
        milk_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(milk_frame, text="Milk Level:").pack(side="left", padx=5)
        self.milk_progress = ctk.CTkProgressBar(milk_frame)
        self.milk_progress.pack(side="left", fill="x", expand=True, padx=5)
        self.milk_progress.set(self.milk_level/2000)
        ctk.CTkButton(milk_frame, text="Refill", 
                     command=lambda: self.refill_resource("Milk"),
                     width=60).pack(side="right", padx=5)

        # Extra ingredients progress bars
        self.resource_bars = {}
        extras_frame = ctk.CTkFrame(resources_frame)
        extras_frame.pack(fill="x", pady=2)

        for extra in ["Caramel Syrup", "Vanilla Syrup", "Chocolate Sauce", "Whipped Cream"]:
            extra_frame = ctk.CTkFrame(extras_frame)
            extra_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(extra_frame, text=f"{extra}:").pack(side="left", padx=5)
            progress = ctk.CTkProgressBar(extra_frame)
            progress.pack(side="left", fill="x", expand=True, padx=5)
            progress.set(1.0)  # Full at start
            self.resource_bars[extra] = progress
            ctk.CTkButton(extra_frame, text="Refill", 
                         command=lambda e=extra: self.refill_resource(e),
                         width=60).pack(side="right", padx=5)

        # Money display
        self.money_label = ctk.CTkLabel(status_frame, 
                                      text=f"Balance: ${self.money:.2f}",
                                      font=("Arial", 14, "bold"))
        self.money_label.pack(pady=10)

    def create_payment_section(self):
        money_frame = ctk.CTkFrame(self.left_panel)
        money_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(money_frame, text="ADD MONEY", 
                    font=("Arial", 16, "bold")).pack(pady=5)

        money_buttons = ctk.CTkFrame(money_frame)
        money_buttons.pack(pady=5)

        for amount in [1, 5, 10, 20]:
            ctk.CTkButton(money_buttons, text=f"${amount}",
                         command=lambda x=amount: self.add_money(x),
                         width=60).pack(side="left", padx=5)

    def create_coffee_selection(self):
        coffee_frame = ctk.CTkFrame(self.left_panel)
        coffee_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(coffee_frame, text="SELECT COFFEE", 
                    font=("Arial", 16, "bold")).pack(pady=5)

        self.coffee_var = ctk.StringVar(value="")
        for coffee, details in self.coffee_menu.items():
            coffee_button_frame = ctk.CTkFrame(coffee_frame)
            coffee_button_frame.pack(fill="x", pady=2)
            
            ctk.CTkRadioButton(coffee_button_frame,
                             text=f"{coffee} (${details['price']:.2f})",
                             variable=self.coffee_var,
                             value=coffee).pack(side="left", padx=5)
            
            ingredients = f"🚰 {details['water']}ml | ☕ {details['coffee']}g"
            if details['milk'] > 0:
                ingredients += f" | 🥛 {details['milk']}ml"
            
            ctk.CTkLabel(coffee_button_frame,
                        text=ingredients,
                        font=("Arial", 10)).pack(side="right", padx=5)
    def create_size_selection(self):
        size_frame = ctk.CTkFrame(self.left_panel)
        size_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(size_frame, text="SELECT SIZE", 
                    font=("Arial", 16, "bold")).pack()
        
        self.size_var = ctk.StringVar(value="Medium")
        for size, multiplier in self.size_options.items():
            ctk.CTkRadioButton(size_frame, 
                             text=f"{size} (x{multiplier})",
                             variable=self.size_var,
                             value=size).pack(pady=2)

    def create_extras_selection(self):
        extras_frame = ctk.CTkFrame(self.left_panel)
        extras_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(extras_frame, text="EXTRAS", 
                    font=("Arial", 16, "bold")).pack()
        
        self.extra_vars = {}
        for extra, details in self.extras.items():
            var = ctk.BooleanVar()
            self.extra_vars[extra] = var
            ctk.CTkCheckBox(extras_frame, 
                          text=f"{extra} (+${details['price']:.2f})",
                          variable=var).pack(pady=2)

    def create_temperature_control(self):
        temp_frame = ctk.CTkFrame(self.left_panel)
        temp_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(temp_frame, text="TEMPERATURE", 
                    font=("Arial", 16, "bold")).pack()
        
        self.temp_slider = ctk.CTkSlider(temp_frame, 
                                        from_=65, 
                                        to=95, 
                                        number_of_steps=30,
                                        command=self.update_temperature)
        self.temp_slider.set(self.temperature)
        self.temp_slider.pack(pady=5)
        
        self.temp_label = ctk.CTkLabel(temp_frame, text=f"{self.temperature}°C")
        self.temp_label.pack()

    def create_brew_button(self):
        self.brew_button = ctk.CTkButton(self.left_panel,
                                       text="BREW COFFEE ☕",
                                       command=self.start_brewing,
                                       height=40,
                                       font=("Arial", 16, "bold"))
        self.brew_button.pack(pady=20)

    def create_right_panel_content(self):
        # Digital Clock
        clock_frame = ctk.CTkFrame(self.right_panel)
        clock_frame.pack(fill="x", pady=10, padx=10)
        self.clock_label = ctk.CTkLabel(clock_frame, 
                                    text="00:00:00",
                                    font=("Arial", 24, "bold"))
        self.clock_label.pack(pady=5)

        # Machine Status
        self.status_label = ctk.CTkLabel(self.right_panel,
                                    text="Coffee Machine Ready ☕",
                                    font=("Arial", 20, "bold"))
        self.status_label.pack(pady=10)

        # Daily Special
        special_frame = ctk.CTkFrame(self.right_panel)
        special_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(special_frame, 
                    text="TODAY'S SPECIAL ⭐",
                    font=("Arial", 16, "bold")).pack(pady=5)
        self.update_daily_special()

        # Order Form
        order_frame = ctk.CTkFrame(self.right_panel)
        order_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(order_frame, text="PLACE ORDER 📝", 
                    font=("Arial", 16, "bold")).pack(pady=5)

        # Customer Name
        name_frame = ctk.CTkFrame(order_frame)
        name_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(name_frame, text="Name:").pack(side="left", padx=5)
        self.customer_name = ctk.CTkEntry(name_frame)
        self.customer_name.pack(side="left", fill="x", expand=True, padx=5)

        # Table Number
        table_frame = ctk.CTkFrame(order_frame)
        table_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(table_frame, text="Table #:").pack(side="left", padx=5)
        self.table_number = ctk.CTkEntry(table_frame)
        self.table_number.pack(side="left", fill="x", expand=True, padx=5)

        # Notes
        notes_frame = ctk.CTkFrame(order_frame)
        notes_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(notes_frame, text="Special Notes:").pack(anchor="w", padx=5)
        self.order_notes = ctk.CTkTextbox(notes_frame, height=60)
        self.order_notes.pack(fill="x", padx=5, pady=5)

        # Place Order Button
        ctk.CTkButton(order_frame, 
                    text="Place Order",
                    command=self.place_order,
                    height=30,
                    font=("Arial", 14, "bold")).pack(pady=10)

        # Coffee Tip of the Day
        tip_frame = ctk.CTkFrame(self.right_panel)
        tip_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(tip_frame, 
                    text="COFFEE TIP 💡",
                    font=("Arial", 16, "bold")).pack(pady=5)
        self.tip_label = ctk.CTkLabel(tip_frame, 
                                    text="",
                                    wraplength=350)
        self.tip_label.pack(pady=5)

        # Recent Orders
        orders_frame = ctk.CTkFrame(self.right_panel)
        orders_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(orders_frame, 
                    text="RECENT ORDERS 📋",
                    font=("Arial", 16, "bold")).pack(pady=5)
        self.orders_display = ctk.CTkTextbox(orders_frame, height=200)
        self.orders_display.pack(fill="x", pady=5)
        
    def place_order(self):
        if not self.coffee_var.get():
            self.show_warning("⚠️ Please select a coffee!")
            return
        
        if not self.customer_name.get():
            self.show_warning("⚠️ Please enter customer name!")
            return
        
        if not self.table_number.get():
            self.show_warning("⚠️ Please enter table number!")
            return
        
        # Start brewing process
        self.start_brewing()
        
        # Clear form after successful order
        self.customer_name.delete(0, 'end')
        self.table_number.delete(0, 'end')
        self.order_notes.delete('1.0', 'end')
        
    def add_to_recent_orders(self, coffee_type, size, extras):
        # Get current time
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Get customer details
        customer = self.customer_name.get()
        table = self.table_number.get()
        notes = self.order_notes.get("1.0", "end-1c")
        
        # Create order details string
        order_details = f"Time: {current_time}\n"
        order_details += f"Customer: {customer}\n"
        order_details += f"Table: {table}\n"
        order_details += f"Coffee: {coffee_type}\n"
        order_details += f"Size: {size}\n"
        
        # Add selected extras
        selected_extras = [extra for extra, var in extras.items() if var.get()]
        if selected_extras:
            order_details += f"Extras: {', '.join(selected_extras)}\n"
        
        # Add notes if any
        if notes.strip():
            order_details += f"Notes: {notes}\n"
        
        order_details += "-" * 30 + "\n"
        
        # Add to recent orders list
        self.recent_orders.append(order_details)
        
        # Keep only the last 5 orders
        if len(self.recent_orders) > self.max_recent_orders:
            self.recent_orders.pop(0)
        
        # Update orders display
        self.orders_display.delete("1.0", "end")
        for order in reversed(self.recent_orders):
            self.orders_display.insert("1.0", order)
            
    def check_resources(self, coffee_type, size_multiplier):
        insufficient = []
        coffee_details = self.coffee_menu[coffee_type]
        
        # Check basic resources
        if self.water_level < coffee_details['water'] * size_multiplier:
            insufficient.append('water')
        if self.coffee_beans < coffee_details['coffee'] * size_multiplier:
            insufficient.append('coffee beans')
        if coffee_details['milk'] > 0 and self.milk_level < coffee_details['milk'] * size_multiplier:
            insufficient.append('milk')
        
        # Check extras
        for extra, var in self.extra_vars.items():
            if var.get():
                if extra == "Extra Shot" and self.coffee_beans < self.extras[extra]["coffee"]:
                    insufficient.append('coffee beans')
                elif "syrup" in self.extras[extra]:
                    syrup_name = extra.lower().replace(" ", "_")
                    if getattr(self, syrup_name) < self.extras[extra]["syrup"]:
                        insufficient.append(extra)
        
        return insufficient

    def update_resources(self, coffee_type):
        size_multiplier = self.size_options[self.size_var.get()]
        coffee_details = self.coffee_menu[coffee_type]
        
        # Update basic resources
        self.water_level -= coffee_details['water'] * size_multiplier
        self.coffee_beans -= coffee_details['coffee'] * size_multiplier
        if coffee_details['milk'] > 0:
            self.milk_level -= coffee_details['milk'] * size_multiplier
        
        # Update progress bars
        self.water_progress.set(self.water_level/2000)
        self.coffee_progress.set(self.coffee_beans/1000)
        self.milk_progress.set(self.milk_level/2000)
        
        # Update extras
        for extra, var in self.extra_vars.items():
            if var.get():
                if extra == "Extra Shot":
                    self.coffee_beans -= self.extras[extra]["coffee"]
                    self.coffee_progress.set(self.coffee_beans/1000)
                elif "syrup" in self.extras[extra]:
                    syrup_name = extra.lower().replace(" ", "_")
                    current_amount = getattr(self, syrup_name)
                    setattr(self, syrup_name, current_amount - self.extras[extra]["syrup"])
                    self.resource_bars[extra].set(getattr(self, syrup_name)/1000)

    def refill_resource(self, resource):
        if resource == "Water":
            self.water_level = 2000
            self.water_progress.set(1.0)
        elif resource == "Coffee":
            self.coffee_beans = 1000
            self.coffee_progress.set(1.0)
        elif resource == "Milk":
            self.milk_level = 2000
            self.milk_progress.set(1.0)
        else:
            # Handle extra ingredients
            resource_var = resource.lower().replace(" ", "_")
            setattr(self, resource_var, 1000)
            self.resource_bars[resource].set(1.0)
    def start_clock_update(self):
        def update_clock():
            while True:
                current_time = datetime.now().strftime("%H:%M:%S")
                self.clock_label.configure(text=current_time)
                time.sleep(1)
        
        clock_thread = threading.Thread(target=update_clock, daemon=True)
        clock_thread.start()

    def start_tip_rotation(self):
        def rotate_tips():
            tip_index = 0
            while True:
                self.tip_label.configure(text=self.coffee_tips[tip_index])
                tip_index = (tip_index + 1) % len(self.coffee_tips)
                time.sleep(10)
        
        tip_thread = threading.Thread(target=rotate_tips, daemon=True)
        tip_thread.start()

    def update_daily_special(self):
        day = datetime.now().strftime("%A")
        special = self.daily_specials[day]
        special_text = f"{special['drink']}\n{special['discount']}% OFF TODAY!"
        
        special_label = ctk.CTkLabel(self.right_panel,
                                   text=special_text,
                                   font=("Arial", 14))
        special_label.pack(pady=5)

    def update_temperature(self, value):
        self.temperature = int(value)
        self.temp_label.configure(text=f"{self.temperature}°C")

    def add_money(self, amount):
        self.money += amount
        self.money_label.configure(text=f"Balance: ${self.money:.2f}")

    def start_brewing(self):
        if self.is_brewing:
            self.show_warning("⚠️ Coffee is being prepared, please wait!")
            return

        selected_coffee = self.coffee_var.get()
        if not selected_coffee:
            self.show_warning("⚠️ Please select a coffee!")
            return

        total_price = self.calculate_price()
        
        # Apply daily special discount
        day = datetime.now().strftime("%A")
        special = self.daily_specials[day]
        if selected_coffee == special["drink"] or special["drink"] == "All Drinks":
            discount = special["discount"] / 100
            total_price = total_price * (1 - discount)

        if self.money < total_price:
            self.show_warning("⚠️ Insufficient balance!")
            return

        # Resource check
        insufficient = self.check_resources(selected_coffee, 
                                         self.size_options[self.size_var.get()])
        if insufficient:
            self.show_warning(f"⚠️ Insufficient {', '.join(insufficient)}!")
            return

        # Start brewing process
        self.is_brewing = True
        self.money -= total_price
        self.total_sales += total_price
        self.drinks_sold[selected_coffee] = self.drinks_sold.get(selected_coffee, 0) + 1
        
        # Update displays
        self.money_label.configure(text=f"Balance: ${self.money:.2f}")
        self.update_resources(selected_coffee)
        
        # Add to recent orders
        self.add_to_recent_orders(
            coffee_type=selected_coffee,
            size=self.size_var.get(),
            extras=self.extra_vars
        )
        
        # Start brewing thread
        brewing_thread = threading.Thread(target=lambda: self.brew_coffee(selected_coffee))
        brewing_thread.start()

    def brew_coffee(self, coffee_type):
        steps = [
            ("☕ Starting to prepare your coffee...", 1),
            ("⚙️ Grinding coffee beans...", 2),
            (f"🌡️ Heating water to {self.temperature}°C...", 2),
            ("⏳ Preparing espresso...", 2),
            ("🥛 Heating milk..." if self.coffee_menu[coffee_type]["milk"] > 0 else None, 2),
            ("🌪️ Frothing milk..." if self.coffee_menu[coffee_type]["milk"] > 0 else None, 2),
            (f"👨‍🍳 Preparing {coffee_type}...", 2),
            ("🍯 Adding extras..." if any(var.get() for var in self.extra_vars.values()) else None, 1),
            ("✨ Your coffee is ready! Enjoy!", 2)
        ]

        steps = [(step, duration) for step, duration in steps if step is not None]

        for step, duration in steps:
            self.status_label.configure(text=step)
            time.sleep(duration)

        self.is_brewing = False
        self.status_label.configure(text="Coffee Machine Ready ☕")

    def show_warning(self, message):
        warning_window = ctk.CTkToplevel(self.app)
        warning_window.title("Warning")
        warning_window.geometry("300x150")

        ctk.CTkLabel(warning_window, text=message, wraplength=250).pack(pady=20)
        ctk.CTkButton(warning_window, text="OK",
                     command=warning_window.destroy).pack(pady=10)

    def calculate_price(self):
        if not self.coffee_var.get():
            return 0
        
        base_price = self.coffee_menu[self.coffee_var.get()]["price"]
        size_multiplier = self.size_options[self.size_var.get()]
        extras_price = sum(self.extras[extra]["price"] 
                         for extra, var in self.extra_vars.items() if var.get())
        
        return (base_price * size_multiplier) + extras_price

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    coffee_machine = ModernCoffeeMachine()
    coffee_machine.run()