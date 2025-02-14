from flask import jsonify, Response, Blueprint
from services import get_platforms, get_accounts, get_fields, get_insights
import pandas as pd

from datetime import datetime

routes = Blueprint("routes", __name__)
    

@routes.route("/")
def home():
    return jsonify({
        "name": "Natalia Armstrong",
        "email": "natalia.armstronggg@gmail.com",
        "linkedin": "https://www.linkedin.com/in/nataliaarmstrong23/"
    })


@routes.route("/<platform>")
def get_platform_ads(platform):
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
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{current_time}_{platform}.csv"
    csv_data = df.to_csv(index=False)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})


@routes.route("/<platform>/resumo")
def get_platform_summary(platform):
    platforms = get_platforms()
    platform_data = next((plat for plat in platforms if plat['value'] == platform), None)

    if platform_data is None:
        return jsonify({"error": "Platform not found"}), 404

    accounts = get_accounts(platform_data['value'])
    fields = get_fields(platform_data['value'])
    summary_ads = []

    field_map = {field['value']: field['text'] for field in fields}

    all_platform_data = [] 

    for account in accounts:
        insights = get_insights(platform_data['value'], account, list(field_map.keys()))
        for ad in insights:
            ad["Platform"] = platform_data['text']
            ad["Account"] = account['name']
            all_platform_data.append(ad)
    
    df = pd.DataFrame(all_platform_data)
    df = df.rename(columns=field_map)

    numeric_columns = df.select_dtypes(include=['number']).columns
    df_summed = df.groupby(['Platform', 'Account'])[numeric_columns].sum().reset_index()

    summary_ads.extend(df_summed.to_dict(orient='records'))


    df_summary = pd.DataFrame(summary_ads)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{current_time}_{platform}_resumo.csv"
    csv_data = df_summary.to_csv(index=False)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})


@routes.route("/geral")
def get_all_ads():
    platforms = get_platforms()
    all_ads = []

    for platform in platforms:
        accounts = get_accounts(platform['value'])
        fields = get_fields(platform['value'])
        
        field_map = {field['value']: field['text'] for field in fields}
        
        for account in accounts:
            insights = get_insights(platform['value'], account, list(field_map.keys()))
            for ad in insights:
                ad["Platform"] = platform['text']
                ad["Account"] = account['name']
                all_ads.append(ad)

    df = pd.DataFrame(all_ads)
    df = df.rename(columns=field_map)

    numeric_columns = df.select_dtypes(include=['number']).columns
    df_summed = df.groupby(['Platform', 'Account'])[numeric_columns].sum().reset_index()


    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{current_time}_geral.csv"
    csv_data = df_summed.to_csv(index=False)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})


@routes.route("/geral/resumo")
def get_summary_ads():
    platforms = get_platforms()
    summary_ads = []
    for platform in platforms:
        accounts = get_accounts(platform['value'])
        fields = get_fields(platform['value'])

        field_map = {field['value']: field['text'] for field in fields}
        
        all_platform_data = [] 

        for account in accounts:
            insights = get_insights(platform['value'], account, list(field_map.keys()))
            for ad in insights:
                ad["Platform"] = platform['text']
                ad["Account"] = account['name']
                all_platform_data.append(ad)
        
        df = pd.DataFrame(all_platform_data)
        df = df.rename(columns=field_map)

        numeric_columns = df.select_dtypes(include=['number']).columns
        df_summed = df.groupby(['Platform'])[numeric_columns].sum().reset_index()

        summary_ads.extend(df_summed.to_dict(orient='records'))

    df_summary = pd.DataFrame(summary_ads)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{current_time}_geral_resumo.csv"
    csv_data = df_summary.to_csv(index=False)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})

if __name__ == "__main__":
    routes.run(debug=True, host="0.0.0.0", port=5000)
