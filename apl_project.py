import ply.lex as lex
import ply.yacc as yacc
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv('API_KEY')

# Check if API key is retrieved correctly
if not api_key:
    raise ValueError("API_KEY not found. Make sure it's defined in the .env file.")

# Set the API key for the openai module
openai.api_key = api_key

# Create a chat completion
try:
    chat_completion = openai.ChatCompletion.create(
        model="davinci-002",  # Use the correct model name
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ]
    )

    # Print the response
    print(chat_completion)
except Exception as e:
    print(f"Error occurred: {e}")

tokens = [
 
 'INT',
 'FLOAT',
 'NAME',
 'PLUS',
 'MINUS',
 'DIVIDE',
 'MULTIPLY',
 'EQUALS'
 
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'='
t_ignore = r' '

def t_INT(t):
   r'\d+'
   t.value = int(t.value)
   return t
def t_FLOAT(t):
   r'\d\.\d+'
   t.value = float(t.value)
   return t
def t_NAME(t):
   r'[a-zA-Z_][a-zA-Z_0-9]*'
   t.type = 'NAME'
   return t
def t_error(t):
   print("Illegal syntax")
   t.lexer.skip(1)

lexer = lex.lex()

lexer.input("1+ 3 ")

while True:
   tok = lexer.token()
   if not tok:
       break
   print(tok)