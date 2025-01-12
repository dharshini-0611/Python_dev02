import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from fpdf import FPDF
from datetime import datetime, timedelta

USD_TO_INR = 83

def calculate_due_date():
    try:
        invoice_date = datetime.strptime(invoice_date_entry.get(), '%Y-%m-%d')
        payment_terms = int(payment_terms_entry.get())
        due_date = invoice_date + timedelta(days=payment_terms)
        due_date_label.config(text=f"Due Date: {due_date.strftime('%Y-%m-%d')}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid invoice date (YYYY-MM-DD) and payment terms (integer).")
def add_item():
    category = category_var.get()
    description = description_entry.get().strip()
    quantity = quantity_entry.get().strip()
    price = price_entry.get().strip()
    tax_rate = tax_rate_entry.get().strip()
    if not category or not description or not quantity or not price or not tax_rate:
        messagebox.showerror("Input Error", "All fields are required!")
        return
    try:
        quantity = int(quantity)
        price = float(price)
        tax_rate = float(tax_rate)

        total = quantity * price
        tax = total * (tax_rate / 100)
        total_with_tax = total + tax

        price_inr = price * USD_TO_INR
        total_inr = total_with_tax * USD_TO_INR
        items_listbox.insert(tk.END, f"{category} - {description} | Qty: {quantity} | Price: Rs {price_inr:.2f} | Tax: {tax_rate}% | Total: Rs {total_inr:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for quantity, price, and tax rate.")
def generate_invoice():
    customer_name = customer_name_entry.get().strip()
    customer_address = customer_address_entry.get().strip()
    phone_number = phone_number_entry.get().strip()
    date_of_service = date_of_service_entry.get().strip()
    invoice_date = invoice_date_entry.get().strip()
    payment_terms = payment_terms_entry.get().strip()
    if not customer_name or not customer_address or not phone_number or not date_of_service or not invoice_date or not payment_terms:
        messagebox.showerror("Input Error", "All fields are required!")
        return
    try:
        payment_terms = int(payment_terms)
        due_date = (datetime.strptime(invoice_date, '%Y-%m-%d') + timedelta(days=payment_terms)).strftime('%Y-%m-%d')

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=10)
        try:
            pdf.image("shop_logo.jpg", x=10, y=8, w=30)  
        except FileNotFoundError:
            messagebox.showerror("Error", "Logo file 'shop_logo.jpg' not found!")
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="Classic Corner Shop", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 5, txt="14B,Classic Street,Chennai-600 001", ln=True, align='C')
        pdf.cell(0, 5, txt="Phone: 987-654-3210 | Email: info@classiccorner.com", ln=True, align='C')

        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Customer Name: {customer_name}", ln=True)
        pdf.cell(0, 8, f"Customer Address: {customer_address}", ln=True)
        pdf.cell(0, 8, f"Phone: {phone_number}", ln=True)

        pdf.ln(5)
        pdf.cell(0, 8, f"Invoice Date: {invoice_date}", ln=True)
        pdf.cell(0, 8, f"Date of Service: {date_of_service}", ln=True)
        pdf.cell(0, 8, f"Payment Terms: {payment_terms} days", ln=True)
        pdf.cell(0, 8, f"Due Date: {due_date}", ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, 'Description', 1, align='C')
        pdf.cell(25, 10, 'Quantity', 1, align='C')
        pdf.cell(35, 10, 'Unit Price (Rs)', 1, align='C')
        pdf.cell(25, 10, 'Tax Rate (%)', 1, align='C')
        pdf.cell(35, 10, 'Total (Rs)', 1, align='C')
        pdf.ln()

        pdf.set_font("Arial", '', 10)
        total_amount = 0
        for index in range(items_listbox.size()):
            item = items_listbox.get(index)

            parts = item.split(" | ")
            description = parts[0].split(" - ")[1]
            quantity = parts[1].split(": ")[1]
            price = parts[2].split(": ")[1].replace("Rs ", "")
            tax_rate = parts[3].split(": ")[1].replace("%", "")
            total = parts[4].split(": ")[1].replace("Rs ", "")

            pdf.cell(40, 10, description, 1, align='C')
            pdf.cell(25, 10, quantity, 1, align='C')
            pdf.cell(35, 10, f"Rs {price}", 1, align='C')
            pdf.cell(25, 10, f"{tax_rate}%", 1, align='C')
            pdf.cell(35, 10, f"Rs {total}", 1, align='C')
            pdf.ln()

            total_amount += float(total)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(25, 10, f"Subtotal: Rs {total_amount:.2f}", ln=True, align='C')
        pdf.cell(45, 10, f"Total Amount Due: Rs {total_amount:.2f}", ln=True, align='C')

        pdf.ln(15)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, "Authorized Signature:", ln=True, align='L')
        pdf.ln(20)
        pdf.cell(0, 10, "____________________________", ln=True, align='L')
        pdf.cell(0, 10, "Classic Corner Shop", ln=True, align='L')

        pdf.output(f"invoice_{invoice_date}.pdf")
        messagebox.showinfo("Success", f"Invoice generated successfully!\nSaved as invoice_{invoice_date}.pdf")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating invoice: {str(e)}")
root = tk.Tk()
root.title("Invoice Generator")

tk.Label(root, text="Customer Name").grid(row=0, column=0, padx=10, pady=5)
customer_name_entry = tk.Entry(root)
customer_name_entry.grid(row=0, column=1)

tk.Label(root, text="Customer Address").grid(row=1, column=0, padx=10, pady=5)
customer_address_entry = tk.Entry(root)
customer_address_entry.grid(row=1, column=1)

tk.Label(root, text="Phone Number").grid(row=2, column=0, padx=10, pady=5)
phone_number_entry = tk.Entry(root)
phone_number_entry.grid(row=2, column=1)

tk.Label(root, text="Date of Service (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5)
date_of_service_entry = tk.Entry(root)
date_of_service_entry.grid(row=3, column=1)

tk.Label(root, text="Invoice Date (YYYY-MM-DD)").grid(row=4, column=0, padx=10, pady=5)
invoice_date_entry = tk.Entry(root)
invoice_date_entry.grid(row=4, column=1)

tk.Label(root, text="Payment Terms (Days)").grid(row=5, column=0, padx=10, pady=5)
payment_terms_entry = tk.Entry(root)
payment_terms_entry.grid(row=5, column=1)


due_date_label = tk.Label(root, text="Due Date: N/A")
due_date_label.grid(row=6, column=0, columnspan=2, pady=10)
tk.Button(root, text="Calculate Due Date", command=calculate_due_date).grid(row=7, column=0, columnspan=2)

tk.Label(root, text="Category").grid(row=8, column=0, padx=10, pady=5)
category_var = tk.StringVar()
category_menu = ttk.Combobox(root, textvariable=category_var, values=[
    "Groceries", "Household Essentials", "Health and Beauty",
    "Toys and Games", "Beverages", "Stationery",
    "Gift Items", "Classic Snacks", "Vintage Items", "Seasonal Products"])
category_menu.grid(row=8, column=1)

tk.Label(root, text="Description").grid(row=9, column=0, padx=10, pady=5)
description_entry = tk.Entry(root)
description_entry.grid(row=9, column=1)

tk.Label(root, text="Quantity").grid(row=10, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=10, column=1)

tk.Label(root, text="Price per Unit (in $)").grid(row=11, column=0, padx=10, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=11, column=1)

tk.Label(root, text="Tax Rate (%)").grid(row=12, column=0, padx=10, pady=5)
tax_rate_entry = tk.Entry(root)
tax_rate_entry.grid(row=12, column=1)

tk.Button(root, text="Add Item", command=add_item).grid(row=13, column=0, columnspan=2, pady=10)

items_listbox = tk.Listbox(root, width=100, height=10)
items_listbox.grid(row=14, column=0, columnspan=2, padx=10, pady=10)

tk.Button(root, text="Generate Invoice", command=generate_invoice).grid(row=15, column=0, columnspan=2, pady=10)

root.mainloop()
