from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    date: datetime
    
    sales_type: str        # 'Sales Type'
    customer_name: str     # 'Customer Name'
    item_details: str      # 'Item Details'
    unit: str              # 'Unit'
    
    quantity: float        # 'Quantity'
    rate: float            # 'Rate' (Converted from Object/String)
    amount: float          # 'Amount' (Converted from Object/String)