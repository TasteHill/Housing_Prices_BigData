import pandas as pd
from Tools import housing_price_preprocessor as hpc
import seaborn as sns
import matplotlib.pyplot as plt
from Tools import dong_info_preprocessor as dip

def university_dense_rent(house_df):
    # 대학 정보 데이터 로드 및 처리
    univ_df = pd.read_csv('Datas/대학정보 데이터/서울시 대학 및 전문대학 DB 정보 (한국어).csv')
    univ_df = univ_df[['학교명', '학교종류', '주소', '행정동']]
    univ_df = univ_df.dropna()

    # 집 데이터 그룹화
    house_df = house_df.dropna()
    grouped_house_df = house_df.groupby('행정동')['단위면적가격'].mean().reset_index()

    # 대학 데이터 그룹화
    grouped_univ_df = univ_df.groupby('행정동').size().reset_index(name='대학개수')

    # 행정구역 면적 데이터 로드 및 처리
    area_df = dip.load_dong_info()

    # 행정동 데이터 준비
    dong_df = area_df[['행정동']].copy()

    # 대학 개수 데이터 병합
    result_univ_count_df = pd.merge(dong_df, grouped_univ_df, how='left', on='행정동')
    result_univ_count_df.fillna(0, inplace=True)

    # 대학 개수와 단위면적가격 데이터 병합
    combined_df = pd.merge(result_univ_count_df, grouped_house_df, how='left', on='행정동')
    combined_df.fillna(0, inplace=True)

    # 스캐터 플롯 그리기
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=combined_df, x='대학개수', y='단위면적가격', alpha=0.7)
    plt.title('대학 개수별 단위면적가격', fontsize=16)
    plt.xlabel('대학 개수', fontsize=12)
    plt.ylabel('단위면적가격', fontsize=12)
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    df = hpc.housing_monthlyrent_price_preprocessor(300)
    university_dense_rent(df)