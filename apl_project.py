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
precedence = (
    ('left', 'DOT'),
    ('left', 'LAMBDA'),
    ('left', 'VAR')
)

def p_expr_var(p):
    'expr : VAR'
    p[0] = ('var', p[1])

def p_expr_func_arg(p):
    'expr : expr expr'
    p[0] = ('func_arg', p[1], p[2])

def p_expr_lambda_expr(p):
    'expr : LAMBDA VAR DOT expr'
    p[0] = ('lambda', p[2], p[4])

def p_expr_parens(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]
    
#error handling
def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

#logging
# Beta reduction function block start
def replace(var, expr, replacement):
    if expr[0] == 'var':
        if expr[1] == var:
            return replacement
        else:
            return expr
    elif expr[0] == 'lambda':
        if expr[1] == var:
            return expr
        else:
            return ('lambda', expr[1], replace(var, expr[2], replacement))
    elif expr[0] == 'func_arg':
        return ('func_arg', replace(var, expr[1], replacement), replace(var, expr[2], replacement))
    else:
        return expr

def beta(expr):
    if expr[0] == 'func_arg':
        if expr[1][0] == 'lambda':
            return replace(expr[1][1], expr[1][2], expr[2])
        else:
            return ('func_arg', beta(expr[1]), beta(expr[2]))
    elif expr[0] == 'lambda':
        return ('lambda', expr[1], beta(expr[2]))
    else:
        return expr

def to_string(expr):
    if expr[0] == 'var':
        return expr[1]
    elif expr[0] == 'lambda':
        return f"#{expr[1]}.{to_string(expr[2])}"
    elif expr[0] == 'func_arg':
        return f"({to_string(expr[1])} {to_string(expr[2])})"
    else:
        return ""

def to_normal_form(expr):
    prev_expr = None
    while expr != prev_expr:
        prev_expr = expr
        expr = beta(expr)
    return expr
#Beta reduction function block end

def blast_off():
    while True:
        try:
            # Prompt user for input
            s = input("Enter expression (or 'exit' to exit the application): ")
            if s.strip().lower() == 'exit':
                print("Arion 5 Rocket... oops... I mean Mission Aborted!")
                break

            # Tokenize and parse the input
            lexer.input(s)
            for token in lexer:
                print(f"Token: {token.type}, Value: {token.value}")
            
            data = (s)
            ast = parser.parse(data)
            print("Original AST:", ast)
            
            if ast:
               reduced_ast = to_normal_form(ast)
               print("Reduced AST:", reduced_ast)
               print("Reduced Expression in Normal Form:", to_string(reduced_ast))
               chat_session = model.start_chat(
               history=[]
               )  
               response = chat_session.send_message("(Imagine that the '#' is a Lambda symbol). Explain how we got to " +to_string(reduced_ast) + "from " +s+ " in terms of BETA reduction from Lambda Calculus.")
               print(response.text)
            else:
               print("Failed to parse the expression.")
               
        except EOFError:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

# Start the interpreter
blast_off()