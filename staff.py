# ============================================================
# CABZ LAUNDRY SYSTEM - ADMIN
# ============================================================

import data

from config import STAFF_USERNAME, SECURITY_ANSWER
from orders import mark_order_ready
from receipt import print_laundry_info, print_price_breakdown
from utils import (
    pause, banner, section, field, menu_item, ask,
    success, error, warn, info, hint, box, table, badge
)


# ============================================================
# ADMIN LOGIN
# ============================================================

def staff_login():

    attempts = 3

    while attempts > 0:
        banner("ADMIN LOGIN", "Authorized personnel only")
        print()

        username = ask("Username: ").strip()
        password = ask("Password: ")

        if username == STAFF_USERNAME and password == data.staff_password:
            print()
            success("Login successful!")
            info("Welcome, Admin!")
            staff_menu()
            return

        attempts -= 1
        print()
        error("Invalid username or password.")
        warn(f"Attempts remaining: {attempts}")

    print()
    error("Too many incorrect attempts.")
    error("Admin access denied.")
    pause()


# ============================================================
# FORGOT USERNAME / PASSWORD
# ============================================================

def account_recovery():

    banner("ACCOUNT RECOVERY", "Verify your identity first")
    print()

    menu_item("1", "Recover Username")
    menu_item("2", "Reset Password")
    menu_item("3", "Back")
    print()

    choice = ask("Enter choice (1-3): ").strip()

    if choice == "3":
        return

    if choice not in ("1", "2"):
        error("Invalid choice.")
        pause()
        return

    section("SECURITY QUESTION")
    print("  What is the name of the laundry shop?")
    print()

    answer = ask("Answer: ")

    if answer.strip().lower() != SECURITY_ANSWER.lower():
        print()
        error("Incorrect security answer.")
        error("Account recovery failed.")
        pause()
        return

    print()
    success("Identity verified.")

    if choice == "1":
        field("Your admin username is", STAFF_USERNAME)

    elif choice == "2":
        new_password = ask("Enter New Password: ")
        confirm_password = ask("Confirm New Password: ")

        if new_password == confirm_password and new_password != "":
            data.staff_password = new_password
            print()
            success("Password successfully changed!")
        else:
            print()
            error("Passwords do not match or password is empty.")

    pause()


# ============================================================
# ADMIN ACCESS
# ============================================================

def staff_access():

    while True:
        banner("ADMIN ACCESS", "Login or recover your account")
        print()

        menu_item("1", "Login")
        menu_item("2", "Forgot Username / Password")
        menu_item("3", "Back")
        print()

        choice = ask("Enter choice (1-3): ").strip()

        if choice == "1":
            staff_login()
            return

        elif choice == "2":
            account_recovery()

        elif choice == "3":
            return

        else:
            error("Invalid choice.")


# ============================================================
# ADMIN - VIEW ALL ORDERS
# ============================================================

def view_all_orders():

    banner("ALL LAUNDRY ORDERS", "Complete list of recorded orders")
    print()

    if len(data.orders) == 0:
        info("No orders have been recorded.")
    else:
        rows = []

        for order in data.orders:
            rows.append([
                order["order_number"],
                order["customer_name"],
                order["service"],
                format(order["weight"], ".1f") + " kg",
                order["status"]
            ])

        table(
            ["ORDER NUMBER", "CUSTOMER NAME", "SERVICE / PACKAGE", "WEIGHT", "PICKUP STATUS"],
            [12, 16, 18, 9, 16],
            rows,
            status_col=4
        )

    pause()


# ============================================================
# ADMIN - DISPLAY ORDER DETAILS
# ============================================================

def display_staff_order(order):

    banner("ORDER DETAILS", order["order_number"])

    section("ORDER INFORMATION")
    field("Order Number", order["order_number"])
    field("Order Date", order["date"])
    field("Order Time", order["time"])

    section("CUSTOMER AND LAUNDRY DETAILS")
    field("Customer Name", order["customer_name"])
    print_laundry_info(order, loads_label="Loads Required", show_separate=False)

    print_price_breakdown(order)

    if order.get("ready_date"):
        field("Marked Ready", f"{order['ready_date']} {order['ready_time']}")


# ============================================================
# ADMIN - VIEW ORDER DETAILS
# ============================================================

def view_order_details():
    """Show order table repeatedly until the admin chooses Back."""

    while True:
        banner("VIEW ORDER DETAILS", "Select an order to see its full details")
        print()

        if len(data.orders) == 0:
            info("No orders have been recorded.")
            pause()
            return

        rows = []
        for index, order in enumerate(data.orders, start=1):
            rows.append([
                "[" + str(index) + "]",
                order["order_number"],
                order["customer_name"],
                order["service"],
                order["status"]
            ])

        table(
            ["CHOICE", "ORDER NUMBER", "CUSTOMER NAME", "SERVICE / PACKAGE", "PICKUP STATUS"],
            [6, 12, 16, 18, 16],
            rows,
            status_col=4
        )

        print()
        menu_item("0", "Back")
        print()

        choice = ask("Select order: ").strip()

        if choice == "0":
            return

        try:
            order_index = int(choice)
            if 1 <= order_index <= len(data.orders):
                display_staff_order(data.orders[order_index - 1])
                pause()
                # Loop repeats, returning to the order table instead of Admin Menu.
                continue

            error("Invalid selection.")
        except ValueError:
            error("Please enter a valid number.")


# ============================================================
# ADMIN - MARK ORDER READY (SINGLE / MULTIPLE / SELECT ALL)
# ============================================================

def mark_order_ready_menu():
    """Allow admin to mark one, several, or all pending orders as ready."""

    banner("MARK ORDER AS READY", "Mark one, several, or all pending orders")
    print()

    # Only orders that are not ready should be selectable.
    not_ready_orders = [
        order for order in data.orders
        if order.get("status") != "READY TO PICK UP"
    ]

    if not not_ready_orders:
        info("All orders are already ready for pickup.")
        pause()
        return

    rows = []

    for index, order in enumerate(not_ready_orders, start=1):
        rows.append([
            "[" + str(index) + "]",
            order["order_number"],
            order["customer_name"],
            order["service"],
            format(order["weight"], ".1f") + " kg",
            order["status"]
        ])

    table(
        ["CHOICE", "ORDER NUMBER", "CUSTOMER NAME", "SERVICE / PACKAGE", "WEIGHT", "STATUS"],
        [6, 12, 16, 18, 9, 16],
        rows,
        status_col=5
    )

    # Dynamic choice avoids conflicting with order numbers in the table.
    select_all_choice = len(not_ready_orders) + 1

    print()
    menu_item(str(select_all_choice), "Select All NOT READY Orders")
    menu_item("0", "Back")
    print()
    hint("Select one or multiple orders separated by commas (e.g., 1,2).")
    hint(f"Choose [{select_all_choice}] to select all pending orders.")
    print()

    while True:
        raw_choice = ask("Select completed order(s): ").strip()

        if raw_choice == "0":
            return

        try:
            # A single dynamic select-all number selects every pending order.
            if raw_choice == str(select_all_choice):
                selected_orders = list(not_ready_orders)
            else:
                parts = [part.strip() for part in raw_choice.split(",")]
                if not parts or any(not part.isdigit() for part in parts):
                    error("Invalid input. Enter choice numbers separated by commas.")
                    continue

                choices = [int(part) for part in parts]
                if len(set(choices)) != len(choices):
                    error("Duplicate choices detected. Please enter each choice once.")
                    continue
                if any(choice < 1 or choice > len(not_ready_orders) for choice in choices):
                    error("Invalid selection. Choose a listed order, Select All, or 0 to go back.")
                    continue

                selected_orders = [not_ready_orders[choice - 1] for choice in choices]

            section("SELECTED ORDERS")
            selected_rows = []
            for order in selected_orders:
                selected_rows.append([
                    order["order_number"],
                    order["customer_name"],
                    order["service"]
                ])

            table(
                ["ORDER NUMBER", "CUSTOMER NAME", "SERVICE / PACKAGE"],
                [12, 16, 18],
                selected_rows
            )

            print()
            info(f"Total selected: {len(selected_orders)}")
            print()
            menu_item("1", "Confirm and Mark as Ready")
            menu_item("2", "Cancel")
            print()

            while True:
                confirm = ask("Enter choice: ").strip()
                if confirm in ("1", "2"):
                    break
                error("Invalid choice. Please enter 1 to confirm or 2 to cancel.")

            if confirm == "2":
                print()
                warn("No orders were changed.")
                pause()
                return

            # Update only selected orders that remain NOT READY.
            updated = 0
            for order in selected_orders:
                if order.get("status") != "READY TO PICK UP":
                    mark_order_ready(order)
                    updated += 1

            if updated == len(not_ready_orders) and len(selected_orders) == len(not_ready_orders):
                headline = f"✓ SUCCESS! All {updated} orders marked as READY TO PICK UP."
            else:
                headline = f"✓ SUCCESS! {updated} order(s) marked as READY TO PICK UP."

            box(
                [
                    headline,
                    "The updated pickup status is now available in the customer status checker.",
                ],
                "green"
            )
            pause()
            return

        except (ValueError, IndexError):
            error("Invalid selection. Please try again.")


# ============================================================
# ADMIN - VIEW READY ORDERS
# ============================================================

def view_ready_orders():

    banner("ORDERS READY FOR PICKUP", "Laundry that customers can already collect")
    print()

    rows = []

    for order in data.orders:
        if order["status"] == "READY TO PICK UP":
            rows.append([
                order["order_number"],
                order["customer_name"],
                order["service"],
                format(order["weight"], ".1f") + " kg",
                order["status"]
            ])

    if not rows:
        info("There are no orders ready for pickup.")
    else:
        table(
            ["ORDER NUMBER", "CUSTOMER NAME", "SERVICE / PACKAGE", "WEIGHT", "PICKUP STATUS"],
            [12, 16, 18, 9, 16],
            rows,
            status_col=4
        )

    pause()


# ============================================================
# ADMIN MENU
# ============================================================

def staff_menu():

    while True:
        banner("ADMIN MENU", "Manage laundry orders")
        print()

        menu_item("1", "View All Orders")
        menu_item("2", "View Order Details")
        menu_item("3", "Mark Order as Ready")
        menu_item("4", "View Ready for Pickup")
        menu_item("5", "Logout")
        print()

        choice = ask("Enter choice (1-5): ").strip()

        if choice == "1":
            view_all_orders()

        elif choice == "2":
            view_order_details()

        elif choice == "3":
            mark_order_ready_menu()

        elif choice == "4":
            view_ready_orders()

        elif choice == "5":
            print()
            info("Admin logged out.")
            return

        else:
            error("Invalid choice.")
