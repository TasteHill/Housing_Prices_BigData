from tqdm import tqdm
import pandas as pd
import requests
import os
import requests


def get_geocoding_api(place, api_key):
    url = f"https://dapi.kakao.com/v2/local/search/address.json?query={place}"
    headers = {"Authorization": f"KakaoAK {api_key}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result["documents"]:
            return result["documents"][0]["y"], result["documents"][0]["x"]
    return None, None  # 실패 시 None 반환


def get_location(df: pd.DataFrame, location_column: str, api_key: str, cache_file: str = "location_cache.csv") -> pd.DataFrame:
    if os.path.exists(cache_file):
        cache_df = pd.read_csv(cache_file)
    else:
        cache_df = pd.DataFrame(columns=["주소", "위도", "경도"])

    cached_addresses = set(cache_df["주소"])

    unique_addresses = set(df[location_column])
    new_addresses = unique_addresses - cached_addresses

    new_data = []
    for address in tqdm(new_addresses, desc="Fetching new addresses"):
        lat, lng = get_geocoding_api(address, api_key)
        if lat and lng is not None:
            new_data.append({"주소": address, "위도": lat, "경도": lng})

    new_df = pd.DataFrame(new_data)

    updated_cache_df = pd.concat([cache_df, new_df], ignore_index=True)

    updated_cache_df.to_csv(cache_file, index=False)

    result_df = df.merge(updated_cache_df, left_on=location_column, right_on="주소", how="left")

    return result_df





