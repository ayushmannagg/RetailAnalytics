from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from database import get_session
from models import Sale
from schemas import SaleResponse, ForecastResponse

router = APIRouter(prefix="/sales", tags=["Sales"])

# 1. Get Unique Items
@router.get("/items", response_model=List[str])
def get_items(session: Session = Depends(get_session)):
    statement = select(Sale.item_details).distinct()
    results = session.exec(statement).all()
    # clean out None or empty strings
    return [r for r in results if r and str(r).strip() != '']

# 2. Get All Sales
@router.get("/", response_model=List[SaleResponse])
def read_sales(
    item: Optional[str] = None,
    limit: int = 100, 
    session: Session = Depends(get_session)
):
    query = select(Sale)
    if item:
        query = query.where(Sale.item_details == item)
    query = query.order_by(Sale.date.desc()).limit(limit)
    return session.exec(query).all()

# 3. FORECAST ENDPOINT (Debugged & Fixed)
@router.get("/forecast", response_model=ForecastResponse)
def get_sales_forecast(
    item: Optional[str] = None,
    session: Session = Depends(get_session)
):
    print(f"\n🔮 Forecasting Request for: {item if item else 'ALL ITEMS'}")

    # --- A. Fetch Data ---
    query = select(Sale.date, Sale.amount)
    if item:
        query = query.where(Sale.item_details == item)
        
    results = session.exec(query).all()
    
    if not results:
        print("❌ No data found in database for this selection.")
        # Return 0 instead of 404 to keep Frontend alive
        return {"next_month_prediction": 0, "trend_direction": "No Data"}

    # --- B. Prepare DataFrame ---
    df = pd.DataFrame(results, columns=['date', 'amount'])
    df['date'] = pd.to_datetime(df['date'])

    # Group by Month
    # Note: 'ME' is Month End. If this fails on older pandas, use 'M'
    try:
        monthly_sales = df.groupby(pd.Grouper(key='date', freq='ME')).sum().reset_index()
    except:
        monthly_sales = df.groupby(pd.Grouper(key='date', freq='M')).sum().reset_index()

    print(f"✅ Found {len(monthly_sales)} distinct months of history.")

    # --- C. Safety Check ---
    # We lowered the requirement to 2 months. 
    # (Random Forest technically runs on 2 points, though 10 is better).
    if len(monthly_sales) < 2:
        print("⚠️ Not enough history for AI. Returning simple average.")
        avg_val = monthly_sales['amount'].mean()
        return {"next_month_prediction": round(avg_val, 2), "trend_direction": "Stable"}

    # --- D. Feature Engineering ---
    monthly_sales['month'] = monthly_sales['date'].dt.month
    monthly_sales['quarter'] = monthly_sales['date'].dt.quarter
    monthly_sales['year'] = monthly_sales['date'].dt.year
    monthly_sales['lag_1'] = monthly_sales['amount'].shift(1)
    
    model_data = monthly_sales.dropna()

    # --- E. Train Random Forest ---
    X = model_data[['month', 'quarter', 'year', 'lag_1']]
    y = model_data['amount']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # --- F. Predict Next Month ---
    last_row = monthly_sales.iloc[-1]
    next_date = last_row['date'] + pd.DateOffset(months=1)
    
    next_input = pd.DataFrame([{
        'month': next_date.month,
        'quarter': next_date.quarter,
        'year': next_date.year,
        'lag_1': last_row['amount']
    }])
    
    prediction = model.predict(next_input)[0]
    
    # Trend Logic
    recent_avg = monthly_sales['amount'].tail(3).mean()
    trend = "Up" if prediction > recent_avg else "Down"
    
    print(f"🚀 Prediction: {prediction}")
    
    return {
        "next_month_prediction": round(prediction, 2),
        "trend_direction": trend
    }