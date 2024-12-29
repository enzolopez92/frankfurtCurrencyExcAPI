from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

@dataclass
class Currency:
    """Currency model."""
    code: str
    name: str

@dataclass
class ExchangeRate:
    """Exchange rate model."""
    base: str
    date: datetime
    rates: Dict[str, float]

@dataclass
class TimeSeries:
    """Time series model for exchange rates."""
    base: str
    start_date: datetime
    end_date: datetime
    rates: Dict[str, Dict[str, float]]
