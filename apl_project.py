#Name             |  github
#Leondre Bromfield|  @Leon-dre
#Tichina Buckle   |  @Tichina
#Orville Cole     |  @villas_cole1838
#Nathan Williams  |  @Natjoe


import ply.lex as lex
import ply.yacc as yacc
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Retrieve the API key from environment variables
key = os.getenv('API_KEY')

genai.configure(api_key=key)

# Create the Gemini model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)


# YACC Tokens
tokens = ['LAMBDA', 'DOT', 'LPAREN', 'RPAREN', 'VAR']

# regular expressions
t_LAMBDA = r'\#'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'# Ignores spaces and escape

def t_VAR(t):
    r'[a-z]'
    return t

def t_error(t):
    if t.value[0].isupper():
        print(f"Illegal character '{t.value[0]}'. Character must be lowercase.")
    else:
        print(f"Illegal character '{t.value[0]}' detected.")
    t.lexer.skip(1)

lexer = lex.lex()

# Grammar rules
def p_expr_var(p):
    'expr : VAR'
    p[0] = ('var', p[1])

def p_expr_func_arg(p):
    'expr : func arg'
    p[0] = ('func_arg', p[1], p[2])

def p_expr_lambda_expr(p):
    'expr : LAMBDA VAR DOT expr'
    p[0] = ('lambda', p[2], p[4])

def p_func_var(p):
    'func : VAR'
    p[0] = ('var', p[1])

def p_func_lambda_expr(p):
    'func : LPAREN LAMBDA VAR DOT expr RPAREN'
    p[0] = ('lambda', p[3], p[5])

def p_func_func_arg(p):
    'func : func arg'
    p[0] = ('func_arg', p[1], p[2])

def p_func_var_expr(p):
    'func : VAR DOT expr'
    p[0] = ('var_expr', p[1], p[3])

def p_arg_var(p):
    'arg : VAR'
    p[0] = ('var', p[1])

def p_arg_lambda_expr(p):
    'arg : LPAREN LAMBDA VAR DOT expr RPAREN'
    p[0] = ('lambda', p[3], p[5])

def p_arg_func_arg(p):
    'arg : LPAREN func arg RPAREN'
    p[0] = ('func_arg', p[2], p[3])

#error handling
def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

#logging

def run_interpreter():
    while True:
        try:
            # Prompt user for input
            s = input("Enter expression (or 'exit' to quit): ")
            if s.strip().lower() == 'exit':
                print("Arion 5 Rocket... oops... I mean Mission Aborted!")
                break

            # Tokenize and parse the input
            lexer.input(s)
            for token in lexer:
                print(f"Token: {token.type}, Value: {token.value}")
            chat_session = model.start_chat(
              history=[
              ]
            )
            response = chat_session.send_message("Use BETA reduction to solve " + s +" and show steps. The '#' is the lambda symbol")
            print(response.text)
            result = parser.parse(s)
            print("Parsed Result:", result)

        except EOFError:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

# Start the interpreter
run_interpreter()