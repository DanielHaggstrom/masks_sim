from people import *


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


def daily_test(people_list, masks_dict, data_db):
    """Realizar un test de COVID-19 y guardar los resultados. Llamar cada día."""
    date = Person.current_datetime.date()
    col_masks_df = []
    for person in people_list:
        if person.isAlive is False:
            col_masks_df.append(-1)
        elif person.pcr == "Positivo":
            col_masks_df.append(1)
        else:
            col_masks_df.append(0)
    data_db["Fallecidos"].append(col_masks_df.count(-1))
    data_db["Contagiados"].append(col_masks_df.count(1))
    data_db["Inmunizados"].append(len([x for x in people_list if x.covid == "Inmune"]))
    masks_dict[date] = col_masks_df
