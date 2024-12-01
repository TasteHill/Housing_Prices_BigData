import pandas as pd
from Tools import housing_price_preprocessor as hpc
import seaborn as sns
import matplotlib.pyplot as plt
from Tools import location_getter as lg
from Tools import location_type_converter as ltc
from Tools import dong_info_preprocessor as dip

def large_scale_store(house_df, api_key):
    plt.rc("font", family="Malgun Gothic")
    sns.set(font="Malgun Gothic",
            rc={"axes.unicode_minus": False}, style='white')

    store_df = pd.read_csv('Datas/대규모점포 데이터/서울시 대규모점포 인허가 정보.csv', encoding='ansi')
    store_df = store_df[['인허가일자', '사업장명', '도로명주소']]

    store_df = lg.get_location(store_df, '도로명주소', api_key)

    store_df = ltc.convert_dong_type(store_df, 'Datas/행정구역/hangjeongdong_서울특별시.geojson')

    grouped_store_df = store_df.groupby('행정동').size().reset_index(name='대형점포수')

    area_df = dip.load_dong_info()
    dong_df = area_df[['행정동']].copy()

    result_store_count_df = pd.merge(dong_df, grouped_store_df, how='left', on='행정동')
    result_store_count_df.fillna(0, inplace=True)

    house_df = house_df.groupby('행정동')['단위면적가격'].mean().reset_index()
    combined_df = pd.merge(house_df,result_store_count_df , how='left', on='행정동')
    combined_df.fillna(0, inplace=True)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=combined_df, x='대형점포수', y='단위면적가격', alpha=0.7)
    plt.title('대형점포 수별 단위면적가격', fontsize=16)
    plt.xlabel('대형점포 수', fontsize=12)
    plt.ylabel('단위면적가격', fontsize=12)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    df = hpc.housing_monthlyrent_price_preprocessor(3000)
    large_scale_store(df)