from prompt import prompt_interviewer, prompt_result, prompt_verdict
# from langchain.llms import openai
from langchain_community.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
print(openai_key)

llm = OpenAI(model_name = 'gpt-4o-mini', api_key = openai_key)

def handle_question(state):
   
    history = state.get('history', '').strip()
    role = state.get('interviewer','').strip()
    candidate = state.get('candidate', '').strip()


    prompt = prompt_interviewer.format(role,candidate,history)

    question = role+ ": " +llm.invoke(prompt)
    print("\nQuestion: \n\n",question)
    if(history=='Nothing'):
        history=''
    return {"history":history+'\n'+question,"current_question":question,"total_questions":state.get('total_questions')+1}

def handle_response(state):
    history = state.get('history','').strip()
    question = state.get('current_question','').strip()
    candidate = state.get('candidate','').strip()

    user_answer = input('\nEnter your Answer: \n')
    answer = candidate + ': ' + user_answer
    print('\nResponse: \n'+answer)
    return {'history':history+'\n'+answer, 'current_answer':answer}

def handle_eval(state):
    question = state.get('current_question','').strip()
    answer = state.get('current_answer','').strip()
    history = state.get('history','').strip()

    prompt = prompt_result.format(question,answer)
    evaluation = llm.invoke(prompt)
    #print(prompt)
    print('\nEvaluation :\n'+evaluation)
    print('\n*****************Done******************\n')
    return {'history':history+'\n'+evaluation}

def handle_result(state):
    history = state.get('history','').strip()
    candidate = state.get('candidate','').strip()
    prompt = prompt_verdict.format(candidate,history)
    result = llm.invoke(prompt)
    print('\n Results: \n'+result)

    return {'result':result,'history':history}

def check_conv_length(state):
    
    if (state.get('total_questions') < 5):
        
        return 'handle_question'
    else:
    
        return 'handle_result'






