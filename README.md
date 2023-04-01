# Vehicle Arrival Time Prediction

This Python script predicts arrival time windows for vehicles at various stops based on current location, speed, and other factors such as wait times and travel time uncertainties. It also takes into account skipped stops and provides alternative arrival time windows.

## Features

- Calculate Haversine distance between two coordinates (latitude and longitude)
- Convert time strings (HH:MM) to minutes and vice versa
- Predict arrival time windows for vehicle stops, taking into account uncertainties and correlations
- Handle skipped stops by providing alternative arrival time windows
- Print arrival time windows in a formatted table

## Installation

No additional packages are required for this script, just make sure you have Python 3.x installed.

## Usage

1. Define your `Stop` objects with the required attributes. For example:

```python
stops = [
    Stop(0, (40.7128, -74.0060), expected_departure="08:00"),
    Stop(1, (40.7138, -74.0070), expected_arrival="08:30", expected_departure="08:35", wait_time=5, skipped=True),
    Stop(2, (40.7148, -74.0080), expected_arrival="09:10", expected_departure="09:15", wait_time=5, actual_arrival="09:10", actual_departure="09:15"),
    Stop(3, (40.7158, -74.0090), expected_arrival="09:50")
]
```

2. Set the current vehicle coordinates, speed, and current time:
    
```python
vehicle_coordinates = (40.7128, -74.0060)  # Vehicle's current GPS coordinates (latitude, longitude)
speed = 30
std_dev_travel_minutes = 0.5 * 60
std_dev_wait_minutes = 0.5 * 60
current_time = "08:45"
```

3. Call the predict_arrival_time_windows function with the required parameters:

```python
arrival_time_windows = predict_arrival_time_windows(vehicle_coordinates, stops, current_time, speed, std_dev_travel_minutes, std_dev_wait_minutes)
```

4. Print the arrival time windows in a formatted table:

```python
print_arrival_time_windows(arrival_time_windows, stops)
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

