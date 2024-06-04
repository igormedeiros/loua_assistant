import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
groq_model = "llama3-70b-8192"

# Set up the LLM ChatGroq
groq_llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name=groq_model)


def function_call(prompt):
    function_options = ['obter previsão do tempo', 'obter cotação do dólar', 'obter as últimas notícias', 'Nenhuma']

    sys_msg = f"""
        Você é um modelo de IA especializado em identificar chamadas de função. Sua tarefa é determinar qual
        ação é mais adequada para responder ao prompt do usuário: obter a previsão do tempo, verificar a cotação do dólar,
        obter as últimas notícias ou nenhuma das opções. Você deve escolher apenas uma dessas ações ou optar por não chamar
        nenhuma função se for mais apropriado.

        Aqui estão alguns exemplos para ajudá-lo:
        - "Uau, acho que está ficando frio" -> obter previsão do tempo
        - "O dólar está mais barato hoje?" -> obter cotação do dólar
        - "Você ouviu falar sobre aquele acidente?" -> obter as últimas notícias
        - "Você sabe o meu nome?" -> Nenhuma

        Responda com uma única seleção da lista fornecida: {function_options}.
        Não inclua explicações ou informações adicionais. Formate sua resposta exatamente como está na lista.
    """
    
    # Check if the prompt contains keywords related to the name
    if any(keyword in prompt.lower() for keyword in ["nome", "quem é você"]):
        return "Nenhum"

    function_convo = [{'role': 'system', 'content': sys_msg},
                     {'role': 'user', 'content': prompt}]

    result = groq_llm.invoke(function_convo)
    result_content = result.content.strip()

    if result_content not in function_options:
        result_content = 'None'

    return result_content

def get_confirmation_intention(prompt):
    answer_options = ['sim', 'não', None]

    sys_msg = f"""
        Você é um modelo de IA especializado em identificar a intenção do usuário. Sua tarefa é determinar qual
        resposta está por trás do prompt do usuário, se é uma das opções {answer_options}. Você deve retornar a string "sim", se esta for a intenção que você identificar e "não" para uma intenção negativa, você ainda pode retornar None se estiver em dúvida sobre a intenção.

        Aqui estão alguns exemplos para ajudá-lo:
        - "ah poderia ser" -> sim
        - "ah estou em dúvida" -> None
        - "Outra hora" -> não
        - "Acho que seria bom" -> sim
        - "não precisa" -> não 

        Responda com uma única seleção da lista fornecida: {answer_options}.
        Não inclua explicações ou informações adicionais. Formate sua resposta exatamente como está na lista.
    """
    
    function_convo = [{'role': 'system', 'content': sys_msg},
                      {'role': 'user', 'content': prompt}]

    result = groq_llm.invoke(function_convo)
    result_content = result.content.strip()

    if result_content not in answer_options:
        result_content = None

    return result_content