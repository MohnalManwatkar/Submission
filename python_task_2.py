import pandas as pd


def calculate_distance_matrix(df):
    # distance between toll location
    distance = df.pivot_table(index='id_start', columns='id_end', values='distance', fill_value=0)
    # calculatimg cumulative distances
    cumulative_distances = distance + distance.transpose()

    for col in cumulative_distances.columns:
        for row in cumulative_distances.index:
            if cumulative_distances.loc[row, col] == 0 and row != col:
                intermediate_points = cumulative_distances.loc[row] + cumulative_distances.loc[:, col]
                intermediate_points = intermediate_points[intermediate_points != 0]
                if len(intermediate_points) > 0:
                    cumulative_distances.loc[row, col] = intermediate_points.min()

    cumulative_distances.values[[range(len(cumulative_distances))] * 2] = 0

    return cumulative_distances


import pandas as pd

def unroll_distance_matrix(df):

    unrolled_data = []

    # Iterate through the matrix and capture the indices and values
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            id_start = df.index[i]
            id_end = df.columns[j]
            distance = df.iloc[i, j]
            unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Create a DataFrame from the captured data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

# Example usage:
# Assuming 'distance_matrix' is your distance matrix DataFrame
unrolled_dataframe = unroll_distance_matrix(distance_matrix)
print(unrolled_dataframe)


def find_ids_within_ten_percentage_threshold(df, reference_id):
    # Filter the DataFrame based on the reference ID
    reference_data = df[(df['id_start'] == reference_id) | (df['id_end'] == reference_id)]

    # Calculate the average distance of the reference ID
    avg_distance_reference = reference_data['distance'].mean()

    # Calculate the threshold range (within 10%)
    threshold_lower = avg_distance_reference * 0.9
    threshold_upper = avg_distance_reference * 1.1

    # Filter IDs whose average distance lies within the threshold range
    filtered_ids = df.groupby(['id_start', 'id_end']).agg(avg_distance=('distance', 'mean'))
    filtered_ids = filtered_ids[
        (filtered_ids['avg_distance'] >= threshold_lower) &
        (filtered_ids['avg_distance'] <= threshold_upper) &
        (filtered_ids.index.get_level_values(0) != reference_id) &
        (filtered_ids.index.get_level_values(1) != reference_id)
        ].reset_index()

    return filtered_ids


def calculate_toll_rate(df):
    # Assuming df contains columns like 'vehicle_type', 'distance', 'time', etc. for toll rate calculation
    # You may need to adjust the column names and calculation logic based on your actual DataFrame

    # Define toll rates for different vehicle types (example rates)
    rate = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6  # Example toll rate for trucks (per kilometer or based on other parameters)
        # Add more vehicle types and their corresponding toll rates if needed
    }

    # Calculate toll rates based on vehicle type and other relevant factors
    for vehicle_type, rate in rate.items():
        df[vehicle_type] = df['distance'] * rate

    return df
