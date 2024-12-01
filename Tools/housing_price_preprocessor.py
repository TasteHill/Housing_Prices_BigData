import os
import pandas as pd
from Tools import location_getter as lg
from Tools import location_type_converter as ltc

def get_files(house_type):
    # Main.py 경로
    base_dir = os.getcwd()
    filepath = os.path.join(base_dir, 'Datas', '전월세 데이터', house_type)
    filelist = []

    if os.path.exists(filepath):
        for root, dirs, files in os.walk(filepath):
            for file in files:
                filelist.append(os.path.join(root, file))
    else:
        print(f"Directory '{filepath}' does not exist.")
    return filelist

def housing_monthlyrent_price_preprocessor(count, api_key):
    filelist = get_files('단독다가구')

    # 빈 데이터프레임 초기화
    combined_df = pd.DataFrame()


    # 파일 하나씩 읽어와서 합치기
    for file in filelist:
        try:
            df = pd.read_excel(file, header=12)
            df.dropna(subset='도로명',inplace=True)
            df = df[df['전월세구분'] == '월세']
            df['월세금(만원)'] = df['월세금(만원)'].str.replace(",", "").astype(float)  # 쉼표 제거 후 float 변환
            df['계약면적(㎡)'] = df['계약면적(㎡)'].astype(float)  # float 변환
            df['단위면적가격'] = df['월세금(만원)'] / df['계약면적(㎡)']
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    # 데이터 제한
    combined_df = combined_df.iloc[:count]

    # 상세주소로 위도, 경도 데이터 가져오기
    combined_df = lg.get_location(combined_df, '도로명', api_key)
    combined_df = ltc.convert_dong_type(combined_df, 'Datas/행정구역/hangjeongdong_서울특별시_with_dong_name.geojson')

    # 이상치 제거
    Q1 = combined_df['단위면적가격'].quantile(0.25)
    Q3 = combined_df['단위면적가격'].quantile(0.75)
    IQR = Q3 - Q1
    combined_df = combined_df[(combined_df['단위면적가격'] >= (Q1 - 1.5 * IQR)) &
                              (combined_df['단위면적가격'] <= (Q3 + 1.5 * IQR))]

    # 결측값 제거
    combined_df.dropna(how='any',subset=['단위면적가격','경도','위도','행정동'],inplace=True)

    combined_df.to_csv('Datas/Refined_Datas/rent_df.csv')
    return combined_df




def apartment_trade_preprocessor(count, api_key):
    df = pd.read_excel('Datas/아파트 매매 데이터/아파트(매매)_실거래가_20241201000540.xlsx',header=12)
    df = df.iloc[:count]

    df['거래금액(만원)'] = df['거래금액(만원)'].str.replace(",", "").astype(float)  # 쉼표 제거 후 float 변환
    df['전용면적(㎡)'] = df['전용면적(㎡)'].astype(float)  # float 변환

    df['단위면적가격'] = df['거래금액(만원)'] / df['전용면적(㎡)']

    df = lg.get_location(df, '도로명', api_key)
    df = ltc.convert_dong_type(df, 'Datas/행정구역/hangjeongdong_서울특별시_with_dong_name.geojson')

    df.dropna(how='any',subset=['단위면적가격','경도','위도','행정동'],inplace=True)

    df.to_csv('Datas/Refined_Datas/apartment_df.csv')

    return df


if __name__ == "__main__":
    print(apartment_trade_preprocessor(100))