import requests
from datetime import datetime
from typing import Dict, List, Optional, Union
from ..config import Config

class APIError(Exception):
    """Custom exception for API-related errors."""
    pass

class ForexAPIClient:
    """Client for interacting with the Forex API."""
    
    def __init__(self, base_url: str = Config.API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request to the API with error handling."""
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=Config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {str(e)}")

    def get_latest_rates(self, base: str = None, symbols: List[str] = None) -> Dict:
        """Fetch latest exchange rates."""
        params = {}
        if base:
            params['base'] = base
        if symbols:
            params['symbols'] = ','.join(symbols)
        return self._make_request('latest', params)

    def get_historical_rates(self, date: str, base: str = None, 
                           symbols: List[str] = None) -> Dict:
        """Fetch historical exchange rates for a specific date."""
        params = {}
        if base:
            params['base'] = base
        if symbols:
            params['symbols'] = ','.join(symbols)
        return self._make_request(date, params)

    def get_time_series(self, start_date: str, end_date: str = None, 
                       base: str = None, symbols: List[str] = None) -> Dict:
        """Fetch exchange rates for a time period."""
        endpoint = f"{start_date}..{end_date if end_date else ''}"
        params = {}
        if base:
            params['base'] = base
        if symbols:
            params['symbols'] = ','.join(symbols)
        return self._make_request(endpoint, params)

    def get_currencies(self) -> Dict:
        """Fetch available currencies."""
        return self._make_request('currencies')
