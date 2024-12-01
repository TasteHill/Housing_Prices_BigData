import pandas as pd
from Tools import housing_price_preprocessor as hpc
import seaborn as sns
import matplotlib.pyplot as plt
from Tools import location_getter as lg
from Tools import location_type_converter as ltc
from Tools import dong_info_preprocessor as dip

def train_station(apartment_df: pd.DataFrame, api_key):
    plt.rc("font", family="Malgun Gothic")
    sns.set(font="Malgun Gothic",
            rc={"axes.unicode_minus": False}, style='white')

    # 도시철도 데이터 로드
    train_df = pd.read_excel("Datas/철도 데이터/전체_도시철도역사정보_20240930.xlsx")
    train_df = train_df[train_df['역사도로명주소'].str.contains('서울', na=False)]
    print(train_df['역사도로명주소'])

    # 위치 데이터 가져오기
    train_df = lg.get_location(train_df, '역사도로명주소', api_key)
    train_df = ltc.convert_dong_type(train_df, 'Datas/행정구역/hangjeongdong_서울특별시.geojson')

    # train_df[['위도', '경도']]
    # apartment_df[['위도', '경도']]

    apartment_df.dropna(subset='위도',inplace=True)

    # 거리 계산
    apartment_with_distances = calculate_nearest_station(apartment_df, train_df)

    grouped_apartment = apartment_with_distances.groupby('최단역거리')['단위면적가격'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=grouped_apartment, x='최단역거리', y='단위면적가격', alpha=0.7)
    plt.title('가장 가까운 역 거리별 단위면적가격', fontsize=16)
    plt.xlabel('평균 단위면적가격', fontsize=12)
    plt.ylabel('역으로부터 거리', fontsize=12)
    plt.grid(True)
    plt.show()



from geopy.distance import geodesic
from tqdm import tqdm

def calculate_nearest_station(apartment_df: pd.DataFrame, train_df: pd.DataFrame):
    # tqdm으로 아파트 데이터를 순회하며 진행 상황 표시
    nearest_distances = []

    for _, apt_row in tqdm(apartment_df.iterrows(), total=len(apartment_df), desc="아파트-지하철 거리 계산 중"):
        apt_location = (apt_row['위도'], apt_row['경도'])

        # 각 지하철역과의 거리 계산
        distances = train_df.apply(
            lambda station_row: geodesic(apt_location, (station_row['위도'], station_row['경도'])).meters,
            axis=1
        )

        # 가장 가까운 거리 저장
        nearest_distances.append(distances.min())

    # 결과를 새로운 컬럼으로 저장
    apartment_df['최단역거리'] = nearest_distances
    return apartment_df


if __name__ == "__main__":
    # 주택 데이터 전처리
    #df = hpc.housing_monthlyrent_price_preprocessor(3000)
    #train_station()
    train_station(hpc.apartment_trade_preprocessor(3000))