import streamlit as st
from agent_manager import AgentManager
from config import Config

def load_css():
    st.markdown("""
        <style>
        .main-header {color: #1E3A8A; font-size: 42px; font-weight: bold; text-align: center; margin-bottom: 30px;}
        .sub-header {font-size: 28px; font-weight: bold; color: #1E3A8A; margin-top: 30px; margin-bottom: 20px;}
        .description {font-size: 18px; color: #4B5563; margin-bottom: 20px;}
        .feature-box {background-color: #F3F4F6; border-radius: 10px; padding: 20px; margin-bottom: 20px;}
        .feature-title {font-size: 20px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;}
        .feature-desc {font-size: 16px; color: #4B5563;}
        </style>
    """, unsafe_allow_html=True)



def main():
    st.set_page_config(page_title="DerivaQuery: Natural Language Database Queries for Derivatives", page_icon="🏠", layout="wide")
    load_css()

    st.markdown('<h1 class="main-header">DerivaQuery: Your Intelligent Derivative Query Solution</h1>', unsafe_allow_html=True)

    #db_manager = DatabaseManager()
    agent_manager = AgentManager()

    st.markdown('<p class="description">Welcome to DerivaQuery ! We leverage advanced AI and comprehensive market data to provide precise and intuitive natural language queries for derivatives products.</p>', unsafe_allow_html=True)

    st.markdown('<h2 class="sub-header">Select a Database</h2>', unsafe_allow_html=True)
    database = st.selectbox("Choose a database to analyze:", ["FinDerivaDB", "MarketQueryDB", "DerivDataVault", "TradeInsightDB"])

    database_map = {
        "FinDerivaDB": "FinDerivaDB",
        "MarketQueryDB": "MarketQueryDB",
        "DerivDataVault": "DerivDataVault",
        "TradeInsightDB": "TradeInsightDB"
    }

    selected_database = database_map[database]

    st.markdown('<h2 class="sub-header">Ask DerivaQueryBot</h2>', unsafe_allow_html=True)
    user_question = st.text_input(f"What would you like to know about derivatives in {database}?")

    if st.button("Get Insights"):
        with st.spinner(f"Analyzing ..."):
            st.success(agent_manager.query_evaluation(user_question))
            #st.success(user_question) 
            #if response == Config.GOAHEAD:
                #response = agent_manager.query(user_question)
                #st.success(f"Here's the Answer:  {response}")
                #st.success('SUCESSO')
            #else:
            #    st.warning('I cannot perform this request')
            #st.write(response)

    #st.markdown('<h2 class="sub-header">Market Insights</h2>', unsafe_allow_html=True)
    #st.plotly_chart(create_city_price_comparison(db_manager), use_container_width=True)


if __name__ == "__main__":
    main()