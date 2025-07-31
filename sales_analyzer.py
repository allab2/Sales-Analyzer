# Project Structure
# csv-analyzer/
# ├── sales_data.csv         (Sample dataset you already have)
# ├── report.txt             (Generated output file)
# ├── analyzer.py            (Main script)
# └── README.md              (To be added when pushing to GitHub)

import csv
import os
from collections import Counter, defaultdict
from datetime import datetime

def analyze_sales_data(filename):
    total_records = 0
    total_revenue = 0.0
    product_sales = Counter()
    monthly_revenue = defaultdict(float)
    monthly_units = defaultdict(int)
    daily_orders = defaultdict(int)

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row["Product"]
            quantity = int(row["Quantity"])
            price = float(row["Price"])
            date_str = row["Date"]

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                continue  # skip bad date formats

            total_records += 1
            revenue = quantity * price
            total_revenue += revenue

            product_sales[product] += quantity
            month_key = date.strftime("%Y-%m")
            monthly_revenue[month_key] += revenue
            monthly_units[month_key] += quantity

            day_key = date.strftime("%Y-%m-%d")
            daily_orders[day_key] += 1

    top_products = product_sales.most_common(5)

    # Write report
    with open("sales_report.txt", "w") as report:
        report.write("------ Sales Metrics ------\n")
        report.write(f"Total Records: {total_records}\n")
        report.write(f"Total Revenue: ${total_revenue:.2f}\n\n")

        report.write("------ Top 5 Products by Quantity Sold ------\n")
        for product, qty in top_products:
            report.write(f"{product}: {qty} units\n")
        report.write("\n")

        report.write("------ Monthly Revenue and Units ------\n")
        for month in sorted(monthly_revenue):
            report.write(f"{month}: ${monthly_revenue[month]:.2f}, {monthly_units[month]} units\n")
        report.write("\n")

        report.write("------ Daily Order Count ------\n")
        for day in sorted(daily_orders):
            report.write(f"{day}: {daily_orders[day]} orders\n")

if __name__ == "__main__":
    file_path = "sales_data.csv"
    if os.path.exists(file_path):
        analyze_sales_data(file_path)
        print("Analysis complete. Report generated as 'report.txt'.")
    else:
        print("'sales_data.csv' not found.")
