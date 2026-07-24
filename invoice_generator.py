"""
Invoice Generator
------------------
SoftGrowTech Internship - Task 1 (Python Programming)
Project 3: Invoice Generator

Description:
A menu-driven console application that generates a bill/invoice based on
user input. It supports adding multiple items, applies tax and discount,
calculates the final total, and saves the generated invoice to a text
file (file handling), along with a running log of all invoices created.

Author: <Your Name>
"""

import os
from datetime import datetime

INVOICE_FOLDER = "invoices"
INVOICE_LOG_FILE = "invoice_log.txt"

TAX_RATE = 0.05          # 5% tax
DISCOUNT_THRESHOLD = 1000  # Orders above this amount get a discount
DISCOUNT_RATE = 0.10      # 10% discount


def ensure_invoice_folder():
    """Create the folder where individual invoice files will be stored."""
    if not os.path.exists(INVOICE_FOLDER):
        os.makedirs(INVOICE_FOLDER)


def get_customer_details():
    """Collect basic customer information from the user."""
    print("\n--- Customer Details ---")
    name = input("Enter customer name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter customer name: ").strip()

    phone = input("Enter customer phone number: ").strip()
    return {"name": name, "phone": phone}


def get_items():
    """Collect item details (name, quantity, price) from the user."""
    items = []
    print("\n--- Add Items ---")
    while True:
        item_name = input("Enter item name (or 'done' to finish): ").strip()
        if item_name.lower() == "done":
            if not items:
                print("You must add at least one item.")
                continue
            break
        if not item_name:
            print("Item name cannot be empty.")
            continue

        quantity = get_positive_number("Enter quantity: ", integer=True)
        price = get_positive_number("Enter price per unit: ")

        subtotal = quantity * price
        items.append({
            "name": item_name,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal
        })
        print(f"Added: {item_name} x{quantity} @ {price:.2f} = {subtotal:.2f}")

    return items


def get_positive_number(prompt, integer=False):
    """Helper to safely read a positive number (int or float) from user input."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value) if integer else float(value)
            if number <= 0:
                print("Please enter a value greater than 0.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def calculate_totals(items):
    """Calculate subtotal, tax, discount, and grand total."""
    subtotal = sum(item["subtotal"] for item in items)
    tax = subtotal * TAX_RATE
    discount = subtotal * DISCOUNT_RATE if subtotal > DISCOUNT_THRESHOLD else 0
    grand_total = subtotal + tax - discount

    return {
        "subtotal": subtotal,
        "tax": tax,
        "discount": discount,
        "grand_total": grand_total
    }


def generate_invoice_number():
    """Generate a simple unique invoice number based on date and time."""
    return "INV-" + datetime.now().strftime("%Y%m%d-%H%M%S")


def build_invoice_text(invoice_no, customer, items, totals):
    """Format the invoice into a readable text block."""
    lines = []
    lines.append("=" * 45)
    lines.append("               INVOICE".center(45))
    lines.append("=" * 45)
    lines.append(f"Invoice No : {invoice_no}")
    lines.append(f"Date       : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    lines.append(f"Customer   : {customer['name']}")
    lines.append(f"Phone      : {customer['phone']}")
    lines.append("-" * 45)
    lines.append(f"{'Item':<15}{'Qty':>5}{'Price':>10}{'Subtotal':>15}")
    lines.append("-" * 45)

    for item in items:
        lines.append(
            f"{item['name']:<15}{item['quantity']:>5}"
            f"{item['price']:>10.2f}{item['subtotal']:>15.2f}"
        )

    lines.append("-" * 45)
    lines.append(f"{'Subtotal':<35}{totals['subtotal']:>10.2f}")
    lines.append(f"{'Tax (5%)':<35}{totals['tax']:>10.2f}")
    lines.append(f"{'Discount':<35}{-totals['discount']:>10.2f}")
    lines.append("-" * 45)
    lines.append(f"{'GRAND TOTAL':<35}{totals['grand_total']:>10.2f}")
    lines.append("=" * 45)
    lines.append("Thank you for your business!".center(45))
    lines.append("=" * 45)

    return "\n".join(lines)


def save_invoice(invoice_no, invoice_text):
    """Save the invoice to its own file and append a summary to the log file."""
    ensure_invoice_folder()
    file_path = os.path.join(INVOICE_FOLDER, f"{invoice_no}.txt")

    with open(file_path, "w") as f:
        f.write(invoice_text)

    with open(INVOICE_LOG_FILE, "a") as log:
        log.write(f"{invoice_no} generated on "
                   f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")

    return file_path


def view_past_invoices():
    """List previously generated invoices from the log file."""
    print("\n--- Past Invoices ---")
    if not os.path.exists(INVOICE_LOG_FILE):
        print("No invoices have been generated yet.")
        return

    with open(INVOICE_LOG_FILE, "r") as log:
        content = log.read().strip()
        print(content if content else "No invoices have been generated yet.")


def generate_new_invoice():
    """Full workflow to create, display, and save a new invoice."""
    customer = get_customer_details()
    items = get_items()
    totals = calculate_totals(items)
    invoice_no = generate_invoice_number()
    invoice_text = build_invoice_text(invoice_no, customer, items, totals)

    print("\n" + invoice_text)

    file_path = save_invoice(invoice_no, invoice_text)
    print(f"\nInvoice saved successfully to: {file_path}")


def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n===== INVOICE GENERATOR =====")
        print("1. Generate New Invoice")
        print("2. View Past Invoices Log")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            generate_new_invoice()
        elif choice == "2":
            view_past_invoices()
        elif choice == "3":
            print("Thank you for using Invoice Generator. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main_menu()
