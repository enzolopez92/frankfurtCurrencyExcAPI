from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd
from ..api.client import ForexAPIClient
from ..models.currency import ExchangeRate, TimeSeries, Currency
from ..config import Config

class ExchangeService:
    """Service for currency exchange operations."""
    
    def __init__(self, client: ForexAPIClient):
        self.client = client
        self._currencies_cache = {}
        self._last_cache_update = None

    def get_currencies(self) -> Dict[str, Currency]:
        """Get available currencies with caching."""
        if (not self._currencies_cache or 
            not self._last_cache_update or 
            datetime.now() - self._last_cache_update > timedelta(seconds=Config.CACHE_EXPIRY)):
            
            currencies_data = self.client.get_currencies()
            self._currencies_cache = {
                code: Currency(code=code, name=name)
                for code, name in currencies_data.items()
            }
            self._last_cache_update = datetime.now()
        
        return self._currencies_cache

    def convert_currency(self, amount: float, from_currency: str, 
                        to_currency: str) -> float:
        """Convert amount between currencies using latest rates."""
        rates = self.client.get_latest_rates(
            base=from_currency, 
            symbols=[to_currency]
        )
        return amount * rates['rates'][to_currency]

    def get_rate_trends(self, base: str, symbols: List[str], 
                       days: int = 30) -> pd.DataFrame:
        """Analyze rate trends over specified period."""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        data = self.client.get_time_series(
            start_date=start_date,
            end_date=end_date,
            base=base,
            symbols=symbols
        )
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame.from_dict(data['rates'], orient='index')
        df.index = pd.to_datetime(df.index)
        return df
