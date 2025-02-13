from flask import Flask, jsonify, Response
import requests
import pandas as pd

app = Flask(__name__)

# Dados pessoais no endpoint raiz
@app.route("/")
def home():
    return jsonify({
        "name": "Natalia Armstrong",
        "email": "natalia.armstronggg@gmail.com",
        "linkedin": "https://www.linkedin.com/in/nataliaarmstrong23/"
    })

# URL da API
API_URL = "https://sidebar.stract.to/api"
TOKEN = "ProcessoSeletivoStract2025"  # Token geral, que não é usado para as contas

# Funções para consumir os endpoints da API
def get_platforms():
    """ Obtém a lista de plataformas disponíveis. """
    url = f"{API_URL}/platforms"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['platforms']

def get_accounts(platform):
    """ Obtém as contas para uma plataforma específica. """
    url = f"{API_URL}/accounts?platform={platform}"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['accounts']

def get_fields(platform):
    """ Obtém os campos disponíveis para uma plataforma. """
    url = f"{API_URL}/fields?platform={platform}"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['fields']

def get_insights(platform, account, fields):
    """ Obtém os insights de anúncios de uma conta em uma plataforma usando o token da conta. """
    url = f"{API_URL}/insights?platform={platform}&account={account['id']}&token={account['token']}&fields={','.join(fields)}"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['insights']

# Endpoint para retornar todos os anúncios de todas as plataformas
@app.route("/geral")
def get_all_ads():
    """ Retorna um CSV com todos os anúncios de todas as plataformas. """
    platforms = get_platforms()
    all_ads = []

    for platform in platforms:
        accounts = get_accounts(platform['value'])
        fields = get_fields(platform['value'])
        
        # Mapeando os campos (text como header e value como chave dos dados)
        field_map = {field['value']: field['text'] for field in fields}
        
        for account in accounts:
            insights = get_insights(platform['value'], account, list(field_map.keys()))
            for ad in insights:
                ad["Platform"] = platform['text']
                ad["Account"] = account['name']
                all_ads.append(ad)

    # Criação do DataFrame com as colunas dinâmicas baseadas nos "text"
    df = pd.DataFrame(all_ads)
    df = df.rename(columns=field_map)

    # Somando os valores numéricos para cada plataforma e conta
    numeric_columns = df.select_dtypes(include=['number']).columns
    df_summed = df.groupby(['Platform', 'Account'])[numeric_columns].sum().reset_index()

    # Gerar o CSV com todos os dados agregados
    csv_data = df_summed.to_csv(index=False)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=geral.csv"})

@app.route("/geral/resumo")
def get_summary_ads():
    """ Retorna um resumo CSV com todos os anúncios de todas as plataformas. """
    platforms = get_platforms()
    summary_ads = []

    for platform in platforms:
        accounts = get_accounts(platform['value'])
        fields = get_fields(platform['value'])

        # Mapeando os campos (text como header e value como chave dos dados)
        field_map = {field['value']: field['text'] for field in fields}
        
        all_platform_data = []  # Armazenar todos os anúncios dessa plataforma

        for account in accounts:
            insights = get_insights(platform['value'], account, list(field_map.keys()))
            for ad in insights:
                ad["Platform"] = platform['text']
                ad["Account"] = account['name']
                all_platform_data.append(ad)
        
        df = pd.DataFrame(all_platform_data)
        df = df.rename(columns=field_map)

        # Somando os valores numéricos para cada plataforma
        numeric_columns = df.select_dtypes(include=['number']).columns
        df_summed = df.groupby(['Platform'])[numeric_columns].sum().reset_index()

        # Gerar o CSV com os dados agregados
        summary_ads.extend(df_summed.to_dict(orient='records'))

    # Criar o DataFrame para o resumo
    df_summary = pd.DataFrame(summary_ads)

    # Gerar o CSV com os dados agregados
    csv_data = df_summary.to_csv(index=False)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=geral_resumo.csv"})

# Endpoint para retornar os anúncios de uma plataforma específica
@app.route("/<platform>")
def get_platform_ads(platform):
    """ Retorna um CSV com todos os anúncios de uma plataforma específica. """
    platforms = get_platforms()
    platform_data = next((plat for plat in platforms if plat['value'] == platform), None)

    if platform_data is None:
        return jsonify({"error": "Platform not found"}), 404

    accounts = get_accounts(platform_data['value'])
    fields = [field['value'] for field in get_fields(platform_data['value'])]
    all_ads = []

    for account in accounts:
        insights = get_insights(platform_data['value'], account, fields)
        for ad in insights:
            ad["Platform"] = platform_data['text']
            ad["Account"] = account['name']
            all_ads.append(ad)

    df = pd.DataFrame(all_ads)
    csv_data = df.to_csv(index=False)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={platform}_ads.csv"})

# Endpoint para retornar o resumo de uma plataforma específica
@app.route("/<platform>/resumo")
def get_platform_summary(platform):
    """ Retorna um resumo CSV de uma plataforma específica. """
    platforms = get_platforms()
    platform_data = next((plat for plat in platforms if plat['value'] == platform), None)

    if platform_data is None:
        return jsonify({"error": "Platform not found"}), 404

    accounts = get_accounts(platform_data['value'])
    fields = get_fields(platform_data['value'])
    summary_ads = []

    # Mapeando os campos (text como header e value como chave dos dados)
    field_map = {field['value']: field['text'] for field in fields}

    all_platform_data = []  # Armazenar todos os anúncios dessa plataforma

    for account in accounts:
        insights = get_insights(platform_data['value'], account, list(field_map.keys()))
        for ad in insights:
            ad["Platform"] = platform_data['text']
            ad["Account"] = account['name']
            all_platform_data.append(ad)
    
    df = pd.DataFrame(all_platform_data)
    df = df.rename(columns=field_map)

    # Somando os valores numéricos para cada conta e plataforma
    numeric_columns = df.select_dtypes(include=['number']).columns
    df_summed = df.groupby(['Platform', 'Account'])[numeric_columns].sum().reset_index()

    # Gerar o CSV com os dados agregados
    summary_ads.extend(df_summed.to_dict(orient='records'))

    # Criar o DataFrame para o resumo
    df_summary = pd.DataFrame(summary_ads)

    # Gerar o CSV com os dados agregados
    csv_data = df_summary.to_csv(index=False)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={platform}_resumo.csv"})

if __name__ == "__main__":
    app.run(debug=True)
