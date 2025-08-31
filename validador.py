import chardet
import fitz
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()


PROMPT_IA = """
Você é um assistente que classifica e-mails como PRODUTIVOS ou IMPRODUTIVOS sabendo que é uma grande empresa
do setor financeiro, que lida com alto volume de emails diariamente, objetivo é automatizar a leitura e classificação 
desses emails e sugerir classificações e respostas automáticas de acordo com o teor de cada email recebido, liberando tempo da equipe para que não seja mais necessário ter uma pessoa fazendo esse trabalho manualmente.

Considere como PRODUTIVO qualquer e-mail que:
Produtivo: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre
 casos em aberto, dúvidas sobre o sistema).

Considere como IMPRODUTIVO qualquer e-mail que:
Improdutivo: Emails que não necessitam de uma ação imediata
 (ex.: mensagens de felicitações, agradecimentos).

Responda apenas com "Produtivo" ou "Improdutivo" e explique brevemente e o por quê.

"""
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def retirar_texto_pdf(arquivo):
    texto = ''

    with fitz.open(arquivo) as pdf:
        for page in pdf:
            texto += page.get_text()
    return texto.strip()

def tirar_texto_txt(arquivo):
    with open(arquivo, 'rb') as f:
        result = chardet.detect(f.read())
    with open(arquivo, 'r', encoding=result['encoding']) as f:
        return f.read().strip()
def analise_IA(texto):
    # IA do google
    model = genai.GenerativeModel('gemini-2.5-pro')
    resposta = model.generate_content(f'{PROMPT_IA}\n\n Texto do email: {texto}')
    return resposta.text.strip()
