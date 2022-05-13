

from typing import Iterator


def _find_closest_composite_date(items: list[str], pivot: str) -> str:
    """This function will returns the Modis date in items which is the closest to the Modis
    format date pivot (i.e., AYYYDDD), where DDD is in Day-Of-Year calendar.

        via https://stackoverflow.com/questions/32237862/find-the-closest-date-to-a-given-date

    Parameters
    ----------
    items: list of str
        List of all composite format dates (i.e., AYYYYDDD, e.g., A2022023), where DDD is in Day-Of-Year
        calendar (DOY) format.

    pivot: str
        Composite format date (i.e., YYYYDDD, e.g., A2022014), where DDD is in Day-Of-Year calendar (DOY) format.

    Returns
    -------
    closest: str
        Closest date, in Modis format (i.e., AYYYDDD), of the date pivot.

    """
    pivot: int = int(pivot.replace('A', ''))
    items: list[int] = [int(d.replace('A', '')) for d in items]
    closest: int = min(items, key=lambda x: abs(x - pivot))
    return f'A{closest}'


def compute_date_interval(all_dates: list[str], start_date: str, end_date: str) -> Iterator[str]:
    """This function will returns a Modis dates interval between a 'start date' and 'end date',
    where 'start date' < 'end date', otherwise an error is raised.

    Parameters
    ----------
    all_dates: list of str
        List of Modis dates (i.e., AYYYYDDD, e.g., A2022023).
    start_date: str
        Modis format date (i.e., AYYYYDDD, e.g., A2022014), where DDD is in Day-Of-Year calendar (DOY) format.
    end_date: str
        Modis format date (i.e., AYYYYDDD, e.g., A2020123), where DDD is in Day-Of-Year calendar (DOY) format.

    Yields
    ------
    dates_interval: list of dict
        Returns a date sub-interval of the original date range.

    Raises
    ------
    ValueError
        If 'start date' >= 'end date' an ValueError is raised, because the function receives an argument
        of the correct type but an inappropriate value.

    """
    if int(start_date.replace('A', '')) - int(end_date.replace('A', '')) > 0:
        raise ValueError(f'End date {start_date} is not greater than start date {start_date}.')
    start_closest_date: str = _find_closest_composite_date(items=all_dates, pivot=start_date)
    end_closest_date: str = _find_closest_composite_date(items=all_dates, pivot=end_date)
    # get the list indices for chunk the list
    index_start_closest_date: int = all_dates.index(start_closest_date)
    index_end_closest_date: int = all_dates.index(end_closest_date)
    # chunk the initial list with all modis dates
    dates_range: list[str] = all_dates[index_start_closest_date:index_end_closest_date + 1]
    for data in dates_range:
        yield data
