from sqlmodel import Session, select
from database import engine
from models import Sale
from sqlalchemy import func

def check_dates():
    with Session(engine) as session:
        # Get the earliest and latest date
        min_date = session.exec(select(func.min(Sale.date))).one()
        max_date = session.exec(select(func.max(Sale.date))).one()
        
        # Count total rows
        count = session.exec(select(func.count(Sale.id))).one()
        
        # Count DISTINCT months (The most important metric)
        # We group by Year-Month to see how many unique months exist
        unique_dates = session.exec(select(Sale.date)).all()
        unique_months = set(d.strftime('%Y-%m') for d in unique_dates)

        print("\n--- DATABASE DIAGNOSTIC REPORT ---")
        print(f"Total Sales Rows:   {count}")
        print(f"Earliest Date:      {min_date}")
        print(f"Latest Date:        {max_date}")
        print(f"Unique Months:      {len(unique_months)}")
        print(f"Months Found:       {sorted(list(unique_months))}")
        print("----------------------------------\n")

        if len(unique_months) < 5:
            print("❌ FAILURE: Database has less than 5 months of data.")
            print("   The CSV dates were likely not parsed correctly.")
        else:
            print("✅ SUCCESS: Database has enough history.")

if __name__ == "__main__":
    check_dates()