import pandas as pd


def genrate_car_matrix(dataset):
    df = pd.read_csv(dataset)

    pivot_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    #     for digonal values with 0
    for i in range(min(pivot_df.shape)):
        pivot_df.iloc[i, i] = 0

    return pivot_df
matrix = genrate_car_matrix('dataset-1.csv')
print(matrix)


def get_type_count(df: pd.DataFrame) -> dict:
    condition = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]

    choices = ['low', 'medium', 'high']

    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=choices)

    car_type_counts = df['car_type'].value_counts().sort_index().to_dict()
    return car_type_counts


def get_bus_indexes(df: pd.DataFrame) ->list:
    mean_bus = df['bus'].mean()
    df_index = df[df['bus']>2*mean_bus].index.tolist()
    df_index.sort()
    return df_index


def filter_routes(df: pd.DataFrame)->list:
    avg_truck_route = df.groupby('route')['truck'].mean()
    filtered_routes = avg_truck_route[avg_truck_route > 7].index.tolist()
    filtered_routes.sort()
    return filtered_routes


def maultiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    # from question 1
    matrix = new_df

    matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25 if x <= 20 and x >= 20 else x)
    matrix = new_matrix.round(1)
    return matrix

multiply_matrix(matrix).fillna(0)


def time_check(df):
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')
    df = df[(df['start_timestamp'].notnull()) & (df['end_timestamp'].notnull())]
    # calculate duration for each timestamp pair
    df['duration'] = df['end_timestamp'] - df['start_timestamp']

    # Groupby (id,id_2) and checking the duration for each timestamp
    completeness_check = df.groupby(['id', 'id_2']).apply(
        lambda x: (x['duration'].min() >= pd.Timedelta(days=1)) & (len(x['startDay'].unique()) == 7)
    )
    return completeness_check
