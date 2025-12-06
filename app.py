import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from logic.data_fetcher import CommodityDataFetcher
from logic.llm_analyzer import CommodityAnalyzer
import os

# Page config
st.set_page_config(
    page_title="Commodity Investment Advisor",
    page_icon="📈",
    layout="wide"
)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Header
st.title("📈 Commodity Investment Advisor")
st.subheader("AI-Powered Risk Assessment & Portfolio Optimization")
st.divider()

# Sidebar for API keys
with st.sidebar:
    st.header("⚙️ Configuration")
    
    alpha_vantage_key = st.text_input(
        "Alpha Vantage API Key",
        type="password",
        value=os.getenv("ALPHA_VANTAGE_API_KEY", ""),
        help="Get your free API key from https://www.alphavantage.co/support/#api-key"
    )
    
    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Get your FREE API key from https://console.groq.com/keys"
    )
    
    st.divider()
    
    st.header("📊 Supported Assets")
    st.markdown("""
    **Commodities:**
    - Energy: WTI, Brent, Natural Gas
    - Metals: Copper, Aluminum
    - Agriculture: Wheat, Corn, Coffee, Sugar
    
    **Stocks:**
    - Tech: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA
    - Finance: JPM, V
    - Retail: WMT
    """)

# Main content
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    asset_type = st.selectbox(
        "Asset Type",
        ["Commodity", "Stock"],
        help="Choose between commodities or stocks"
    )

with col2:
    if asset_type == "Commodity":
        asset = st.selectbox(
            "Select Commodity",
            ["WTI", "BRENT", "NATURAL_GAS", "COPPER", "ALUMINUM", "WHEAT", "CORN", "SUGAR", "COFFEE"],
            help="Choose a commodity to analyze"
        )
    else:
        asset = st.selectbox(
            "Select Stock",
            ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "WMT"],
            help="Choose a stock to analyze"
        )

with col3:
    investment_amount = st.number_input(
        "Investment Amount ($)",
        min_value=1000,
        max_value=1000000,
        value=10000,
        step=1000
    )

question = st.text_area(
    f"Ask a question about this {asset_type.lower()}",
    placeholder=f"e.g., Should I invest in this {asset_type.lower()}? What are the risks? How much should I allocate?",
    height=100
)

analyze_button = st.button("🔍 Analyze Investment", type="primary", use_container_width=True)

# Analysis
if analyze_button:
    if not alpha_vantage_key or not groq_key:
        st.error("⚠️ Please provide both API keys in the sidebar.")
    elif not question:
        st.error(f"⚠️ Please enter a question about the {asset_type.lower()}.")
    else:
        with st.spinner(f"Fetching {asset_type.lower()} data..."):
            try:
                # Fetch data
                fetcher = CommodityDataFetcher(alpha_vantage_key)
                
                # Get data based on asset type
                if asset_type == "Stock":
                    data = fetcher.get_stock_data(asset)
                else:
                    data = fetcher.get_commodity_data(asset)
                
                if data is None or data.empty:
                    st.error(f"Failed to fetch {asset_type.lower()} data. Please check your API key and try again.")
                else:
                    # Display price chart
                    st.subheader(f"📊 {asset} Price History")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data['value'],
                        mode='lines',
                        name='Price',
                        line=dict(color='#3b82f6', width=2)
                    ))
                    
                    fig.update_layout(
                        title=f"{asset} Historical Prices",
                        xaxis_title="Date",
                        yaxis_title="Price (USD)",
                        hovermode='x unified',
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig, width='stretch')
                    
                    # Analyze with LLM
                    with st.spinner("Analyzing with AI..."):
                        analyzer = CommodityAnalyzer(groq_key)
                        analysis = analyzer.analyze_investment(
                            asset,
                            data,
                            question,
                            investment_amount,
                            asset_type.lower()
                        )
                        
                        if analysis:
                            st.subheader("🤖 AI Investment Analysis")
                            st.markdown(analysis)
                            
                            # Save to history
                            st.session_state.analysis_history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'asset_type': asset_type,
                                'asset': asset,
                                'question': question,
                                'amount': investment_amount,
                                'analysis': analysis
                            })
                        else:
                            st.error("Failed to generate analysis. Please try again.")
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Analysis History
if st.session_state.analysis_history:
    st.divider()
    st.subheader("📚 Analysis History")
    
    for idx, item in enumerate(reversed(st.session_state.analysis_history[-5:])):
        with st.expander(f"{item['timestamp']} - {item['asset_type']}: {item['asset']} (${item['amount']:,})"):
            st.markdown(f"**Question:** {item['question']}")
            st.markdown(f"**Analysis:**\n\n{item['analysis']}")

# Footer
st.divider()
st.info("⚠️ This is for informational purposes only. Not financial advice. Always consult a financial advisor.")