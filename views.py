# views.py
from flask import render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os

from validador import retirar_texto_pdf, tirar_texto_txt, analise_IA

EXTENSOES = {'pdf', 'txt'}

def extensoes_permitidas(nome):
    return '.' in nome and nome.rsplit('.', 1)[1].lower() in EXTENSOES

def init_app(app):
    @app.route('/', methods=['GET', 'POST'])
    def enviar_arquivo():
        if request.method == 'POST':
            acao = request.form.get('acao')

            # --- Análise de TEXTO ---
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

            # --- Análise de ARQUIVO ---
            if acao == "arquivo":
                arquivo = request.files.get('file')
                if not arquivo or arquivo.filename == '':
                    flash('Nenhum arquivo selecionado')
                    return redirect(request.url)

                if not extensoes_permitidas(arquivo.filename):
                    flash('Apenas arquivos PDF e TXT são permitidos')
                    return redirect(request.url)

                nome_arquivo = secure_filename(arquivo.filename)
                caminho_arquivo = os.path.join('uploads', nome_arquivo)
                os.makedirs('uploads', exist_ok=True)
                arquivo.save(caminho_arquivo)

                ext = os.path.splitext(nome_arquivo)[1].lower()
                if ext == '.pdf':
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

            # Se nenhum "acao" veio (ex.: submit sem name/value)
            flash('Selecione uma ação válida.')
            return redirect(request.url)

        return render_template('home.html')
