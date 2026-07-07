from datetime import datetime, timedelta


def get_reporting_period():

    print(
        "Enter reporting period (leave both blank for entire history)."
    )

    start_input = input(
        "Start date (YYYY-MM-DD, blank = earliest available): "
    ).strip()

    end_input = input(
        "End date (YYYY-MM-DD, blank = today): "
    ).strip()

    start = (
        _parse_date(start_input)
        if start_input
        else datetime.now() - timedelta(days=365 * 3)
    )

    end = (
        _parse_date(end_input)
        if end_input
        else datetime.now() + timedelta(days=1)
    )

    if start is None:
        start = datetime.now() - timedelta(days=365 * 3)

    if end is None:
        end = datetime.now() + timedelta(days=1)

    return start, end


def _parse_date(value):

    try:
        return datetime.strptime(value, "%Y-%m-%d")

    except ValueError:

        print(
            f"Couldn't parse '{value}' as YYYY-MM-DD — using default instead."
        )

        return None