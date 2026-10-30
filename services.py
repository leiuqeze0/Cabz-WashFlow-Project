# ============================================================
# CABZ LAUNDRY SYSTEM - SERVICES
# ============================================================

from config import (
    CAPACITY,
    PRICE_WASH,
    PRICE_DRY,
    PRICE_WASH_DRY,
    PRICE_WASH_DRY_FOLD,
    PRICE_DETERGENT,
    PRICE_FABRIC_SOFTENER,
    PRICE_BLEACH
)

from utils import (
    pause, banner, section, menu_item, ask,
    success, error, info, hint, table
)


# ============================================================
# CUSTOMER INPUT
# ============================================================

def get_customer_name():
    """Get a non-empty customer name; reject names made only of numbers."""

    while True:
        name = ask("Enter Customer Name: ").strip()

        # Permit letters (including accented letters), spaces, periods,
        # apostrophes, and hyphens. Reject numeric-only or symbol-only input.
        valid_name = any(char.isalpha() for char in name) and all(
            char.isalpha() or char.isspace() or char in ".'-"
            for char in name
        )

        if valid_name:
            return name

        error("Please enter a valid name using letters, spaces, apostrophes, periods, or hyphens.")


def get_weight():

    while True:
        try:
            weight = float(ask("Enter Laundry Weight (kg): "))

            if weight > 0:
                return weight

            error("Weight must be greater than 0 kg.")

        except ValueError:
            error("Invalid input. Please enter a number.")


def get_special_instructions():
    # Special instructions are for admin reference only.
    # They do not affect loads, pricing, or other calculations.

    section("SPECIAL INSTRUCTIONS")
    hint("Example: Please separate white clothes.")
    hint("Press Enter if there are no special instructions.")

    instructions = ask("Instructions: ").strip()

    if instructions == "":
        return "None"

    return instructions


# ============================================================
# SERVICE SELECTION
# ============================================================

def get_service():

    while True:
        section("SELECT LAUNDRY SERVICE / PACKAGE")
        menu_item("1", "Wash Only")
        menu_item("2", "Dry Only")
        menu_item("3", "Wash and Dry")
        menu_item("4", "Wash, Dry and Fold Package")
        print()

        choice = ask("Enter choice (1-4): ").strip()

        if choice == "1":
            return "Wash Only"

        elif choice == "2":
            return "Dry Only"

        elif choice == "3":
            return "Wash and Dry"

        elif choice == "4":
            return "Wash, Dry and Fold"

        else:
            error("Invalid choice. Please select 1-4.")


# ============================================================
# CUSTOM TIME
# ============================================================

def get_custom_time(service_type):

    while True:
        try:
            minutes = int(
                ask(
                    "Enter customized "
                    + service_type
                    + " duration (minutes): "
                )
            )

            if minutes > 0:
                return minutes

            error("Duration must be greater than 0.")

        except ValueError:
            error("Please enter a whole number.")


# ============================================================
# WASH DURATION
# ============================================================

def get_wash_duration():

    while True:
        section("SELECT WASH DURATION")
        menu_item("1", "15 minutes")
        menu_item("2", "20 minutes")
        menu_item("3", "30 minutes")
        menu_item("4", "40 minutes")
        menu_item("5", "50 minutes")
        menu_item("6", "Customize Time")
        print()

        choice = ask("Enter choice (1-6): ").strip()

        if choice == "1":
            return 15
        elif choice == "2":
            return 20
        elif choice == "3":
            return 30
        elif choice == "4":
            return 40
        elif choice == "5":
            return 50
        elif choice == "6":
            return get_custom_time("wash")
        else:
            error("Invalid choice.")


# ============================================================
# DRY DURATION
# ============================================================

def get_dry_duration():

    while True:
        section("SELECT DRY DURATION")
        menu_item("1", "15 minutes")
        menu_item("2", "20 minutes")
        menu_item("3", "30 minutes")
        menu_item("4", "40 minutes")
        menu_item("5", "50 minutes")
        menu_item("6", "Customize Time")
        print()

        choice = ask("Enter choice (1-6): ").strip()

        if choice == "1":
            return 15
        elif choice == "2":
            return 20
        elif choice == "3":
            return 30
        elif choice == "4":
            return 40
        elif choice == "5":
            return 50
        elif choice == "6":
            return get_custom_time("dry")
        else:
            error("Invalid choice.")


# ============================================================
# ADDITIONAL ITEMS
# ============================================================

def get_item_quantity(item_name):

    while True:
        try:
            quantity = int(ask(f"How many {item_name} do you want? "))

            if quantity > 0:
                return quantity

            error("Quantity must be greater than 0.")

        except ValueError:
            error("Please enter a whole number.")


def get_additional_items():

    selected_items = []
    total_price = 0

    while True:
        section("ADDITIONAL ITEMS")
        menu_item("1", f"Detergent        - PHP {PRICE_DETERGENT} each")
        menu_item("2", f"Fabric Softener  - PHP {PRICE_FABRIC_SOFTENER} each")
        menu_item("3", f"Bleach           - PHP {PRICE_BLEACH} each")
        menu_item("4", "Done / No More Additional Items")
        print()

        choice = ask("Enter choice (1-4): ").strip()

        if choice == "1":
            quantity = get_item_quantity("Detergent")
            selected_items.append(f"Detergent x{quantity}")
            total_price += PRICE_DETERGENT * quantity
            success(f"{quantity} Detergent added.")

        elif choice == "2":
            quantity = get_item_quantity("Fabric Softener")
            selected_items.append(f"Fabric Softener x{quantity}")
            total_price += PRICE_FABRIC_SOFTENER * quantity
            success(f"{quantity} Fabric Softener added.")

        elif choice == "3":
            quantity = get_item_quantity("Bleach")
            selected_items.append(f"Bleach x{quantity}")
            total_price += PRICE_BLEACH * quantity
            success(f"{quantity} Bleach added.")

        elif choice == "4":
            if not selected_items:
                return "None", 0

            return ", ".join(selected_items), total_price

        else:
            error("Invalid choice. Please select 1-4.")


# ============================================================
# SPECIAL INSTRUCTIONS / OPTIONAL SEPARATION
# ============================================================

def get_separation_loads(instructions):
   

    text = instructions.lower()

    separation_words = [
        "separate", "segregate", "segregated", "do not mix",
        "don't mix", "dont mix", "keep separate", "put separately",
        "separate white", "white clothes", "white cloth",
        "colored clothes", "colour clothes", "color clothes",
        "dark clothes", "different load", "separate load"
    ]

    if instructions == "None" or not any(word in text for word in separation_words):
        return 1

    section("SEPARATE LOADS")
    info("The instruction may require separate laundry cycles.")
    hint("Example: white clothes separated from colored clothes.")
    hint("The instruction itself does not change the load count.")
    hint("This question lets you specify the actual separate machine cycles.")

    while True:
        print()
        print("  Do you want the laundry separated into separate machine cycles?")
        menu_item("1", "Yes - use separate loads")
        menu_item("2", "No - keep the laundry in the normal load calculation")
        print()

        choice = ask("Enter choice (1-2): ").strip()

        if choice == "1":
            while True:
                try:
                    separate_loads = int(ask("How many separate loads/cycles are needed? "))

                    if separate_loads >= 2:
                        return separate_loads

                    error("Please enter at least 2 loads/cycles.")

                except ValueError:
                    error("Please enter a whole number.")

        elif choice == "2":
            return 1

        else:
            error("Invalid choice. Please select 1 or 2.")


# ============================================================
# DISPLAY SERVICES
# ============================================================

def display_services():

    banner("CABZ LAUNDRY SERVICES", "Prices and Packages")

    section("LAUNDRY SERVICES / PACKAGES")
    table(
        ["NO.", "SERVICE / PACKAGE", "PRICE PER LOAD"],
        [4, 24, 16],
        [
            ["1", "Wash Only", f"PHP {PRICE_WASH}"],
            ["2", "Dry Only", f"PHP {PRICE_DRY}"],
            ["3", "Wash and Dry", f"PHP {PRICE_WASH_DRY}"],
            ["4", "Wash, Dry & Fold", f"PHP {PRICE_WASH_DRY_FOLD}"],
        ]
    )

    section("ADDITIONAL ITEMS")
    table(
        ["NO.", "ITEM", "PRICE EACH"],
        [4, 24, 16],
        [
            ["1", "Detergent", f"PHP {PRICE_DETERGENT}"],
            ["2", "Fabric Softener", f"PHP {PRICE_FABRIC_SOFTENER}"],
            ["3", "Bleach", f"PHP {PRICE_BLEACH}"],
        ]
    )

    section("GOOD TO KNOW")
    info(f"Machine Capacity: {CAPACITY} kg per load")
    info("Wash: 15, 20, 30, 40, or 50 minutes")
    info("Dry:  15, 20, 30, 40, or 50 minutes")
    info("Customized time is also available.")
    info("Special instructions are available when creating an order.")

    pause()


# ============================================================
# CALCULATE LOADS
# Loads are based only on laundry weight. Special instructions do not affect this calculation.
# ============================================================

def calculate_loads(weight):

    load_count = 0
    remaining_weight = weight

    while remaining_weight > 0:
        load_count += 1
        remaining_weight -= CAPACITY

    return load_count


# ============================================================
# GET SERVICE PRICE
# ============================================================

def get_service_price(service):

    if service == "Wash Only":
        return PRICE_WASH

    elif service == "Dry Only":
        return PRICE_DRY

    elif service == "Wash and Dry":
        return PRICE_WASH_DRY

    else:
        return PRICE_WASH_DRY_FOLD


# ============================================================
# CALCULATE TOTAL SERVICE CHARGE
# ============================================================

def calculate_total(service, loads, additional_price):

    service_price = get_service_price(service)

    return (service_price * loads) + additional_price
