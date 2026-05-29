import csv
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY"
)

total_revenue = 0
product_count = 0
best_quantity = 0
best_product = ""

with open("sales.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        quantity = int(row["quantity"])
        price = float(row["price"])
        
        revenue = quantity * price
        total_revenue += revenue
        product_count += 1
        
        if quantity > best_quantity:
            best_quantity = quantity
            best_product = row["product"]

average_revenue = total_revenue / product_count if product_count > 0 else 0

report_text = f"""Sales Report

Total Revenue: ${total_revenue:.2f}
Average Revenue Per Product: ${average_revenue:.2f}
Best Selling Product: {best_product}
Units Sold: {best_quantity}"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": f"""
Analyze the following sales report.

Provide:
- Key insights
- Business recommendations
- Performance observations

Sales Report:
{report_text}
"""
        }
    ]
)

ai_insights = response.choices[0].message.content

final_report = f"""
{report_text}

AI Insights
===========

{ai_insights}
"""

with open("business_report.txt", "w", encoding="utf-8") as file:
    file.write(final_report)
