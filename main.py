# ============================================================
# CABZ LAUNDRY SERVICES AND ORDER STATUS MONITORING SYSTEM
# ============================================================

from customer import customer_menu
from staff import staff_access
from services import display_services
from utils import display_header, pause, section, menu_item, ask, error, box


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        display_header()

        section("MAIN MENU")

        menu_item("1", "Customer")
        menu_item("2", "Admin")
        menu_item("3", "View Laundry Services and Prices")
        menu_item("4", "Exit")
        print()

        choice = ask(
            "Enter your choice (1-4): "
        )

        if choice == "1":

            # Dili na mo-login ang customer, diretso sa customer menu

            customer_menu()

        elif choice == "2":

            # ang admin mo-login sa ilang account para ma-access ang admin menu

            staff_access()

        elif choice == "3":

            display_services()

        elif choice == "4":

            box(
                [
                    "Thank you for using Cabz Laundry System!",
                    "System closed.",
                ]
            )
            print()

            break

        else:

            error(
                "Invalid choice. Please select 1-4."
            )

            pause()


# ============================================================
# RUN SYSTEM
# ============================================================

if __name__ == "__main__":
    main()
