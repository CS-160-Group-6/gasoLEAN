def compute_score(*, distance: float, avg_speed: float, max_speed: float, avg_rpm: float, max_rpm: float, duration: int) -> float:
    '''
    Compute the score for a ride based on various metrics.
    The score is calculated using a weighted formula that takes into account the distance, average speed,
    maximum speed, average RPM, maximum RPM, and duration of the ride.

    :param distance: Distance of the ride in kilometers
    :param avg_speed: Average speed of the ride in km/h
    :param max_speed: Maximum speed of the ride in km/h
    :param avg_rpm: Average revolutions per minute
    :param max_rpm: Maximum revolutions per minute
    :param duration: Duration of the ride in seconds
    :return: Computed score for the ride from 0-100 (higher is better)
    '''

    # Reasonable maximum values for the metrics
    max_distance: float = 200.0  # km
    max_avg_speed: float = 120.0  # km/h
    max_max_speed: float = 180.0  # km/h
    max_avg_rpm: float = 5000.0  # rpm
    max_max_rpm: float = 8000.0  # rpm
    max_duration: int = 4 * 3600  # 4 hours in seconds

    # Normalize the metrics to a scale of 0-1
    # This is important to ensure that all metrics contribute equally to the score and one metric does
    # not dominate the others.
    norm_distance: float = min(distance / max_distance, 1.0)
    norm_avg_speed: float = min(avg_speed / max_avg_speed, 1.0)
    norm_max_speed: float = min(max_speed / max_max_speed, 1.0)
    norm_avg_rpm: float = min(avg_rpm / max_avg_rpm, 1.0)
    norm_max_rpm: float = min(max_rpm / max_max_rpm, 1.0)
    norm_duration: float = min(duration / max_duration, 1.0)

    # Weights for each metric (must add up to 1.0)
    # These weights can be adjusted based on the importance of each metric in the scoring system.
    # For example, if distance is more important than average speed, increase the weight for distance.
    W_DISTANCE: float = 0.10
    W_AVG_SPEED: float = 0.25
    W_MAX_SPEED: float = 0.20
    W_AVG_RPM: float = 0.20
    W_MAX_RPM: float = 0.15
    W_DURATION: float = 0.10

    score: float = (W_DISTANCE * norm_distance +
            W_AVG_SPEED * norm_avg_speed +
            W_MAX_SPEED * norm_max_speed +
            W_AVG_RPM * norm_avg_rpm +
            W_MAX_RPM * norm_max_rpm +
            W_DURATION * (1 - norm_duration)) * 100

    return round(score, 2)