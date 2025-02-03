import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configuração da sessão
app.secret_key = os.getenv("SECRET_KEY", "chave_padrao")  # Define um valor padrão se a variável não estiver no .env
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configuração da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/criar-artigo', methods=['POST'])
def criar_artigo():
    data = request.json
    tema = data.get("tema", "").strip()
    publico_alvo = data.get("publico_alvo", "").strip()

    if not tema or not publico_alvo:
        return jsonify({"erro": "Por favor, forneça um tema e um público-alvo."}), 400

    # Cria o prompt para a OpenAI
    prompt = f"""
                Crie um artigo curto sobre o tema '{tema}', direcionado para o público-alvo '{publico_alvo}'. 
                O artigo deve ser informativo e engajador.
                Sempre incluir hashtag's referentes ao assundo e a hashtag #WGConsultec no final.
            """

    try:
        # Obtém a resposta da OpenAI
        resposta = obter_resposta_openai(prompt)
        return jsonify({"artigo": resposta})
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar o artigo: {str(e)}"}), 500

def obter_resposta_openai(prompt):
    client = openai.OpenAI()  # Novo formato de inicialização

    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Seu nome e Will, você é um redator especializado em criar artigos curtos e informativos sempre com uma chamada para interação com o público."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600, 
            temperature=0.7
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Erro ao obter resposta da OpenAI: {str(e)}")

@app.route('/limpar-historico', methods=['POST'])
def limpar_historico():
    session.pop("historico", None)
    return jsonify({"mensagem": "Histórico apagado com sucesso."})

if __name__ == '__main__':
    app.run(debug=True)