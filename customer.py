# ============================================================
# CABZ LAUNDRY SYSTEM - CUSTOMER
# ============================================================

import data

from orders import create_order
from utils import (
    pause, banner, section, field, menu_item, ask,
    success, error, info, badge
)


# ============================================================
# CUSTOMER - CHECK PICKUP STATUS
# ============================================================

def check_order_status():

    banner("CHECK PICKUP STATUS", "Type your order number to see if your laundry is ready")
    print()

    order_number = ask("Enter Order Number: ").strip().upper()

    for order in data.orders:

        if order["order_number"] == order_number:

            section("ORDER FOUND!")
            field("Customer Name", order["customer_name"])
            field("Order Number", order["order_number"])
            field("Service", order["service"])
            field("Weight", f"{order['weight']} kg")

            if order["status"] == "READY TO PICK UP":
                field("Pickup Status", badge("READY TO PICK UP"))
                print()
                success("Your laundry is ready for pickup!")
                if order.get("ready_date"):
                    field("Ready Since", f"{order['ready_date']} {order['ready_time']}")
            else:
                field("Pickup Status", badge("NOT READY YET"))
                print()
                info("Your laundry is not ready for pickup yet.")

            pause()
            return

    print()
    error("Order not found.")
    info("Please check your Order Number.")
    pause()


# ============================================================
# CUSTOMER MENU
# ============================================================

def customer_menu():

    while True:
        banner("CUSTOMER MENU", "What would you like to do?")
        print()

        menu_item("1", "Create Laundry Order")
        menu_item("2", "Check Pickup Status")
        menu_item("3", "Exit")
        print()

        choice = ask("Enter choice (1-3): ").strip()

        if choice == "1":
            create_order()

        elif choice == "2":
            check_order_status()

        elif choice == "3":
            return

        else:
            error("Invalid choice.")
