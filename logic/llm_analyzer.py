from groq import Groq
from datetime import datetime

class CommodityAnalyzer:
    """Uses Groq AI to analyze commodity and stock investment opportunities"""
    
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        # Using the latest supported Groq model
        self.model = "llama-3.3-70b-versatile"  # Updated model
    
    def analyze_investment(self, symbol, data, question, investment_amount, asset_type="commodity"):
        """
        Analyze investment using Groq AI
        
        Args:
            symbol: Asset symbol
            data: pandas DataFrame with price data
            question: User's question about the investment
            investment_amount: Amount user wants to invest
            asset_type: "commodity" or "stock"
        
        Returns:
            String with investment analysis
        """
        try:
            # Prepare data summary
            summary = self._prepare_data_summary(symbol, data, investment_amount, asset_type)
            
            # Create prompt
            asset_name = "stock" if asset_type == "stock" else "commodity"
            prompt = f"""You are a financial analyst specializing in {asset_name} investments. 
Analyze the following {asset_name} data and answer the user's question.

{summary}

User's Question: {question}

Provide a comprehensive analysis that includes:
1. Whether this is a good investment opportunity (Yes/No/Maybe with reasoning)
2. Key risks and opportunities
3. Specific investment recommendation (how much to invest or if to avoid)
4. Time horizon considerations
5. Risk level (Low/Medium/High)

Be specific, data-driven, and practical. Format your response in a clear, structured way.
Remember: This is educational information, not financial advice. Users should consult financial advisors."""

            print(f"Calling Groq API with model: {self.model}")
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are a professional financial analyst specializing in {asset_name} markets and investment strategies."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            print("Groq API call successful")
            
            # Extract response
            response_text = response.choices[0].message.content
            
            return response_text
            
        except Exception as e:
            print(f"Error in analysis: {type(e).__name__}: {str(e)}")
            # Return the error message for debugging
            return f"Error during analysis: {type(e).__name__}: {str(e)}\n\nPlease check:\n1. Your Groq API key is correct\n2. You have API credits remaining\n3. Your internet connection is stable"
    
    # Keep the old method for backward compatibility
    def analyze_commodity(self, commodity, data, question, investment_amount):
        """Legacy method - calls analyze_investment"""
        return self.analyze_investment(commodity, data, question, investment_amount, "commodity")
    
    def _prepare_data_summary(self, symbol, data, investment_amount, asset_type="commodity"):
        """Prepare a summary of asset data for analysis"""
        
        if data is None or data.empty:
            return f"No data available for {symbol}"
        
        # Calculate statistics
        current_price = data['value'].iloc[-1]
        prev_price = data['value'].iloc[-2] if len(data) > 1 else current_price
        change = current_price - prev_price
        change_pct = (change / prev_price * 100) if prev_price != 0 else 0
        
        # Get recent prices (last 6 months)
        recent_prices = data['value'].tail(6).tolist()
        
        # Calculate volatility
        volatility = data['value'].std()
        avg_price = data['value'].mean()
        
        # Determine trend
        if len(data) >= 6:
            first_half = data['value'].tail(6).iloc[:3].mean()
            second_half = data['value'].tail(6).iloc[3:].mean()
            trend = "upward" if second_half > first_half * 1.05 else "downward" if second_half < first_half * 0.95 else "sideways"
        else:
            trend = "insufficient data"
        
        asset_name = "Stock" if asset_type == "stock" else "Commodity"
        
        summary = f"""
Asset Type: {asset_name}
Symbol: {symbol}
Investment Amount: ${investment_amount:,.2f}
Current Price: ${current_price:.2f}
Previous Price: ${prev_price:.2f}
Recent Change: ${change:.2f} ({change_pct:+.2f}%)
Average Price: ${avg_price:.2f}
Price Volatility (Std Dev): ${volatility:.2f}
Price Trend: {trend}
Recent Prices (Last 6 periods): {[f"${p:.2f}" for p in recent_prices]}
Data Points Available: {len(data)}
Latest Data Date: {data.index[-1].strftime('%Y-%m-%d')}
"""
        
        return summary
    
    def get_risk_assessment(self, commodity, data):
        """
        Quick risk assessment without full analysis
        
        Returns:
            String: "Low", "Medium", or "High"
        """
        if data is None or len(data) < 6:
            return "High"  # Insufficient data is risky
        
        # Calculate volatility ratio
        volatility = data['value'].std()
        avg_price = data['value'].mean()
        volatility_ratio = (volatility / avg_price * 100) if avg_price != 0 else 100
        
        if volatility_ratio < 10:
            return "Low"
        elif volatility_ratio < 20:
            return "Medium"
        else:
            return "High"