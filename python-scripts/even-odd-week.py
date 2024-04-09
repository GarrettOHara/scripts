import datetime


def is_even_week():
    # Get the current date
    current_date = datetime.datetime.now()

    # Get the ISO week number and year
    iso_year, iso_week, _ = current_date.isocalendar()

    # Calculate the week number within the month
    week_within_month = (current_date.day - 1) // 7 + 1

    # Calculate the total week number within the year
    total_week_within_year = (iso_week - 1) + (week_within_month - 1)

    # Check if the total week number is even
    return total_week_within_year % 2 == 0


if is_even_week():
    print("It's an even week!")
else:
    print("It's an odd week!")
