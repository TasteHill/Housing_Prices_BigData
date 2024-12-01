import pandas as pd
from Tools import housing_price_preprocessor as hpc
import seaborn as sns
import matplotlib.pyplot as plt
from Tools import location_getter as lg
from Tools import location_type_converter as ltc
from Tools import dong_info_preprocessor as dip


def crime(house_df: pd.DataFrame):


    crime_df = pd.read_csv('Datas/강력범죄 데이터/5대+범죄+발생현황_20241130231246.csv', header=3)
    crime_df.drop(0, inplace=True)

    if '행정구' not in crime_df.columns:
        crime_df.rename(columns={'자치구별(2)': '행정구', '발생':'범죄발생건수'}, inplace=True)

    house_df['행정구'] = house_df['시군구'].apply(lambda x: x.split()[1])

    grouped_house_df = house_df.groupby('행정구')['단위면적가격'].mean().reset_index(name='평균단위면적가격')

    merged_df = pd.merge(grouped_house_df, crime_df, how='left', on='행정구')

    print(merged_df)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=merged_df, x='평균단위면적가격', y='범죄발생건수', alpha=0.7)
    plt.title('행정구별 평균 단위면적가격과 범죄발생건수 관계', fontsize=16)
    plt.xlabel('평균 단위면적가격', fontsize=12)
    plt.ylabel('범죄발생건수', fontsize=12)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    df = hpc.housing_monthlyrent_price_preprocessor(3000)
    crime(df)