from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import qrcode


# For local testing:

BASE_URL = "http://10.81.176.124:5000"

def generate_bonafide(student):

    os.makedirs("certificates", exist_ok=True)

    usn = student["usn"]

    filename = f"certificates/bonafide_{usn}.pdf"

    # Certificate number
    certificate_number = f"BON-{datetime.now().year}-{usn}"

    # QR verification URL
    verify_url = f"{BASE_URL}/verify/{certificate_number}"

    # Create QR code
    qr = qrcode.make(verify_url)

    qr_filename = f"certificates/qr_{usn}.png"

    qr.save(qr_filename)

    # Create PDF
    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    # Border
    pdf.rect(40, 40, width - 80, height - 80)

    # College heading
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(
        width / 2,
        height - 90,
        "ABC COLLEGE OF ENGINEERING"
    )

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(
        width / 2,
        height - 110,
        "Belagavi, Karnataka"
    )

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(
        width / 2,
        height - 170,
        "BONAFIDE CERTIFICATE"
    )

    # Certificate number
    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        70,
        height - 210,
        f"Certificate No: {certificate_number}"
    )

    pdf.drawRightString(
        width - 70,
        height - 210,
        f"Date: {datetime.now().strftime('%d-%m-%Y')}"
    )

    # Certificate text
    pdf.setFont("Helvetica", 12)

    text = pdf.beginText()
    text.setTextOrigin(80, height - 280)
    text.setLeading(25)

    text.textLine(
        f"This is to certify that {student['name']}"
    )

    text.textLine(
        f"bearing USN {student['usn']} is a bonafide student"
    )

    text.textLine(
        f"of {student['course']} in the Department of "
        f"{student['department']}."
    )

    text.textLine(
        f"The student is currently studying in Semester "
        f"{student['semester']}."
    )

    text.textLine(
        f"Academic Year: {student['academic_year']}."
    )

    pdf.drawText(text)

    # QR code
    pdf.drawImage(
        qr_filename,
        width - 170,
        180,
        width=100,
        height=100
    )

    pdf.setFont("Helvetica", 9)

    pdf.drawCentredString(
        width - 120,
        165,
        "Scan to verify"
    )

    # Signature
    pdf.setFont("Helvetica-Bold", 11)

    pdf.drawString(
        70,
        130,
        "Date:"
    )

    pdf.drawRightString(
        width - 70,
        130,
        "Principal / Head of Department"
    )

    pdf.save()

    return filename