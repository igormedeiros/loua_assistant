import os
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from crewai import Agent
from pydantic import BaseModel, Field
from typing import List
from tools import obter_previsao_tempo, obter_cotacao_dolar, obter_noticias

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
groq_model = "llama3-70b-8192"

# Set up the LLM ChatGroq
groq_llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name=groq_model)

def get_task_history():
    return SystemMessage(content='''
        Você é uma assistente de voz AI chamada Loua e é do sexo feminino.
        Sua tarefa é gerar a resposta mais útil e factual possível,
        seu tom deve ser amigável, acolhedor e informativo.
        Use o contexto fornecido quando disponível.
        Certifique-se de que suas respostas sejam claras,
        concisas e diretamente relevantes para a conversa em andamento, evitando qualquer verbosidade.
    ''')

# Create tools
previsao_tempo_tool = Tool(name="obter_previsao_tempo", func=obter_previsao_tempo, description="Get the weather forecast.")
cotacao_dolar_tool = Tool(name="obter_cotacao_dolar", func=obter_cotacao_dolar, description="Get the dollar quotation.")
noticias_tool = Tool(name="obter_noticias", func=obter_noticias, description="Get the latest news.")

tools = [previsao_tempo_tool, cotacao_dolar_tool, noticias_tool]


# Define the agent's task
class ChatTask(BaseModel):
    description: str
    expected_output: str
    agent: Agent
    history: List[SystemMessage] = Field(default_factory=lambda: [get_task_history()])
    introduced: bool = False

    def run(self, prompt: str) -> str:
        user_message = HumanMessage(content=prompt)

        # Add user message to history
        self.history.append(user_message)

        response = self.agent.llm._generate(self.history)
        response_text = response.generations[0].text

        # Add response to history
        self.history.append(AIMessage(content=response_text))
        
        return response_text

# Create the agent
loua_agent = Agent(
    role='Assistente de Voz AI',
    goal='Fornecer informações precisas e úteis de maneira amigável e informativa',
    verbose=True,
    memory=True,
    backstory=(
        "Você é Loua, uma assistente de voz AI do sexo feminino. "
        "Sua missão é ajudar os usuários com informações precisas e úteis, "
        "sempre mantendo um tom amigável, gentil e acolhedor."
    ),
    tools=tools,
    llm=groq_llm
)

# Inicialize a tarefa do agente
chat_task = ChatTask(
    description="Responda às perguntas do usuário de maneira amigável e informativa",
    expected_output="Texto de resposta gerado pelo agente Loua",
    agent=loua_agent
)