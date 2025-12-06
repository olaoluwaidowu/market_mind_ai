# Commodity Investment Advisor - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Installation Guide](#installation-guide)
6. [Usage Guide](#usage-guide)
7. [API Documentation](#api-documentation)
8. [Code Structure](#code-structure)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Future Enhancements](#future-enhancements)
12. [Troubleshooting](#troubleshooting)
13. [Contributing](#contributing)
14. [License](#license)

---

## Project Overview

### Description
The **Commodity Investment Advisor** is an AI-powered financial market intelligence platform that provides personalized investment analysis for commodities and stocks. It combines real-time market data from Alpha Vantage with advanced AI analysis from Groq to deliver actionable investment recommendations.

### Problem Statement
Individual investors face significant challenges when making investment decisions:
- Market data is overwhelming and difficult to interpret
- Professional financial advice is expensive ($100-300/hour)
- Manual analysis is time-consuming and requires expertise
- Most platforms focus only on stocks, ignoring commodities

### Solution
Our platform democratizes financial intelligence by:
- Providing free, AI-powered investment analysis
- Supporting both commodities and stocks
- Offering personalized recommendations based on user goals
- Delivering insights through an intuitive web interface

### Target Users
- Retail investors seeking data-driven investment decisions
- Students learning about financial markets
- Small business owners hedging against price risks
- Financial educators demonstrating market analysis

---

## Features

### Core Features
1. **Multi-Asset Support**
   - Commodities: WTI, Brent, Natural Gas, Copper, Aluminum, Wheat, Corn, Sugar, Coffee
   - Stocks: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, JPM, V, WMT

2. **Real-Time Data Analysis**
   - Historical price data from Alpha Vantage API
   - Monthly price trends and patterns
   - Volatility calculations
   - Price change metrics

3. **AI-Powered Recommendations**
   - Investment opportunity assessment (Yes/No/Maybe)
   - Risk level analysis (Low/Medium/High)
   - Specific allocation recommendations
   - Time horizon considerations
   - Key risks and opportunities identification

4. **Interactive Visualizations**
   - Historical price charts with Plotly
   - Trend indicators
   - Hover-over data points for detailed information

5. **Analysis History**
   - Track past queries
   - Compare different investments
   - Review previous recommendations

### Technical Features
- Responsive web interface
- Real-time API integration
- Error handling and validation
- Secure API key management
- Session-based data storage

---

## Technology Stack

### Frontend
- **Streamlit** (v1.31.0): Web application framework
- **Plotly** (v5.18.0): Interactive data visualization

### Backend
- **Python** (3.11+): Core programming language
- **Pandas** (v2.1.4): Data manipulation and analysis
- **Requests** (v2.31.0): HTTP library for API calls

### AI/ML
- **Groq API**: AI inference platform
- **Llama 3.3 70B**: Large language model for analysis

### Data Source
- **Alpha Vantage API**: Real-time and historical market data

### Deployment
- **Streamlit Community Cloud**: Free hosting platform
- **GitHub**: Version control and code repository

### Development Tools
- **Git**: Version control
- **Python Virtual Environment**: Dependency isolation
- **python-dotenv**: Environment variable management

---

## System Architecture

### High-Level Architecture

```
┌─────────────┐
│   User      │
│  Browser    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│    Streamlit Frontend (app.py)      │
│  - User Interface                   │
│  - Input Validation                 │
│  - Visualization                    │
└──────┬──────────────────┬───────────┘
       │                  │
       ▼                  ▼
┌─────────────────┐  ┌──────────────────┐
│ Data Fetcher    │  │  LLM Analyzer    │
│ (data_fetcher)  │  │ (llm_analyzer)   │
│                 │  │                  │
│ - API calls     │  │ - AI prompts     │
│ - Data parsing  │  │ - Analysis       │
│ - Statistics    │  │ - Formatting     │
└────────┬────────┘  └────────┬─────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌──────────────────┐
│ Alpha Vantage   │  │   Groq API       │
│      API        │  │  (Llama 3.3)     │
└─────────────────┘  └──────────────────┘
```

### Data Flow

1. **User Input** → User selects asset and enters question
2. **Data Fetching** → `data_fetcher.py` retrieves market data from Alpha Vantage
3. **Data Processing** → Calculate statistics (volatility, trends, changes)
4. **AI Analysis** → `llm_analyzer.py` sends data to Groq for analysis
5. **Result Rendering** → Streamlit displays chart and AI recommendations
6. **History Storage** → Save analysis in session state

### Component Interaction

```python
# Simplified flow
user_input = get_user_selection()
↓
market_data = data_fetcher.get_data(symbol)
↓
statistics = calculate_statistics(market_data)
↓
ai_analysis = llm_analyzer.analyze(market_data, user_question)
↓
display_results(chart, ai_analysis)
```

---

## Installation Guide

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git (for cloning repository)
- Alpha Vantage API key (free)
- Groq API key (free)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/commodity-advisor.git
cd commodity-advisor
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Get API Keys

**Alpha Vantage:**
1. Visit https://www.alphavantage.co/support/#api-key
2. Enter your email
3. Copy the API key

**Groq:**
1. Visit https://console.groq.com/
2. Sign up (free)
3. Go to API Keys section
4. Create new key

#### 5. Configure Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit .env file and add your keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
GROQ_API_KEY=your_groq_key
```

#### 6. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Verification
Test the installation:
1. App loads without errors
2. Select "Copper" commodity
3. Enter investment amount: $10,000
4. Ask: "Should I invest?"
5. Click "Analyze Investment"
6. You should see a price chart and AI analysis

---

## Usage Guide

### Basic Workflow

#### Step 1: Enter API Keys
1. Look at the sidebar on the left
2. Enter your Alpha Vantage API key
3. Enter your Groq API key
4. Keys are stored for the session only

#### Step 2: Select Asset Type
Choose between:
- **Commodity**: Raw materials like oil, metals, agriculture
- **Stock**: Company shares

#### Step 3: Choose Specific Asset
- For commodities: WTI, Copper, Wheat, etc.
- For stocks: AAPL, MSFT, TSLA, etc.

#### Step 4: Set Investment Amount
Enter the amount you're considering investing ($1,000 - $1,000,000)

#### Step 5: Ask Your Question
Examples:
- "Should I invest in this commodity right now?"
- "What are the main risks of investing in copper?"
- "How much should I allocate to this stock?"
- "Is this a good long-term investment?"

#### Step 6: Analyze
Click the "🔍 Analyze Investment" button

#### Step 7: Review Results
You'll see:
1. **Price Chart**: Historical prices with trends
2. **AI Analysis**: Detailed investment recommendation including:
   - Investment opportunity assessment
   - Risk analysis
   - Specific recommendations
   - Time horizon
   - Key considerations

### Advanced Usage

#### Comparing Investments
1. Analyze first asset (e.g., Gold)
2. Note the recommendation
3. Switch to second asset (e.g., Silver)
4. Analyze and compare
5. Check Analysis History at bottom

#### Understanding Risk Levels
- **Low Risk**: Stable prices, low volatility
- **Medium Risk**: Moderate price swings
- **High Risk**: Volatile, unpredictable movements

#### Best Practices
- ✅ Ask specific questions
- ✅ Consider multiple commodities/stocks
- ✅ Check historical trends on the chart
- ✅ Review analysis history
- ❌ Don't rely solely on AI recommendations
- ❌ Don't invest more than you can afford to lose

---

## API Documentation

### Alpha Vantage Integration

#### Commodity Data
```python
# Endpoint
GET https://www.alphavantage.co/query

# Parameters
function: COMMODITY_NAME (e.g., "WTI", "COPPER")
interval: "monthly"
apikey: YOUR_API_KEY

# Response Format
{
  "data": [
    {
      "date": "2024-12-01",
      "value": "73.45"
    },
    ...
  ]
}
```

#### Stock Data
```python
# Endpoint
GET https://www.alphavantage.co/query

# Parameters
function: "TIME_SERIES_MONTHLY"
symbol: STOCK_SYMBOL (e.g., "AAPL")
apikey: YOUR_API_KEY

# Response Format
{
  "Monthly Time Series": {
    "2024-12-01": {
      "1. open": "150.00",
      "2. high": "155.00",
      "3. low": "148.00",
      "4. close": "152.50",
      "5. volume": "50000000"
    },
    ...
  }
}
```

### Groq AI Integration

#### Chat Completion
```python
# Endpoint
POST https://api.groq.com/openai/v1/chat/completions

# Request Body
{
  "model": "llama-3.3-70b-versatile",
  "messages": [
    {
      "role": "system",
      "content": "You are a financial analyst..."
    },
    {
      "role": "user",
      "content": "Analyze this data..."
    }
  ],
  "max_tokens": 1500,
  "temperature": 0.7
}

# Response Format
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Based on the analysis..."
      }
    }
  ]
}
```

### Rate Limits

**Alpha Vantage (Free Tier):**
- 25 requests per day
- 5 requests per minute

**Groq (Free Tier):**
- 14,400 requests per day
- 30 requests per minute
- 6,000 tokens per minute

---

## Code Structure

### File Organization

```
commodity-advisor/
├── app.py                 # Main Streamlit application
├── data_fetcher.py        # Alpha Vantage API integration
├── llm_analyzer.py        # Groq AI analysis
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

### app.py - Main Application

**Purpose**: Streamlit frontend and user interface

**Key Functions**:
- `main()`: Application entry point
- User input handling
- Chart visualization with Plotly
- Session state management
- Analysis history display

**Structure**:
```python
# Configuration
st.set_page_config(...)

# Sidebar - API Keys
with st.sidebar:
    alpha_vantage_key = st.text_input(...)
    groq_key = st.text_input(...)

# Main content
asset_type = st.selectbox(...)
asset = st.selectbox(...)
question = st.text_area(...)

# Analysis
if st.button("Analyze"):
    # Fetch data
    data = fetcher.get_data(...)
    
    # Display chart
    st.plotly_chart(fig)
    
    # Get AI analysis
    analysis = analyzer.analyze_investment(...)
    
    # Display results
    st.markdown(analysis)
```

### data_fetcher.py - Data Retrieval

**Purpose**: Fetch and process market data from Alpha Vantage

**Classes**:
- `CommodityDataFetcher`: Main data fetching class

**Key Methods**:

```python
class CommodityDataFetcher:
    def __init__(self, api_key):
        """Initialize with API key"""
        
    def get_commodity_data(self, commodity, interval="monthly"):
        """Fetch commodity price data"""
        # Returns: pandas DataFrame
        
    def get_stock_data(self, symbol):
        """Fetch stock price data"""
        # Returns: pandas DataFrame
        
    def get_price_statistics(self, data):
        """Calculate price statistics"""
        # Returns: dict with stats
        
    def get_trend(self, data, periods=6):
        """Determine price trend"""
        # Returns: "upward", "downward", or "sideways"
```

**Data Processing Flow**:
1. Make API request to Alpha Vantage
2. Parse JSON response
3. Convert to pandas DataFrame
4. Set date as index
5. Convert prices to numeric
6. Remove invalid data
7. Return cleaned DataFrame

### llm_analyzer.py - AI Analysis

**Purpose**: Generate investment analysis using Groq AI

**Classes**:
- `CommodityAnalyzer`: AI analysis class

**Key Methods**:

```python
class CommodityAnalyzer:
    def __init__(self, api_key):
        """Initialize with Groq API key"""
        
    def analyze_investment(self, symbol, data, question, 
                          investment_amount, asset_type):
        """Generate investment analysis"""
        # Returns: str (AI analysis)
        
    def _prepare_data_summary(self, symbol, data, 
                              investment_amount, asset_type):
        """Prepare data summary for AI"""
        # Returns: str (formatted summary)
        
    def get_risk_assessment(self, commodity, data):
        """Quick risk assessment"""
        # Returns: "Low", "Medium", or "High"
```

**Analysis Flow**:
1. Prepare data summary with statistics
2. Create prompt with context
3. Call Groq API with Llama 3.3
4. Parse AI response
5. Return formatted analysis

---

## Testing

### Manual Testing Checklist

#### Functionality Tests
- [ ] App loads successfully
- [ ] API keys can be entered
- [ ] All commodities can be selected
- [ ] All stocks can be selected
- [ ] Investment amount accepts valid values
- [ ] Question text area works
- [ ] Analyze button triggers analysis
- [ ] Price chart displays correctly
- [ ] AI analysis appears
- [ ] Analysis history stores queries

#### Data Validation Tests
- [ ] Invalid API keys show error
- [ ] Empty question shows error
- [ ] Invalid commodity symbol handled
- [ ] API rate limits handled gracefully
- [ ] Network errors caught and displayed

#### Edge Cases
- [ ] Very large investment amounts
- [ ] Very small investment amounts
- [ ] Long questions (>500 characters)
- [ ] Special characters in questions
- [ ] Rapid successive queries

### Sample Test Cases

#### Test Case 1: Basic Commodity Analysis
```
Input:
- Asset Type: Commodity
- Commodity: WTI
- Amount: $10,000
- Question: "Should I invest?"

Expected Output:
- Price chart displays
- AI provides Yes/No/Maybe recommendation
- Risk level stated
- Investment suggestion given
```

#### Test Case 2: Stock Analysis
```
Input:
- Asset Type: Stock
- Stock: AAPL
- Amount: $5,000
- Question: "What are the risks?"

Expected Output:
- Stock price chart displays
- AI lists specific risks
- Provides context on Apple's market position
```

#### Test Case 3: Invalid API Key
```
Input:
- Invalid Groq API key
- Valid inputs otherwise

Expected Output:
- Error message displayed
- No crash
- User can correct and retry
```

### Automated Testing (Future)

```python
# Example unit test structure
import unittest
from data_fetcher import CommodityDataFetcher

class TestDataFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = CommodityDataFetcher("test_key")
        
    def test_get_commodity_data(self):
        data = self.fetcher.get_commodity_data("WTI")
        self.assertIsNotNone(data)
        self.assertIn('value', data.columns)
        
    def test_get_price_statistics(self):
        # Mock data
        stats = self.fetcher.get_price_statistics(mock_data)
        self.assertIn('current_price', stats)
        self.assertIn('volatility', stats)
```

---

## Deployment

### Streamlit Community Cloud Deployment

#### Prerequisites
- GitHub account
- Code pushed to GitHub repository
- Alpha Vantage API key
- Groq API key

#### Step-by-Step Deployment

**1. Prepare Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

**2. Deploy on Streamlit Cloud**

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Choose branch: `main`
6. Set main file path: `app.py`
7. Click "Deploy"

**3. Add Secrets**

In the Streamlit Cloud dashboard:
1. Click on your app
2. Go to "Settings" → "Secrets"
3. Add in TOML format:

```toml
ALPHA_VANTAGE_API_KEY = "your_key_here"
GROQ_API_KEY = "your_key_here"
```

4. Save

**4. Verify Deployment**

- App URL: `https://your-app-name.streamlit.app`
- Test all features
- Check logs for errors

#### Deployment Configuration

**streamlit/config.toml** (optional):
```toml
[theme]
primaryColor = "#3b82f6"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
```

### Alternative Deployment Options


```

---

## Disclaimer

**⚠️ IMPORTANT DISCLAIMER**

This application is provided for **educational and informational purposes only**. It does not constitute financial advice, investment advice, trading advice, or any other sort of advice.

**Key Points:**

1. **Not Financial Advice**: The analysis and recommendations provided by this application should not be considered as professional financial advice.

2. **No Guarantees**: Past performance does not guarantee future results. Investment values can go down as well as up.

3. **Do Your Own Research**: Always conduct your own research and consult with a qualified financial advisor before making investment decisions.

4. **Risk Warning**: Investing in commodities and stocks involves substantial risk of loss. You should only invest money you can afford to lose.

5. **AI Limitations**: The AI analysis is based on historical data and may not account for sudden market changes, geopolitical events, or other unforeseen circumstances.

6. **No Liability**: The developers and contributors of this application are not liable for any financial losses incurred through use of this application.

7. **User Responsibility**: You are solely responsible for your investment decisions and their consequences.

**By using this application, you acknowledge that you understand and accept these terms.**

---

## Contact and Support

### Get Help

- **Documentation**: See this file
- **Issues**: Create an issue on GitHub
- **Email**: your.email@example.com
- **Discord**: [Your Discord Server] (optional)


