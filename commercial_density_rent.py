import plotly
import plotly.graph_objects as go
import pandas as pd
from Tools import housing_price_preprocessor as hpc
import seaborn as sns
import matplotlib.pyplot as plt
from Tools import location_getter as lg
from Tools import location_type_converter as ltc
from Tools import dong_info_preprocessor as dip


def calculate_density_rent(api_key):
    plt.rc("font", family="Malgun Gothic")
    sns.set(font="Malgun Gothic",
            rc={"axes.unicode_minus": False}, style='white')

    df = pd.read_excel('Datas/전월세 데이터/단독다가구(전월세)_실거래가_20241129172557.xlsx', header=12)
    df['구_추출'] = df['시군구'].apply(lambda x: ' '.join(x.split()[1:2]))
    df['상세주소'] = df['구_추출'] + ' ' + df['도로명']
    df = df.iloc[:10000]

    df = lg.get_location(df, '상세주소', api_key)
    df = ltc.convert_dong_type(df, 'Datas/행정구역/hangjeongdong_서울특별시.geojson')

    df = df[df['전월세구분'] == '월세']
    df['단위면적가격'] = df['월세금(만원)'] / df['계약면적(㎡)']

    df2 = pd.read_csv('Datas/상권데이터/소상공인시장진흥공단_상가(상권)정보_서울_202406.csv')
    df2_grouped = df2.groupby('행정동명').size().reset_index(name='상권개수')

    area_df = dip.load_dong_info()

    density_df = pd.merge(df2_grouped, area_df, left_on='행정동명', right_on='행정동', how='inner')
    density_df['상권밀도'] = density_df['상권개수'] / density_df['면적']

    df_grouped = df.groupby('행정동')['단위면적가격'].mean().reset_index(name='평균단위면적가격')
    final_df = pd.merge(df_grouped, density_df, on='행정동', how='inner')

    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=final_df, x='상권밀도', y='평균단위면적가격', hue='상권개수', size='상권개수', sizes=(50, 200), palette='viridis',
                    alpha=0.8)
    plt.title('상권 밀도와 평균 단위면적 가격의 관계', fontsize=16)
    plt.xlabel('상권 밀도 (개/k㎡)', fontsize=12)
    plt.ylabel('평균 단위면적 가격 (만원/㎡)', fontsize=12)
    plt.legend(title='상권 개수', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(final_df.head())
    final_df.to_csv('output_density_rent.csv', index=False)


def academy(house_df: pd.DataFrame):
    academy_df = pd.read_csv('Datas/상권데이터/소상공인시장진흥공단_상가(상권)정보_서울_202406.csv')

    academy_grouped = academy_df.groupby(['행정동명', '상권업종대분류명']).size().reset_index(name='업종개수')

    house_df = house_df.groupby('행정동')['단위면적가격'].mean().reset_index()

    merged_df = pd.merge(house_df, academy_grouped, how='left', left_on='행정동', right_on='행정동명')

    merged_df['업종개수'].fillna(0, inplace=True)

    unique_categories = merged_df['상권업종대분류명'].dropna().unique()
    data_by_category = {
        category: merged_df[merged_df['상권업종대분류명'] == category]
        for category in unique_categories
    }

    first_category = unique_categories[0]
    initial_data = data_by_category[first_category]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=initial_data['업종개수'],
        y=initial_data['단위면적가격'],
        mode='markers',
        marker=dict(size=10, opacity=0.7),
        name=first_category,
        text=initial_data['행정동명'],
        hovertemplate='<b>행정동:</b> %{text}<br>' +
                      '<b>업종 개수:</b> %{x}<br>' +
                      '<b>평균 단위면적가격:</b> %{y}<extra></extra>'
    ))

    dropdown_buttons = [
        dict(
            label=category,
            method='update',
            args=[
                {'x': [data_by_category[category]['업종개수']],
                 'y': [data_by_category[category]['단위면적가격']],
                 'text': [data_by_category[category]['행정동명']]}, 
                {'title': f'대분류: {category}'}
            ]
        )
        for category in unique_categories
    ]

    fig.update_layout(
        title=f'대분류: {first_category}',
        xaxis_title='업종 개수',
        yaxis_title='평균 단위면적가격',
        plot_bgcolor='lightgray',
        paper_bgcolor='whitesmoke', 
        template='plotly_white',
        updatemenus=[
            dict(
                buttons=dropdown_buttons,
                direction='down',
                showactive=True
            )
        ]
    )

    # 그래프 표시
    fig.show()



if __name__ == "__main__":
    academy(hpc.apartment_trade_preprocessor(3000))