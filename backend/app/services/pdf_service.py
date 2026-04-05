import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

# Colors
NAVY = colors.HexColor('#1B2A4A')
LIGHT_BLUE = colors.HexColor('#DBEAFE')
WHITE = colors.white
DARK = colors.HexColor('#111827')

def generate_invoice_pdf(billing: dict, parcel: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', fontSize=18, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('Sub', fontSize=10, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica')
    label_style = ParagraphStyle('Label', fontSize=10, textColor=DARK, fontName='Helvetica-Bold')
    value_style = ParagraphStyle('Value', fontSize=10, textColor=DARK, fontName='Helvetica')

    elements = []

    # Header table (navy background)
    header_data = [
        [Paragraph("🚚 SMART LOGISTICS MANAGEMENT SYSTEM", title_style)],
        [Paragraph("INVOICE", subtitle_style)],
    ]
    header_table = Table(header_data, colWidths=[17*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [NAVY, NAVY]),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))

    # Invoice meta
    meta_data = [
        ['Invoice No:', billing.get('invoice_number', 'N/A'), 'Date:', datetime.now().strftime('%d %B %Y')],
        ['Tracking ID:', parcel.get('tracking_id', 'N/A'), 'Status:', billing.get('payment_status', 'Unpaid')],
    ]
    meta_table = Table(meta_data, colWidths=[4*cm, 5*cm, 3*cm, 5*cm])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [LIGHT_BLUE, WHITE]),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 0.5*cm))

    # Sender / Receiver
    sr_data = [
        ['SENDER', 'RECEIVER'],
        [parcel.get('sender_name', 'N/A'), parcel.get('receiver_name', 'N/A')],
        [parcel.get('sender_phone', ''), parcel.get('receiver_phone', '')],
        ['', parcel.get('receiver_address', '')],
    ]
    sr_table = Table(sr_data, colWidths=[8.5*cm, 8.5*cm])
    sr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BLUE]),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ]))
    elements.append(sr_table)
    elements.append(Spacer(1, 0.5*cm))

    # Parcel details
    parcel_data = [
        ['PARCEL DETAILS', '', ''],
        ['Weight', 'Type', 'Description'],
        [f"{parcel.get('weight', 0)} kg", parcel.get('parcel_type', 'N/A'), parcel.get('description', 'N/A')],
    ]
    parcel_table = Table(parcel_data, colWidths=[4*cm, 4*cm, 9*cm])
    parcel_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BLUE),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ]))
    elements.append(parcel_table)
    elements.append(Spacer(1, 0.5*cm))

    # Amount section
    amount_data = [
        ['AMOUNT PAYABLE', f"₹ {billing.get('amount', 0):.2f}"],
        ['Payment Status', billing.get('payment_status', 'Unpaid')],
    ]
    if billing.get('paid_at'):
        amount_data.append(['Paid On', str(billing.get('paid_at', ''))[:10]])

    amount_table = Table(amount_data, colWidths=[8.5*cm, 8.5*cm])
    amount_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (0, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_BLUE, WHITE]),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(amount_table)
    elements.append(Spacer(1, 1*cm))

    # Footer
    footer_data = [['Thank you for using Smart Logistics Management System! 🚚']]
    footer_table = Table(footer_data, colWidths=[17*cm])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, -1), WHITE),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(footer_table)

    doc.build(elements)
    return buffer.getvalue()
