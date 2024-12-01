import pandas as pd
from Tools import housing_price_preprocessor as hpc
import seaborn as sns
import matplotlib.pyplot as plt
from Tools import location_getter as lg
from Tools import location_type_converter as ltc
from Tools import dong_info_preprocessor as dip

def population_density(house_df):
    plt.rc("font", family="Malgun Gothic")
    sns.set(font="Malgun Gothic",
            rc={"axes.unicode_minus": False}, style='white')

    dense_df = pd.read_csv("Datas/인구밀도 데이터/인구밀도_20241129235744.csv", header=1)
    dense_df = dense_df[['동별(3)','인구 (명)','인구밀도 (명/㎢)']]
    dense_df.rename(columns={'동별(3)':'행정동','인구밀도 (명/㎢)':'인구밀도'},inplace=True)

    house_df = house_df.groupby('행정동')['단위면적가격'].mean().reset_index()
    result_dense_df = pd.merge(house_df, dense_df, how='left', on='행정동')
    result_dense_df.fillna(0, inplace=True)


    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=result_dense_df, x='인구밀도', y='단위면적가격', alpha=0.7)
    plt.title('인구밀도별 단위면적가격', fontsize=16)
    plt.xlabel('인구밀도(명/㎢)', fontsize=12)
    plt.ylabel('단위면적가격', fontsize=12)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # 주택 데이터 전처리
    df = hpc.housing_monthlyrent_price_preprocessor(3000)
    population_density(df)