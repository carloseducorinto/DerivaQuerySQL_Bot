from langchain_groq.chat_models import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import AgentType
from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, MessagesPlaceholder, PromptTemplate, SystemMessagePromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from config import Config
import plotly.express as px
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import re
#import getpass
#import os
#os.environ["OPENAI_API_KEY"] = getpass.getpass()

def format_price(price):
    try:
        price_float = float(price.replace(',', ''))
        return f"${price_float:,.2f}"
    except ValueError:
        return price


def clean_text(text):
    clean = re.sub(r'[^\x00-\x7F]+', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

#def create_data_visualization(response):
    #df = db_manager.get_data(query)
    #fig = px.bar(df, x='city', y='avg_price', title='Average Housing Prices by City')
    #fig.update_layout(xaxis_title='City', yaxis_title='Average Price')
    #return fig

def prompt_preparation():

    example_selector = SemanticSimilarityExampleSelector.from_examples(
    Config.examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
    )
     
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input"],
        prefix=Config.system_prefix,
        suffix="",
    )
    
    full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
    )
    
    return full_prompt


class AgentManager:
    def __init__(self):
        
        self.model = ChatGroq(model_name=Config.MODEL_NAME_llama, api_key=Config.GROQ_API_KEY)
        #self.model = ChatOpenAI(model_name=Config.MODEL_NAME, api_key=Config.OPENAI_API_KEY, temperature=0)
        dbuser = Config.DB_user
        dbpassword = Config.DB_password
        dbname = Config.DB_name
        dbhost = Config.DB_host
        dbport = Config.DB_port


        self.db_manager = SQLDatabase.from_uri(f"mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}")

        
    def query(self, question):
        
        agent_executor = create_sql_agent(
            self.model,
            db=self.db_manager,
            prompt=prompt_preparation(),
            agent_type="openai-tools",
            verbose=True
        )
        
 
        response = agent_executor.invoke( {
        "input": question,
        "agent_scratchpad": []
        })['output']
        
        #response = clean_text(response)

        return response
    
    def query_evaluation(self,user_input):
    
        print('Passei 11')
        output_parser = StrOutputParser()
        llm = ChatOpenAI(temperature=0, model=Config.MODEL_NAME_4o)
        prompt = ChatPromptTemplate.from_template(Config.evaluator_agent_template)
        chain = prompt | llm | output_parser
        response = chain.invoke({"user_input": user_input})
        #print(response.messages[0].content)
        return response
    