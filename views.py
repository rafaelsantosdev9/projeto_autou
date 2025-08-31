
from flask import render_template,request,redirect,flash
# deixa o arquivo seguro
from werkzeug.utils import secure_filename
# manipulação de arquivos
import os

from validador import retirar_texto_pdf, tirar_texto_txt,analise_IA

EXTENSOES = {'pdf','txt'}
# compara se o arquivo enviado é os validados
def extensoes_permitidas(arquivo):
    # verifica sem . no arquivo
    return '.' in arquivo and arquivo.rsplit('.',1)[1].lower() in EXTENSOES
    # rsplit() divide uma string eum lista de substrings
def init_app(app):
    @app.route('/', methods=['GET', 'POST'])
    def enviar_arquivo():
        if request.method == 'POST':
            acao = request.form.get('acao')

            # Se clicou em "Analisar Texto"
            if acao == "texto":
                texto_email = request.form.get('texto_email', '').strip()
                if not texto_email:
                    flash('Nenhum texto digitado')
                    return redirect(request.url)
                try:
                    resultado = analise_IA(texto_email)
                    flash(f"Resultado: {resultado}")
                except Exception as e:
                    flash(f"Erro ao processar com IA: {e}")
                return redirect(request.url)

            # Se clicou em "Analisar Arquivo"
            elif acao == "arquivo":
                arquivo = request.files.get('file')
                if not arquivo or arquivo.filename == '':
                    flash('Nenhum arquivo selecionado')
                    return redirect(request.url)

                if arquivo and extensoes_permitidas(arquivo.filename):
                    nome_arquivo = secure_filename(arquivo.filename)
                    caminho_arquivo = os.path.join('uploads', nome_arquivo)
                    os.makedirs('uploads', exist_ok=True)
                    arquivo.save(caminho_arquivo)

                    if nome_arquivo.endswith('.pdf'):
                        texto = retirar_texto_pdf(caminho_arquivo)
                    else:
                        texto = tirar_texto_txt(caminho_arquivo)

                    if not texto.strip():
                        flash('Arquivo vazio')
                        return redirect(request.url)

                    try:
                        resultado = analise_IA(texto)
                        flash(f"Resultado: {resultado}")
                    except Exception as e:
                        flash(f"Erro ao processar com IA: {e}")
                    return redirect(request.url)

                flash('Apenas arquivos PDF e TXT são permitidos')
                return redirect(request.url)

        return render_template('home.html')
