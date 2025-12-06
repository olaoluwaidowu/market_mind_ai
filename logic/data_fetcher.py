import requests
import pandas as pd
from datetime import datetime, timedelta

class CommodityDataFetcher:
    """Fetches commodity and stock data from Alpha Vantage API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        
        # Commodity symbol mapping
        self.commodity_map = {
            "WTI": "WTI",
            "BRENT": "BRENT",
            "NATURAL_GAS": "NATURAL_GAS",
            "COPPER": "COPPER",
            "ALUMINUM": "ALUMINUM",
            "WHEAT": "WHEAT",
            "CORN": "CORN",
            "SUGAR": "SUGAR",
            "COFFEE": "COFFEE"
        }
        
        # Stock symbols (popular stocks)
        self.stock_symbols = {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corp.",
            "GOOGL": "Alphabet Inc.",
            "AMZN": "Amazon.com Inc.",
            "TSLA": "Tesla Inc.",
            "META": "Meta Platforms Inc.",
            "NVDA": "NVIDIA Corp.",
            "JPM": "JPMorgan Chase",
            "V": "Visa Inc.",
            "WMT": "Walmart Inc."
        }
    
    def get_commodity_data(self, commodity, interval="monthly"):
        """
        Fetch commodity data from Alpha Vantage
        
        Args:
            commodity: Commodity symbol (e.g., "WTI", "COPPER")
            interval: Data interval - "monthly", "weekly", or "daily"
        
        Returns:
            pandas DataFrame with date index and commodity prices
        """
        try:
            # Map commodity to Alpha Vantage symbol
            symbol = self.commodity_map.get(commodity, commodity)
            
            params = {
                "function": symbol,
                "interval": interval,
                "apikey": self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if "Error Message" in data:
                print(f"API Error: {data['Error Message']}")
                return None
            
            if "Note" in data:
                print(f"API Note: {data['Note']}")
                return None
            
            # Extract data based on interval
            data_key = "data"
            if data_key not in data:
                print(f"Unexpected API response structure: {data.keys()}")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(data[data_key])
            
            if df.empty:
                print("No data returned from API")
                return None
            
            # Parse dates and set as index
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            df = df.sort_index()
            
            # Convert value to numeric
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            
            # Remove any rows with NaN values
            df = df.dropna()
            
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def get_stock_data(self, symbol):
        """
        Fetch stock data from Alpha Vantage
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "MSFT")
        
        Returns:
            pandas DataFrame with date index and stock prices
        """
        try:
            params = {
                "function": "TIME_SERIES_MONTHLY",
                "symbol": symbol,
                "apikey": self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if "Error Message" in data:
                print(f"API Error: {data['Error Message']}")
                return None
            
            if "Note" in data:
                print(f"API Note: {data['Note']}")
                return None
            
            # Extract time series data
            time_series_key = "Monthly Time Series"
            if time_series_key not in data:
                print(f"Unexpected API response structure: {data.keys()}")
                return None
            
            # Convert to DataFrame
            time_series = data[time_series_key]
            df = pd.DataFrame.from_dict(time_series, orient='index')
            
            if df.empty:
                print("No data returned from API")
                return None
            
            # Parse dates and set as index
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            # Use closing price as value
            df['value'] = pd.to_numeric(df['4. close'], errors='coerce')
            
            # Keep only the value column
            df = df[['value']]
            
            # Remove any rows with NaN values
            df = df.dropna()
            
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None
    
    def get_data(self, symbol, asset_type="commodity"):
        """
        Generic method to fetch data based on asset type
        
        Args:
            symbol: Symbol to fetch
            asset_type: "commodity" or "stock"
        
        Returns:
            pandas DataFrame with price data
        """
        if asset_type == "stock":
            return self.get_stock_data(symbol)
        else:
            return self.get_commodity_data(symbol)
    
    def get_price_statistics(self, data):
        """
        Calculate basic statistics from price data
        
        Args:
            data: pandas DataFrame with price data
        
        Returns:
            Dictionary with statistics
        """
        if data is None or data.empty:
            return None
        
        current_price = data['value'].iloc[-1]
        prev_price = data['value'].iloc[-2] if len(data) > 1 else current_price
        
        stats = {
            'current_price': current_price,
            'previous_price': prev_price,
            'change': current_price - prev_price,
            'change_percent': ((current_price - prev_price) / prev_price * 100) if prev_price != 0 else 0,
            'high_52w': data['value'].tail(12).max(),
            'low_52w': data['value'].tail(12).min(),
            'avg_price': data['value'].mean(),
            'volatility': data['value'].std(),
            'data_points': len(data)
        }
        
        return stats
    
    def get_trend(self, data, periods=6):
        """
        Determine price trend over specified periods
        
        Args:
            data: pandas DataFrame with price data
            periods: Number of periods to analyze
        
        Returns:
            String: "upward", "downward", or "sideways"
        """
        if data is None or len(data) < periods:
            return "insufficient_data"
        
        recent_data = data['value'].tail(periods)
        first_half = recent_data.iloc[:len(recent_data)//2].mean()
        second_half = recent_data.iloc[len(recent_data)//2:].mean()
        
        change_percent = ((second_half - first_half) / first_half * 100) if first_half != 0 else 0
        
        if change_percent > 5:
            return "upward"
        elif change_percent < -5:
            return "downward"
        else:
            return "sideways"