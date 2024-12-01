import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import json
import chardet
from tqdm import tqdm


def convert_dong_type(df, geojson_path):
    import json
    from shapely.geometry import Point
    import geopandas as gpd
    from tqdm import tqdm

    # GeoJSON 파일 로드 (UTF-8 인코딩)
    with open(geojson_path, encoding='utf-8') as f:
        geojson_data = json.load(f)

    # GeoDataFrame으로 변환
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

    # 'dong_name' 필드가 GeoJSON에 포함되어 있어야 함
    if 'dong_name' not in gdf.columns:
        raise ValueError("GeoJSON 파일에 'dong_name' 필드가 포함되어 있지 않습니다.")

    # DataFrame에 '행정동' 열 추가
    df['행정동'] = None

    # 각 행의 경도와 위도를 처리
    for index, row in tqdm(df.iterrows(), desc='법정동-행정동 변환 중...'):
        longitude = row['경도']
        latitude = row['위도']
        point = Point(longitude, latitude)

        # 각 점이 어떤 행정동에 속하는지 판별
        found_dong = None
        for _, geo_row in gdf.iterrows():
            if geo_row['geometry'].contains(point):
                found_dong = geo_row['dong_name']
                break

        # '행정동' 열에 결과 저장
        df.at[index, '행정동'] = found_dong if found_dong else "Unknown"

    # 결과 반환
    return df
