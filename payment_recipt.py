from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

def generate_invoice(data, filename="receipt.pdf"):
    pdf = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1

    title = Paragraph("Sumanth's Hotel", title_style)

    table_style = TableStyle(
        [("BOX", (0, 0), (-1, -1), 1, colors.black),
         ("GRID", (0, 0), (-1, -1), 1, colors.black),
         ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
         ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
         ("BACKGROUND", (0, 1), (-1, -1), colors.beige)]
    )

    table = Table(data, style=table_style)

    gst_block = Paragraph("GST Number: 12ABCDE3456F1Z5<br/>", styles['Normal'])
    signature_block = Paragraph("<br/><br/><br/><br/>Signature: ___________________________<br/><br/>", styles['Normal'])
    spacer = Spacer(1, 20)

    pdf.build([
        title,
        Spacer(1, 20),
        table,
        spacer,
        gst_block,
        Spacer(1, 20),
        signature_block,
        Spacer(1, 20)
    ])

def calculate_totals(data):
    subtotal = 0
    for row in data[1:]:
        try:
            price = float(row[-1].replace(',', '').replace('Rs.', '').replace('/', ''))
            subtotal += price
        except ValueError:
            pass

    gst_rate = 0.039
    gst_amount = subtotal * gst_rate
    total = subtotal + gst_amount
    return subtotal, gst_amount, total

if __name__ == "__main__":
    data = []
    data.append(["Date", "Item Name", "Count", "Price (Rs.)", "Total Price (Rs.)"])

    while True:
        date = input("Enter Date (dd/mm/yyyy): ")
        item_name = input("Enter Item Name: ")
        count = int(input("Enter Count: "))
        price = float(input("Enter Price per Item (Rs.): "))
        total_price = count * price

        data.append([date, item_name, count, f"{price:.2f}", f"{total_price:.2f}"])

        more = input("Add more items? (y/n): ").strip().lower()
        if more != 'y':
            break

    subtotal, gst_amount, total = calculate_totals(data)

    data.append(["Sub Total", "", "", "", f"{subtotal:.2f}"])
    data.append(["Discount", "", "", "", "0.00"])  # Assuming no discount, update as needed
    data.append(["GST (3.9%)", "", "", "", f"{gst_amount:.2f}"])
    data.append(["Total", "", "", "", f"{total:.2f}"])

    generate_invoice(data)
    print("Invoice generated successfully as 'receipt.pdf'")
