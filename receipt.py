# ============================================================
# CABZ LAUNDRY SYSTEM - RECEIPT
# ============================================================

from services import get_service_price
from utils import banner, section, field, rule, box, badge


# ============================================================
# SHARED DISPLAY: LAUNDRY INFORMATION
# (gigamit sa Order Summary, Receipt, ug Admin Order Details)
# ============================================================

def print_laundry_info(order, loads_label="Number of Loads", show_separate=True):

    field("Laundry Weight", f"{order['weight']} kg")
    field("Service / Package", order["service"])

    if order["service"] == "Wash Only":
        field("Wash Duration", f"{order['wash_duration']} minutes")

    elif order["service"] == "Dry Only":
        field("Dry Duration", f"{order['dry_duration']} minutes")

    else:
        field("Wash Duration", f"{order['wash_duration']} minutes")
        field("Dry Duration", f"{order['dry_duration']} minutes")

        if order["service"] == "Wash, Dry and Fold":
            field("Folding", "Included")

    field("Additional Items", order["additional_item"])
    field("Special Instructions", order["special_instructions"])
    field(loads_label, order["loads"])

    if show_separate:
        if order.get("separation_loads", 1) > 1:
            field("Separate Loads", "Yes")
        else:
            field("Separate Loads", "No")


# ============================================================
# SHARED DISPLAY: PRICE BREAKDOWN
# Kini ang usa ra nga lugar nga nag-print sa price breakdown,
# kaya parehas gyud ang Order Summary, Receipt, ug Admin view.
# ============================================================

def print_price_breakdown(order):

    service_price = get_service_price(order["service"])
    service_total = service_price * order["loads"]
    additional_price = order.get("additional_price", 0)

    section("PRICE BREAKDOWN")

    field("Selected Service", order["service"])
    field("Service Rate", f"PHP {service_price:.2f} per load")
    field("Number of Loads", order["loads"])
    field("Service Subtotal", f"PHP {service_total:.2f}")
    field("Additional Items", order["additional_item"])
    field("Additional Items Fee", f"PHP {additional_price:.2f}")

    rule()

    field("TOTAL SERVICE CHARGE", f"PHP {order['total']:.2f}", bold=True)
    field("Pickup Status", badge(order["status"]))


# ============================================================
# PRINT RECEIPT
# ============================================================

def print_receipt(order):

    banner("CABZ LAUNDRY RECEIPT", "Order Summary")

    section("ORDER INFORMATION")
    field("Order Number", order["order_number"])
    field("Date", order["date"])
    field("Time", order["time"])

    section("CUSTOMER AND LAUNDRY DETAILS")
    field("Customer Name", order["customer_name"])
    print_laundry_info(order)

    print_price_breakdown(order)

    box(["Please keep your order number for pickup status checking."])
