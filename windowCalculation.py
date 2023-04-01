import numpy as np
import math

class Stop:
    def __init__(self, stop_number, coordinates, expected_arrival=None, expected_departure=None,
                 wait_time=None, actual_arrival=None, actual_departure=None, skipped=False):
        self.stop_number = stop_number
        self.coordinates = coordinates
        self.expected_arrival = expected_arrival
        self.expected_departure = expected_departure
        self.wait_time = wait_time
        self.actual_arrival = actual_arrival
        self.actual_departure = actual_departure
        self.skipped = skipped

def time_str_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time_str(minutes):
    am_pm = 'AM' if (minutes // 60) % 24 < 12 else 'PM'
    return f"{(minutes // 60) % 12:02d}:{minutes % 60:02d} {am_pm}"


def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad

    a = math.sin(d_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def calculate_total_variance(current_variance_travel, current_variance_wait, previous_variance, correlation_matrix):
    current_variance = current_variance_travel + current_variance_wait
    covariance = correlation_matrix[0, 1] * np.sqrt(previous_variance * current_variance)
    return previous_variance + current_variance + 2 * covariance

def calculate_arrival_time_window(current_time, remaining_travel_time, wait_time, cumulative_variance):
    expected_arrival_time = current_time + remaining_travel_time + wait_time
    std_dev = np.sqrt(cumulative_variance)
    min_expected_time = expected_arrival_time - 1 * std_dev
    max_expected_time = expected_arrival_time + 1 * std_dev
    return min_expected_time, max_expected_time

def predict_arrival_time_windows(vehicle_coordinates, stops, current_time, speed, std_dev_travel=0.5, std_dev_wait=0.5, correlation_matrix=None):
    if correlation_matrix is None:
        correlation_matrix = np.eye(2)

    arrival_time_windows = []
    total_variance = 0
    current_time_minutes = time_str_to_minutes(current_time)
    
    for i, stop in enumerate(stops):
        if i == 0: # Skip the first stop (starting point)
            continue
            
        distance_to_stop = haversine_distance(vehicle_coordinates, stop.coordinates)
        remaining_travel_time = distance_to_stop / speed * 60

        if stop.actual_arrival and not stop.skipped:
            arrival_time_windows.append((stop.actual_arrival, stop.actual_arrival))
            continue

        wait_time = stop.wait_time or 0

        variance_travel = std_dev_travel ** 2
        variance_wait = std_dev_wait ** 2
        total_variance = calculate_total_variance(variance_travel, variance_wait, total_variance, correlation_matrix)

        time_window = calculate_arrival_time_window(current_time_minutes, remaining_travel_time, wait_time, total_variance)

        if stop.skipped:
            # Calculate time window assuming the vehicle returns to the skipped stop after the next stop
            if i + 1 < len(stops):
                next_stop = stops[i + 1]
                distance_to_next_stop = haversine_distance(vehicle_coordinates, next_stop.coordinates)
                remaining_travel_time_to_next_stop = distance_to_next_stop / speed * 60
                time_window_return = calculate_arrival_time_window(current_time_minutes + remaining_travel_time_to_next_stop, remaining_travel_time, wait_time, total_variance)
                time_window_return = (minutes_to_time_str(int(time_window_return[0])), minutes_to_time_str(int(time_window_return[1])))
            else:
                time_window_return = ('N/A', 'N/A')

            # Calculate time window assuming the vehicle continues to the subsequent stops
            time_window_continue = (minutes_to_time_str(int(time_window[0])), minutes_to_time_str(int(time_window[1])))

            time_window = (time_window_return, time_window_continue)
        else:
            time_window = (minutes_to_time_str(int(time_window[0])), minutes_to_time_str(int(time_window[1])))
        
        arrival_time_windows.append(time_window)

    return arrival_time_windows



def print_arrival_time_windows(arrival_time_windows, stops):
    print("Stop Number | Min Expected Arrival | Max Expected Arrival")
    print("-------------------------------------------------------")
    for stop, time_window in zip(stops[1:], arrival_time_windows):
        if isinstance(time_window[0], tuple):  # Skipped stop with two time windows
            min_expected_arrival_return, max_expected_arrival_return = time_window[0]
            min_expected_arrival_continue, max_expected_arrival_continue = time_window[1]
            print(f"{stop.stop_number:^11} | {min_expected_arrival_return:^19}/{min_expected_arrival_continue:^19} | {max_expected_arrival_return:^19}/{max_expected_arrival_continue:^19}")
        else:
            min_expected_arrival, max_expected_arrival = time_window
            print(f"{stop.stop_number:^11} | {min_expected_arrival:^19} | {max_expected_arrival:^19}")




# Mock data
stops = [
    Stop(0, (40.7128, -74.0060), expected_departure="08:00"),
    Stop(1, (40.7138, -74.0070), expected_arrival="08:30", expected_departure="08:35", wait_time=5, skipped=True),
    Stop(2, (40.7148, -74.0080), expected_arrival="09:10", expected_departure="09:15", wait_time=5, actual_arrival="09:10", actual_departure="09:15"),
    Stop(3, (40.7158, -74.0090), expected_arrival="09:50")
]

vehicle_coordinates = (40.7128, -74.0060)  # Vehicle's current GPS coordinates (latitude, longitude)
speed = 30
std_dev_travel_minutes = 0.5 * 60
std_dev_wait_minutes = 0.5 * 60
current_time = "08:45"

# Test
arrival_time_windows = predict_arrival_time_windows(vehicle_coordinates, stops, current_time, speed, std_dev_travel_minutes, std_dev_wait_minutes)
print(arrival_time_windows)
print_arrival_time_windows(arrival_time_windows, stops)
