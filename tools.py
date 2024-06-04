import os
from dotenv import load_dotenv
import pyowm
from langchain.agents import Tool
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
groq_model = "llama3-70b-8192"

# Configurar o LLM ChatGroq
groq_llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name=groq_model)

owp_api_key = os.getenv('OPENWEATHERMAP_API_KEY')

# Definir ferramentas a partir das funções utilitárias
def obter_previsao_tempo():
    owm = pyowm.OWM(owp_api_key)
    mgr = owm.weather_manager()
    
    localizacao = 'São Paulo,BR'
    observation = mgr.weather_at_place(localizacao)
    weather = observation.weather
    dados_meteorologicos = {
        'temperatura': weather.temperature('celsius')['temp'],
        'umidade': weather.humidity,
        'pressao': weather.pressure['press'],
        'descricao': weather.detailed_status,
        'vento': {
            'velocidade': weather.wind()['speed'],
            'direcao': weather.wind()['deg']
        }
    }

    sys_msg = f"Informe a previsão do tempo para {localizacao}, com os seguintes dados: {dados_meteorologicos}"
    prompt = f"""informe a previsão do tempo para {localizacao}.
    A resposta deve ter a saída formatada com os seguintes dados: temperatura, umidade, pressão, descrição, velocidade do vento e direção do vento..
    Exemplo de resposta: Previsão do tempo para São Paulo, BR:

    Condições Atuais
    - Temperatura: 18,09°C
    - Umidade: 80%
    - Pressão: 1027 hPa

    Céu
    - Descrição: Céu Limpo (Clear Sky)

    Vento
    - Velocidade: 2,06 m/s
    - Direção: 70° (Nordeste)

    Em resumo, o tempo em São Paulo está agradável, com um céu limpo e uma temperatura agradável de 18,09°C. O vento é leve, soprando a 2,06 m/s em uma direção nordeste.
    """

    function_convo = [{'role': 'system', 'content': sys_msg}, 
                      {'role': 'user', 'content': prompt}]

    # Correção: Extrair o conteúdo da mensagem e remover espaços em branco extras
    result = groq_llm.invoke(function_convo)
    result_content = result.content  # Extrair o conteúdo da mensagem
    result_stripped = result_content.strip()  # Remover espaços em branco

    return result_stripped

def obter_cotacao_dolar():
    return "Aqui está a cotação do dólar."

def obter_noticias():
    return "Aqui estão as últimas notícias."

# Criar ferramentas
previsao_tempo_tool = Tool(name="obter_previsao_tempo", func=obter_previsao_tempo, description="Obter a previsão do tempo.")
cotacao_dolar_tool = Tool(name="obter_cotacao_dolar", func=obter_cotacao_dolar, description="Obter a cotação do dólar.")
noticias_tool = Tool(name="obter_noticias", func=obter_noticias, description="Obter as últimas notícias.")

tools = [previsao_tempo_tool, cotacao_dolar_tool, noticias_tool]

