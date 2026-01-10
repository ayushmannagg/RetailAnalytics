from pydantic import BaseModel
from datetime import datetime

# What the API returns for a single sale row
class SaleResponse(BaseModel):
    id: int
    date: datetime
    sales_type: str
    customer_name: str
    item_details: str
    unit: str
    quantity: float
    rate: float
    amount: float

    class Config:
        from_attributes = True

# Forecast Response (Stays the same)
class ForecastResponse(BaseModel):
    next_month_prediction: float
    trend_direction: str