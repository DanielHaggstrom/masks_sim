from datetime import time
import pandas
from people import *
from utils import *


# iniciamos la ejecución
def main():
    print("Empieza main.")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, filename='log.txt', filemode='w', format='%(message)s')

    # parámetros de la simulación
    random.seed(4862)
    n = 50000  # número de gente
    person_types = ["Worker", "Student", "Stay at home"]  # probabilidad de tipo de persona
    person_weights = [8, 2, 3]

    start_date = datetime(2020, 3, 1)
    end_date = datetime(2020, 12, 1)

    Hospital.mod_infection = 5
    Pharmacy.mod_infection = 1.3
    Learning_Center.mod_infection = 1.1
    Workplace.mod_infection = 0.8
    Market.mod_infection = 1
    Mall.mod_infection = 1.2

    Home.leave_chance = 0.3
    Hospital.leave_chance = 0.7
    Pharmacy.leave_chance = 0.8
    Learning_Center.leave_chance = 0.1
    Workplace.leave_chance = 0.1
    Market.leave_chance = 0.6
    Mall.leave_chance = 0.4

    Person.p_covid = 0.01  # probabilidad de tener covid al empezar la simulacion
    # probabilidades de que alguien positivo sea asintomático, tenga severidad baja o alta
    Person.covid_chances = [0.2, 0.95]
    Person.p_infect = 0.00001  # probabilidad de ser infectado durante una hora por una persona positiva
    Person.p_mortality = 0.034  # probabilidad de fallecer por la infección
    Person.go_home_chance = 0.6  # probabilidad de irse a casa si tiene un pcr positivo y caso leve
    Person.hospital_chance = 0.9  # probabilidad de ir al hospital cuando se tiene un pcr positivo y es un caso grave
    Person.current_datetime = start_date  # debe ser actualizada cada hora

    # creamos los edificios en Person.building_dict
    # contiene keys con los tipos de edificios, y los valores son listas de los edificios de cada tipo
    Person.building_dict = {"Trabajo": [Workplace("Trabajo 1", 1, n * 0.2),
                                        Workplace("Trabajo 2", 1, n * 0.2),
                                        Workplace("Trabajo 3", 2, n * 0.2),
                                        Workplace("Trabajo 4", 2, n * 0.15)],
                            "Hospital": [Hospital("Hospital 1", 2, n * 0.35, n * 0.2),
                                         Hospital("Hospital 2", 3, n * 0.4, n * 0.3)],
                            "Farmacia": [Pharmacy("Farmacia 1", 3, n * 0.2)],
                            "Centro Educativo": [Learning_Center("Colegio 1", 2, n * 0.2),
                                                 Learning_Center("Colegio 2", 2, n * 0.2),
                                                 Learning_Center("Universidad", 3, n * 0.35)],
                            "Supermercado": [Market("Supermercado 1", 3, n * 0.2),
                                             Market("Supermercado 2", 1, n * 0.1)],
                            "Centro Comercial": [Mall("Centro Comercial", 1, n * 0.5)],
                            "Home": [Person.home]
                            }

    # creamos la gente
    Person.alive = []  # borramos la gente de la ejecución anterior
    Person.dead = []
    for num in range(n):
        person_type = random.choices(population=person_types, weights=person_weights)[0]
        if person_type == "Worker":
            Worker(num)
        elif person_type == "Student":
            Student(num)
        elif person_type == "Stay at home":
            Stay_at_home(num)
    Person.home.occupancy = Person.alive.copy()
    poblacion = Person.alive.copy()

    # horas umbrales
    hora_limite_1 = time(22, 0, 0)
    hora_limite_2 = time(8, 0, 0)

    # obtenemos una lista de edificios
    edificios = []
    for value in Person.building_dict.values():
        edificios.extend(value)

    # creamos los dataframes
    mascarillas = {"id": [mask for mask in range(n)]}
    datos_gravedad = mascarillas.copy()
    datos = {"Fallecidos": [], "Contagiados": [], "Inmunizados": [], "Fecha": [], "Asintomáticos": [],
             "Casos leves": [], "Casos graves": []}
    pos_por_edificio = {"fecha": []}
    for edificio in edificios:
        pos_por_edificio[edificio.name] = []

    # iniciamos la simulación
    print("Empezando simulación.")
    for single_date in daterange(start_date, end_date):
        Person.current_datetime = single_date
        for persona in Person.alive:
            persona.update()
        for edificio in edificios:
            edificio.update()

        # comprobamos si son entre las 22:00 y las 08:00 inclusive
        hour = time(single_date.hour, 0, 0)

        if hour == hora_limite_1:
            if len(datos["Fallecidos"]) > 0:
                print(str(single_date) + " " + str(datos["Fallecidos"][-1]) + " " + str(datos["Contagiados"][-1]))
            # todos a casa
            for persona in Person.alive:
                persona.back_home()
            # hacemos tests
            datos["Fecha"].append(single_date.date())
            daily_test(poblacion, mascarillas, datos_gravedad, datos, edificios, pos_por_edificio)
            continue

        if time_in_range(hora_limite_1, hora_limite_2, hour):
            # nadie se mueve
            pass
        else:
            # todos se mueven
            for persona in Person.alive:
                persona.move()
            for edificio in edificios:
                edificio.contact()

    print("Guardando datos.")
    # guardamos los datos
    for edificio in edificios:
        df = pandas.DataFrame.from_dict(edificio.db)
        df.to_csv(edificio.name + ".csv", sep=";")
    mascarillas = pandas.DataFrame.from_dict(mascarillas).set_index("id")
    mascarillas.to_csv("mascarillas.csv", sep=";")
    datos_df = pandas.DataFrame.from_dict(datos).set_index("Fecha")
    datos_df.to_csv("datos_diarios.csv", sep=";")
    pos_por_edificio_df = pandas.DataFrame.from_dict(pos_por_edificio).set_index("fecha")
    pos_por_edificio_df.to_csv("positivos_por_edificio.csv", sep=";")
    datos_gravedad = pandas.DataFrame.from_dict(datos_gravedad).set_index("id")
    datos_gravedad.to_csv("datos_gravedad.csv", sep=";")
    print("Terminado.")


main()
