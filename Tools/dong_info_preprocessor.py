import pandas as pd


def load_dong_info():
    # 행정구역 면적 데이터 로드 및 처리
    area_df = pd.read_csv('Datas/행정구역 면적 데이터/행정구역(동별)_20241128003145.csv', header=2)
    area_df.drop(columns=['동별(1)', '동별(2)'], axis=1, inplace=True)
    area_df.rename(columns={'동별(3)': '행정동', '면적 (k㎡)': '면적'}, inplace=True)
    area_df = area_df[area_df['행정동'] != '소계']  # '소계' 제거
    return area_df