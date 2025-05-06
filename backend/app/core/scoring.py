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

    # TODO: Implement the scoring algorithm
    pass