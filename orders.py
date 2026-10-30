# ============================================================
# CABZ LAUNDRY SYSTEM - ORDERS
# ============================================================

from datetime import datetime

import data

from services import (
    get_customer_name,
    get_weight,
    get_service,
    get_wash_duration,
    get_dry_duration,
    get_additional_items,
    get_special_instructions,
    get_separation_loads,
    calculate_loads,
    calculate_total
)

from receipt import print_receipt, print_laundry_info, print_price_breakdown

from utils import (
    banner, section, field, menu_item, ask,
    success, error, warn, info, box
)


# ============================================================
# ORDER STATUS
# ============================================================

def mark_order_ready(order):
    """Admin uses this only when the laundry is actually ready."""

    order["status"] = "READY TO PICK UP"
    order["ready_date"] = datetime.now().strftime("%B %d, %Y")
    order["ready_time"] = datetime.now().strftime("%I:%M %p")

    return order["status"]


# ============================================================
# DISPLAY ORDER SUMMARY
# ============================================================

def display_order_summary(order):

    banner("ORDER SUMMARY", "Please review your order before confirming")

    section("CUSTOMER AND LAUNDRY DETAILS")
    field("Customer Name", order["customer_name"])
    print_laundry_info(order)

    print_price_breakdown(order)


# ============================================================
# EDIT ORDER
# ============================================================

def edit_order(order):

    while True:
        banner("EDIT ORDER", "Choose what you want to change")
        print()

        menu_item("1", "Customer Name")
        menu_item("2", "Laundry Weight")
        menu_item("3", "Service / Package")
        menu_item("4", "Wash Duration")
        menu_item("5", "Dry Duration")
        menu_item("6", "Additional Items")
        menu_item("7", "Special Instructions")
        menu_item("8", "Finish Editing")
        print()

        choice = ask("Select what to edit: ").strip()

        if choice == "1":
            order["customer_name"] = get_customer_name()

        elif choice == "2":
            order["weight"] = get_weight()
            weight_loads = calculate_loads(order["weight"])
            order["loads"] = max(weight_loads, order.get("separation_loads", 1))
            order["total"] = calculate_total(
                order["service"],
                order["loads"],
                order["additional_price"]
            )

        elif choice == "3":
            order["service"] = get_service()
            order["wash_duration"] = None
            order["dry_duration"] = None

            if order["service"] == "Wash Only":
                order["wash_duration"] = get_wash_duration()

            elif order["service"] == "Dry Only":
                order["dry_duration"] = get_dry_duration()

            else:
                order["wash_duration"] = get_wash_duration()
                order["dry_duration"] = get_dry_duration()

            order["total"] = calculate_total(
                order["service"],
                order["loads"],
                order["additional_price"]
            )

        elif choice == "4":
            if order["service"] == "Dry Only":
                info("Wash duration is not required.")
            else:
                order["wash_duration"] = get_wash_duration()

        elif choice == "5":
            if order["service"] == "Wash Only":
                info("Dry duration is not required.")
            else:
                order["dry_duration"] = get_dry_duration()

        elif choice == "6":
            item, item_price = get_additional_items()
            order["additional_item"] = item
            order["additional_price"] = item_price
            order["total"] = calculate_total(
                order["service"],
                order["loads"],
                order["additional_price"]
            )

        elif choice == "7":
            order["special_instructions"] = get_special_instructions()
            order["separation_loads"] = get_separation_loads(
                order["special_instructions"]
            )
            weight_loads = calculate_loads(order["weight"])
            order["loads"] = max(weight_loads, order["separation_loads"])
            order["total"] = calculate_total(
                order["service"],
                order["loads"],
                order["additional_price"]
            )

        elif choice == "8":
            print()
            success("Order editing finished.")
            return

        else:
            error("Invalid choice.")


# ============================================================
# CREATE LAUNDRY ORDER
# ============================================================

def create_order():

    banner("CREATE LAUNDRY ORDER", "Fill in the details of your laundry")
    print()

    customer_name = get_customer_name()
    weight = get_weight()
    service = get_service()

    wash_duration = None
    dry_duration = None

    if service == "Wash Only":
        wash_duration = get_wash_duration()

    elif service == "Dry Only":
        dry_duration = get_dry_duration()

    else:
        wash_duration = get_wash_duration()
        dry_duration = get_dry_duration()

    additional_item, additional_price = get_additional_items()
    special_instructions = get_special_instructions()
    separation_loads = get_separation_loads(special_instructions)

    weight_loads = calculate_loads(weight)
    loads = max(weight_loads, separation_loads)

    total = calculate_total(
        service,
        loads,
        additional_price
    )

    order = {
        "order_number": "",
        "customer_name": customer_name,
        "weight": weight,
        "service": service,
        "wash_duration": wash_duration,
        "dry_duration": dry_duration,
        "additional_item": additional_item,
        "additional_price": additional_price,
        "special_instructions": special_instructions,
        "separation_loads": separation_loads,
        "loads": loads,
        "total": total,
        "date": "",
        "time": "",
        "ready_date": "",
        "ready_time": "",
        "status": "NOT READY"
    }

    while True:
        display_order_summary(order)

        section("WHAT WOULD YOU LIKE TO DO?")
        menu_item("1", "EDIT ORDER")
        menu_item("2", "CONFIRM ORDER")
        menu_item("3", "CANCEL ORDER")
        print()

        choice = ask("Enter choice: ").strip()

        if choice == "1":
            edit_order(order)

        elif choice == "2":
            data.order_counter += 1

            order["order_number"] = (
                "CABZ-" + str(data.order_counter).zfill(4)
            )

            current_time = datetime.now()
            order["date"] = current_time.strftime("%B %d, %Y")
            order["time"] = current_time.strftime("%I:%M %p")
            order["status"] = "NOT READY"

            data.orders.append(order)

            box(
                [
                    "✓ ORDER CONFIRMED!",
                    "Your order has been successfully recorded.",
                    "The admin will mark it ready when the laundry is finished.",
                ],
                "green"
            )

            print_receipt(order)

            input("\n  » Press ENTER to Continue to Customer Menu...")
            return

        elif choice == "3":
            print()
            warn("Order cancelled.")
            return

        else:
            error("Invalid choice.")
