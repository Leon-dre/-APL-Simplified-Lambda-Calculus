import ply.lex as lex
import ply.yacc as yacc
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# load_dotenv()

# # Retrieve the API key from environment variables
# key = os.getenv('API_KEY')

# genai.configure(api_key=key)

# # Create the model
# # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
# generation_config = {
#   "temperature": 0.5,
#   "top_p": 0.95,
#   "top_k": 64,
#   "max_output_tokens": 240,
#   "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#   model_name="gemini-1.5-flash",
#   generation_config=generation_config,
#   # safety_settings = Adjust safety settings
#   # See https://ai.google.dev/gemini-api/docs/safety-settings
# )

# chat_session = model.start_chat(
#   history=[
#   ]
# )
# response = chat_session.send_message("Explain the meaning of big O")
# print(response.text)

# Token definitions
tokens = ['LAMBDA', 'DOT', 'LPAREN', 'RPAREN', 'VAR']

t_LAMBDA = r'\#'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'# Ignore spaces and tabs

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

def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

# Test the lexer and parser
def test_parser(input_string):
    lexer.input(input_string)
    for token in lexer:
        print(f"Token: {token.type}, Value: {token.value}")

    result = parser.parse(input_string)
    print("Parsed Result:", result)

# Test examples
test_parser("a")
test_parser("#x.x")
test_parser("(#x.#y.yx)")
test_parser("fa")