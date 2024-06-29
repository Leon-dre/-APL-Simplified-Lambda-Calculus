import ply.lex as lex
import ply.yacc as yacc
import openai as OpenAI
from dotenv import load_dotenv
import os

load_dotenv

client = OpenAI(
   api_key =os.getenv('API_KEY'),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo-instrct",
)

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