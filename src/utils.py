from datetime import timedelta


# funciones útiles
def daterange(starting_date, ending_date):
    """Generar rango de fechas entre las fechas indicadas."""
    for count in range(int((ending_date - starting_date).total_seconds() / 3600)):
        yield starting_date + timedelta(hours=count)


def time_in_range(start, end, x):
    """Comprobar si una fecha está entre las indicadas."""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
