import os
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_qr_codes(start_value, end_value, qr_codes_per_page, file_name):
    qr_code_size = 80  # Size of each QR code image
    qr_margin = 15  # Margin between QR codes and page borders
    id_font_size = 13  # Font size for the ID text below the QR code
    page_width, page_height = letter  # Page size (letter size: 8.5 x 11 inches)
    qr_codes = []

    # Generate QR codes for each value in the specified range
    for value in range(start_value, end_value + 1):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(value))  # Add the value as the QR code data
        qr.make(fit=True)
        qr_codes.append((qr, value))

    # Create the PDF and start drawing QR codes and IDs
    pdf = canvas.Canvas(file_name, pagesize=letter)
    current_x, current_y = qr_margin, page_height - qr_margin

    current_row = 1

    # Loop through the QR codes and add them to the PDF
    for i, (qr, value) in enumerate(qr_codes, start=0):
        print(f"i: {i}")

        if i % qr_codes_per_page == 0 and i != 0:
            if current_row == 8:
                current_row = 1
                pdf.showPage()  # Start a new page for each set of QR codes
                current_x = qr_margin
                current_y = page_height - qr_margin
            else:
                current_row += 1
                current_x = qr_margin
                current_y -= qr_code_size + qr_margin

        img_path = f"temp_qr_{i}.png"
        qr.make_image(fill_color="black", back_color="white").save(img_path)

        # Draw the QR code image on the PDF
        pdf.drawImage(
            img_path,
            current_x,
            current_y - qr_code_size,
            width=qr_code_size,
            height=qr_code_size,
        )

        # Draw the ID text below the QR code
        pdf.setFont("Helvetica", id_font_size)
        pdf.drawString(current_x + 15, current_y - qr_code_size - 10, f"ID: {value}")

        current_x += qr_code_size + qr_margin

        os.remove(img_path)  # Remove the temporary QR code image

    pdf.save()  # Save the PDF file
    print(f"{len(qr_codes)} QR codes generated and saved to '{file_name}'.")


# Specify the range of values and other options
start_value = 1
end_value = 800
qr_codes_per_page = 6  # Number of QR codes per page
pdf_file_name = "generated_qr_codes.pdf"

generate_qr_codes(start_value, end_value, qr_codes_per_page, pdf_file_name)
