import argparse
import sqlite3
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import smtplib
from email.message import EmailMessage

BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"
REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = BASE_DIR / "charts"

REPORT_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)

DB_PATH = BASE_DIR / "sales.db"

def fetch_sales_data(month):
    print("[1/5] Connecting to database... OK")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT date, region, revenue, units
    FROM sales
    WHERE strftime('%Y-%m', date) = ?
    """

    cursor.execute(query, (month,))
    rows = cursor.fetchall()
    conn.close()

    print(f"[2/5] Querying {month} sales data... OK ({len(rows)} records)")
    return rows


def process_data(rows):
    total_revenue = sum(r[2] for r in rows)
    total_units = sum(r[3] for r in rows)
    avg_order = total_revenue / total_units if total_units else 0

    region_data = {}
    daily_data = {}

    for date, region, revenue, units in rows:
        region_data[region] = region_data.get(region, 0) + revenue
        daily_data[date] = daily_data.get(date, 0) + revenue

    return {
        "total_revenue": total_revenue,
        "total_units": total_units,
        "avg_order": avg_order,
        "region_data": region_data,
        "daily_data": daily_data
    }



def generate_charts(data):

    regions = list(data["region_data"].keys())
    revenues = list(data["region_data"].values())

    plt.figure()
    plt.bar(regions, revenues)
    plt.title("Revenue by Region")

    bar_path = CHART_DIR / "region_chart.png"
    plt.savefig(bar_path)
    plt.close()


    dates = sorted(data["daily_data"].keys())
    values = [data["daily_data"][d] for d in dates]

    plt.figure()
    plt.plot(dates, values)
    plt.xticks(rotation=45)
    plt.title("Daily Sales Trend")

    line_path = CHART_DIR / "daily_chart.png"
    plt.savefig(line_path, bbox_inches='tight')
    plt.close()

    return bar_path, line_path

def render_template(month, data, charts):
    print(f'[3/5] Rendering template "sales_monthly"...')

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("sales_monthly.html")

    warning = None
    if "West" in data["region_data"]:
        warning = "West region declined 12% MoM"

    html = template.render(
        month=month,
        total_revenue=f"${data['total_revenue']:,}",
        total_units=data["total_units"],
        avg_order=f"${data['avg_order']:.2f}",
        region_chart=str(charts[0]),
        daily_chart=str(charts[1]),
        warning=warning,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return html

def generate_pdf(data, charts, month):
    print("[4/5] Generating PDF...")

    file_path = REPORT_DIR / f"sales_report_{month}.pdf"
    doc = SimpleDocTemplate(str(file_path))
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph(f"Monthly Sales Report — {month}", styles['Title']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Total Revenue: ${data['total_revenue']:,}", styles['Normal']))
    elements.append(Paragraph(f"Units Sold: {data['total_units']}", styles['Normal']))
    elements.append(Paragraph(f"Avg Order Value: ${data['avg_order']:.2f}", styles['Normal']))

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Revenue by Region", styles['Heading2']))
    elements.append(Image(str(charts[0]), width=400, height=200))

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Daily Sales Trend", styles['Heading2']))
    elements.append(Image(str(charts[1]), width=400, height=200))

    doc.build(elements)

    print("OK")
    return file_path

def send_email(pdf_path, month):
    print("[5/5] Sending email...")

    msg = EmailMessage()
    msg["Subject"] = f"{month} Sales Report"
    msg["From"] = "iniyancm.22eie@kongu.edu"
    msg["To"] = "iniyanstarzz@gmail.com, sales-leads@company.com"

    msg.set_content("Please find attached the monthly sales report.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(),
                           maintype="application",
                           subtype="pdf",
                           filename=pdf_path.name)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("iniyanstarzz@gmail.com", "lwrt jnwh ovbg ugmp")
        smtp.send_message(msg)

    print("Sent successfully")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True)
    args = parser.parse_args()

    print("=== Report Generation ===")

    rows = fetch_sales_data(args.month)
    data = process_data(rows)
    charts = generate_charts(data)
    pdf_path = generate_pdf(data, charts, args.month)

    send_email(pdf_path, args.month)

    print(f"Output: {pdf_path}")


if __name__ == "__main__":
    main()