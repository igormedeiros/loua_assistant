from langchain.schema import HumanMessage, AIMessage
from voice import speak

from crew import previsao_tempo_tool, cotacao_dolar_tool, noticias_tool, chat_task
from llm_utils import function_call, get_confirmation_intention

def main():
    while True:
        prompt = input("Você: ")
        
        # Discover the intention and suggest a function
        suggested_function = function_call(prompt)
        
        if suggested_function == 'Nenhum':
            response_text = chat_task.run(prompt)
        else:
            confirmation = input(f"Loua: Você gostaria de {suggested_function}?\nVocê: ")
            intention = get_confirmation_intention(confirmation)
            if intention == 'sim':
                if 'obter previsão do tempo' in suggested_function:
                    response_text = previsao_tempo_tool.func()
                elif 'obter cotação do dólar' in suggested_function:
                    response_text = cotacao_dolar_tool.func()
                elif 'obter últimas notícias' in suggested_function:
                    response_text = noticias_tool.func()
                
            else:
                response_text = "Ok, não vou realizar nenhuma ação. Posso ajudar com algo mais?"
        # Add the executed action to the history
        chat_task.history.append(HumanMessage(content=prompt))
        chat_task.history.append(AIMessage(content=response_text))
        print(f"Loua: {response_text}")
        speak(response_text)

if __name__ == "__main__":
    main()