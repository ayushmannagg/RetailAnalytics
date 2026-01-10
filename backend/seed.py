import pandas as pd
import os
import re
from datetime import datetime
from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Sale

# 1. Helper function to clean money strings (e.g. "1,200.00" -> 1200.0)
def clean_currency(value):
    if pd.isna(value):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    
    # Remove commas and spaces
    clean_str = str(value).replace(',', '').replace(' ', '')
    try:
        return float(clean_str)
    except ValueError:
        return 0.0

def seed_data():
    create_db_and_tables()
    
    with Session(engine) as session:
        if session.exec(select(Sale)).first():
            print("⚠️  Clearing old data from database...")
            session.exec("DELETE FROM sale")
            session.commit()

        print("Reading SalesRegister_cleaned.csv...")
        
        csv_path = r"C:\Winter_2025-26_Projects\project-1\RetailAnalytics\data\SalesRegister_cleaned.csv"
        
        if not os.path.exists(csv_path):
            print(f"❌ Error: File not found at {csv_path}")
            return

        try:
            df = pd.read_csv(csv_path)
            
            print(f"Columns found: {list(df.columns)}")
            
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return

        print(f"Processing {len(df)} rows...")
        sales_objects = []
        
        for _, row in df.iterrows():
            try:
                date_val = pd.to_datetime(row['Date'], dayfirst=True) #for indian date system
            except:
                print(f"⚠️ Warning: Could not parse date: {row['Date']}")
                date_val = datetime.utcnow()
            
            # 6. Clean Numbers
            qty = clean_currency(row['Quantity'])
            rate = clean_currency(row['Rate'])
            amt = clean_currency(row['Amount'])

            # 7. Create Database Object
            sale = Sale(
                date=date_val,
                sales_type=str(row['Sales Type']),
                customer_name=str(row['Customer Name']),
                item_details=str(row['Item Details']),
                quantity=qty,
                unit=str(row['Unit']),
                rate=rate,
                amount=amt
            )
            sales_objects.append(sale)
        
        # 8. Save to DB
        session.add_all(sales_objects)
        session.commit()
        print(f"✅ Success! {len(sales_objects)} records inserted into database.")

if __name__ == "__main__":
    seed_data()