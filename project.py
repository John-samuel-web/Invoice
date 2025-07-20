from reportlab.pdfgen import canvas

# === User Inputs ===
print("------ INVOICE GENERATOR ------")

company_name = "John Samuel Enterprises"

# Customer details
customer_name = input("Enter customer name: ")
customer_phone = input("Enter customer phone: ")
customer_address = input("Enter customer address: ")

# Number of items
num_items = int(input("Enter number of items: "))

# Default GST
default_tax = 0.18  # 18% GST

# Input Lists
item = []
warranty = []
unit_price = []
qty = []
tax = []

for i in range(num_items):
    print(f"\nEnter details for Item {i+1}:")
    item.append(input("Item name: "))
    warranty.append(int(input("Warranty (months): ")))
    unit_price.append(float(input("Unit price: ")))
    qty.append(int(input("Quantity: ")))
    tax.append(default_tax)

# Optional charges
discount = float(input("Enter discount amount (₹): "))
service_charge = float(input("Enter service charge (₹): "))

# === Product Object Setup ===
objects = []
class Product:
    def __init__(self, item, warranty, unit_price, tax, quantity):
        self.item = item
        self.unit_price = unit_price
        self.warranty = warranty
        self.tax = tax
        self.quantity = quantity
        self.t_price = unit_price * quantity

for x in range(len(item)):
    obj = Product(item[x], warranty[x], unit_price[x], tax[x], qty[x])
    objects.append(obj)

# === PDF Setup ===
fileName = 'sample_invoice.pdf'
pdf = canvas.Canvas(fileName)
pdf.setTitle("Invoice")

# Layout Offsets
y_offset = 0
cust_offset = 50
table_offset = 0
sub_total_y_offset = -5

# === Header Section ===
pdf.setFont("Helvetica-Bold", 36)
pdf.setFillColorRGB(.3, .3, .3)
pdf.drawString(40, 735 - y_offset, "INVOICE")
pdf.setFont("Helvetica", 13)
pdf.setFillColorRGB(0, 0, 0)

# Company Details
pdf.drawRightString(550, 750 - y_offset, company_name)
pdf.drawRightString(550, 730 - y_offset, "Hyderabad, India")
pdf.drawRightString(550, 710 - y_offset, "contact@johnsamuel.com")
pdf.drawRightString(550, 690 - y_offset, "+91 9876543210")

# === Customer Section ===
y_offset += cust_offset
pdf.setFont("Helvetica-Bold", 13)
pdf.drawString(40, 680 - y_offset, "Billed To:")
pdf.setFont("Helvetica", 13)
pdf.drawString(40, 660 - y_offset, customer_name)
pdf.drawString(40, 640 - y_offset, customer_phone)
pdf.drawString(40, 620 - y_offset, customer_address)

# Invoice Info
pdf.drawRightString(550, 660 - y_offset, "Invoice : #001")
pdf.drawRightString(550, 640 - y_offset, "Issued on : Today")
pdf.drawRightString(550, 620 - y_offset, "Payment Status : Paid")

# === Items Table Header ===
y_offset += table_offset
unit_price_x_pos = 370
warranty_x_pos = 280
qty_x_pos = 470
price_x_pos = 550

pdf.setFont("Helvetica-Bold", 12)
pdf.setLineWidth(.2)
pdf.line(40, 600 - y_offset, 550, 600 - y_offset)
pdf.drawString(40, 585 - y_offset, "Item")
pdf.drawString(warranty_x_pos, 585 - y_offset, "Warranty")
pdf.line(40, 580 - y_offset, 550, 580 - y_offset)
pdf.drawString(unit_price_x_pos, 585 - y_offset, "Unit Price")
pdf.drawCentredString(qty_x_pos, 585 - y_offset, "Qty")
pdf.drawRightString(price_x_pos, 585 - y_offset, "Price")
pdf.setFont("Helvetica", 13)

# === Items Table Rows ===
for i in range(len(objects)):
    y_pos = 565 - y_offset - 20 * i
    pdf.drawString(40, y_pos, objects[i].item)
    pdf.drawString(warranty_x_pos, y_pos, str(objects[i].warranty))
    pdf.setFont("Helvetica", 10)
    pdf.drawString(warranty_x_pos + 18, y_pos, "Months")
    pdf.setFont("Helvetica", 13)
    pdf.drawRightString(unit_price_x_pos + 40, y_pos, str(objects[i].unit_price))
    pdf.setFont("Helvetica", 10)
    pdf.drawString(unit_price_x_pos + 45, y_pos, "+GST")
    pdf.setFont("Helvetica", 13)
    pdf.drawString(qty_x_pos, y_pos, str(objects[i].quantity))
    pdf.drawRightString(price_x_pos, y_pos, str(objects[i].t_price))

pdf.line(40, 565 - y_offset - 20 * i - 5, 556, 565 - y_offset - 20 * i - 5)

# === Totals Calculation ===
total_tax = sum([obj.t_price * obj.tax for obj in objects])
sub_total = sum([obj.t_price for obj in objects])

# Offsets for totals
y_offset += sub_total_y_offset
labels_x_pos = 480

pdf.drawRightString(labels_x_pos, 565 - y_offset - 20 * i - 25, "Sub Total : ")
pdf.drawRightString(550, 565 - y_offset - 20 * i - 25, str(sub_total))

pdf.drawRightString(labels_x_pos, 565 - y_offset - 20 * i - 40, "GST (18%) : ")
pdf.drawRightString(550, 565 - y_offset - 20 * i - 40, "+ " + str(round(total_tax, 2)))

if service_charge:
    y_offset += 10
    pdf.drawRightString(labels_x_pos, 565 - y_offset - 20 * i - 45, "Service Charge : ")
    pdf.drawRightString(550, 565 - y_offset - 20 * i - 45, "+ " + str(service_charge))

if discount:
    y_offset += 10
    pdf.drawRightString(labels_x_pos, 565 - y_offset - 20 * i - 45, "Discount : ")
    pdf.drawRightString(550, 565 - y_offset - 20 * i - 45, "- " + str(discount))

# Final Total
final_total = sub_total + total_tax + service_charge - discount
pdf.line(380, 565 - y_offset - 20 * i - 45, 556, 565 - y_offset - 20 * i - 45)
pdf.setFont("Helvetica-Bold", 15)
pdf.drawRightString(labels_x_pos, 565 - y_offset - 20 * i - 63, "Total : ")
pdf.drawRightString(550, 565 - y_offset - 20 * i - 63, str(round(final_total, 2)))
pdf.line(380, 565 - y_offset - 20 * i - 70, 556, 565 - y_offset - 20 * i - 70)

# Thank You Note
pdf.setFont("Helvetica", 13)
pdf.drawString(40, 505 - y_offset - 20 * i, "Thanks for visiting")

# Save PDF
pdf.save()

print("\n✅ Invoice generated: sample_invoice.pdf")
