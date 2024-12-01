import pandas as pd
from Tools import housing_price_preprocessor as hpc
import seaborn as sns
import matplotlib.pyplot as plt
from Tools import location_getter as lg
from Tools import location_type_converter as ltc
from Tools import dong_info_preprocessor as dip

def construction_year(house_df:pd.DataFrame):
    plt.rc("font", family="Malgun Gothic")
    sns.set(font="Malgun Gothic",
            rc={"axes.unicode_minus": False}, style='white')

    house_df = house_df.dropna(subset='건축년도')
    grouped_house_df = house_df.groupby('행정동').agg(
        평균건축년도=('건축년도', 'mean'),
        평균단위면적가격=('단위면적가격', 'mean')
    )


    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=grouped_house_df, x='평균건축년도', y='평균단위면적가격', alpha=0.7)
    plt.title('행정동별 평균 건축년도와 평균 단위면적가격', fontsize=16)
    plt.xlabel('평균건축년도', fontsize=12)
    plt.ylabel('평균단위면적가격', fontsize=12)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # 주택 데이터 전처리
    #df = hpc.housing_monthlyrent_price_preprocessor(3000)
    construction_year(hpc.apartment_trade_preprocessor(3000))