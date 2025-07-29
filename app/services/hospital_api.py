import requests

def fetch_hospital_data(api_key: str, page: int = 1, per_page: int = 1000):
    url = "https://api.odcloud.kr/api/3045143/v1/uddi:a121e723-7ae7-44df-ba6f-86eb09a633e7"
    params = {
        "page": page,
        "perPage": per_page,
        "returnType": "JSON",
        "serviceKey": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json().get("data", [])
    return [item for item in data if item.get("병원종별", "").strip() == "종합병원"]
