# importamos todas las librerías
import math
import random
from datetime import timedelta, datetime, time
import numpy as np
import pandas
import logging


# Clase básica Base_Building
class Base_Building:
    def __init__(self, name):
        self.name = name
        self.db = {"datetime": [], "id": [],
                   "pcr": []}  # diccionario con listas par datetime, id de mascarilla y resultado de pcr
        self.occupancy = []  # lista de mascarillas dentro del edificio

    def enter(self, person):
        """Una mascarilla entra en el edificio, registrando su entrada."""
        self.occupancy.append(person)
        person.building = self

    def exit(self, person):
        """Una mascarilla sale del edificio."""
        self.occupancy.remove(person)
        person.building = None

    def contact(self, mod_infection):
        """Las mascarillas presentes entran en contacto, pudiendo infectarse."""
        negative = [person for person in self.occupancy if person.covid == "Negativo"]
        infected_num = len([person for person in self.occupancy if person.covid == "Positivo"])
        for person in negative:
            person.contact(infected_num, mod_infection)

    def update(self):
        """Registra las mascarillas en su base de datos. Se ha de llamar cada hora."""
        for person in self.occupancy:
            self.db["datetime"].append(type(person).current_datetime)
            self.db["id"].append(person.id)
            self.db["pcr"].append(person.pcr)


# clase Home
class Home(Base_Building):
    leave_change = None

    def __init__(self):
        super().__init__("Home")

    def contact(self):
        return None  # nadie se contagia en casa


# clase Building
class Building(Base_Building):
    def __init__(self, name, weight, capacity):
        self.weight = weight  # peso en las probabilidades
        self.capacity = capacity  # número máximo de gente permitida
        super().__init__(name)

    def enter(self, person):
        """Una mascarilla entra en el edificio."""
        if len(self.occupancy) >= self.capacity:  # será necesario usar try
            raise Exception("Edificio Lleno.")
        super().enter(person)


# clase Hospital
class Hospital(Building):
    # todo que el hospital distinga ente pacientes y visitantes
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, visitor_capacity, beds):
        self.beds = beds  # aforo máximo de hospitalizados
        # lista de personas hospitalizadas. self.occupancy muestra a los visitantes,
        # análogamente ocurre con capacity y beds.
        self.hospitalized = []
        super().__init__(name, weight, visitor_capacity)

    def admission(self, person):
        """Un paciente es ingresado."""
        if len(self.hospitalized) >= self.beds:
            raise Exception("Hospital lleno de pacientes.")
        self.hospitalized.append(person)
        person.building = self

    def discharge(self, person):
        """Un paciente es dado de alta."""
        self.hospitalized.remove(person)
        person.building = None

    def contact(self):
        """Contagios entre todos los visitantes del hospital."""
        super().contact(Hospital.mod_infection)  # todo implementar correctamente el contagio en un hospital

    def update(self):
        """Registra a todos los visitantes y enfermos en la base de datos."""
        for person in self.hospitalized:
            self.db["datetime"].append(type(person).current_datetime)
            self.db["id"].append(person.id)
            self.db["pcr"].append(person.pcr)
        super().update()


# clase Pharmacy
class Pharmacy(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().contact(Pharmacy.mod_infection)


# clase Centro Educativo
class Learning_Center(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().contact(Learning_Center.mod_infection)


# clase Workplace
class Workplace(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().contact(Workplace.mod_infection)


# Clase Market
class Market(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().contact(Market.mod_infection)


# Clase Mall
class Mall(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().contact(Market.mod_infection)


# clase Person
class Person:
    p_covid = None  # probabilidad de tener covid al empezar la simulacion
    p_infect = None  # probabilidad de ser infectado durante una hora por una persona positiva
    p_mortality = None  # probabilidad de fallecer por la infección
    hospital_chance = None  # probabilidad de ir al hospital cuando se tiene un pcr positivo
    immunity = None  # días de inmunidad después de recuperarte
    incubation_time = None  # tiempo de incubación
    current_datetime = None  # debe ser actualizada cada hora, e inicializada al principio de la simulación
    building_dict = None  # keys con los tipos de edificios, y los valores son listas de los edificios de cada tipo
    alive = []  # contiene a la gente viva
    dead = []  # contiene a los fallecidos
    home = Home()  # el hogar

    def __init__(self, id):
        self.id = id
        self.building = Person.home  # edificio en el que se encuentra actualmente
        self.isAlive = True  # la persona empieza viva
        Person.alive.append(self)
        # decidimos si empieza infectado o no
        if random.random() > Person.p_covid:
            self.covid = "Negativo"  # si tiene COVID-19 o no
            self.pcr = "Negativo"  # resultado del PCR
            self.pcr_datetime = None  # fecha a partir de la cual empieza a dar positivo en el PCR
            self.recovery_datetime = None  # fecha en la que se recupera, si no fallece
            self.immunity_datetime = None  # fecha en la que se termina la inmunidad
        else:
            self.covid = "Positivo"
            self.pcr = "Negativo"
            self.pcr_datetime = Person.current_datetime + timedelta(days=Person.incubation_time)
            self.recovery_datetime = self.pcr_datetime + timedelta(days=Person.get_disease_length())
            self.immunity_datetime = self.recovery_datetime + timedelta(days=Person.immunity)

    def __enter_home(self):
        """La persona entra en su casa."""
        Person.home.enter(self)

    def back_home(self):
        """La persona vuelve a su casa."""
        if self.building != Person.home:
            # todo esto es feo, arreglar
            if isinstance(self.building, Hospital):
                if self in self.building.hospitalized:
                    return None
            self.building.exit(self)
            self.__enter_home()

    def move(self):
        """La persona se mueve, según sus circunstancias."""
        raise Exception("Método no implementado.")  # se implementa en cada clase hija

    def infect(self):
        """La persona se contagia de COVID-19."""
        logging.debug("persona " + str(self.id) + " ha sido infectada")
        self.covid = "Positivo"
        self.pcr_datetime = Person.current_datetime + timedelta(days=Person.incubation_time)
        self.recovery_datetime = self.pcr_datetime + timedelta(days=Person.get_disease_length())
        self.immunity_datetime = self.recovery_datetime + timedelta(days=Person.immunity)

    def contact(self, number_of_infected, mod_infection):
        """La persona hace contacto con un número de infectados."""
        if self.covid != "Negativo":
            return None
        for i in range(number_of_infected):
            threshold = Person.p_infect * mod_infection
            if random.random() < threshold:
                self.infect()
                return None

    def update(self):
        """Se comprueba el estado de la persona. Se debe llamar cada hora."""
        # vemos si el PCR debe dar positivo
        if Person.current_datetime == self.pcr_datetime:
            self.pcr = "Positivo"
        # si PCR es positivo y no está en un hospital, hay una probabilidad de ser ingresado
        if self.pcr == "Positivo" and not isinstance(self.building,
                                                     Hospital) and random.random() < Person.hospital_chance:
            hospital = Person.select_building("Hospital")
            self.building.exit(self)
            try:
                hospital.admission(self)
            except:
                self.__enter_home()
        # comprobamos si se recupera o fallece
        if Person.current_datetime == self.recovery_datetime:
            self.pcr = "Negativo"
            if random.random() < Person.p_mortality:
                self.isAlive = False
                Person.alive.remove(self)
                Person.dead.append(self)
                # todo es feo, arreglar
                if isinstance(self.building, Hospital):
                    if self in self.building.hospitalized:
                        self.building.discharge(self)
                    else:
                        self.building.exit(self)
                else:
                    self.building.exit(self)
                return None
            else:
                self.covid = "Inmune"
                # todo es feo, arreglar
                # recibe el alta
                if isinstance(self.building, Hospital):
                    if self in self.building.hospitalized:
                        self.building.discharge(self)
                    else:
                        self.building.exit(self)
                else:
                    self.building.exit(self)
                self.__enter_home()
        # comprobamos si pierde la inmunidad
        if Person.current_datetime == self.immunity_datetime:
            self.covid = "Negativo"

    @staticmethod
    def get_disease_length():
        length = 0
        while length <= 10:
            length = np.random.normal(loc=20, scale=7)
        length = math.floor(length)
        return length

    @staticmethod
    def select_building(building_type):
        """Selecciona un edificio del diccionario, dado el tipo, respetando los pesos."""
        return random.choices(population=Person.building_dict[building_type],
                              weights=[element.weight for element in Person.building_dict[building_type]])[0]

    @staticmethod
    def select_type(type_weights_dict):
        """Selecciona un tipo de edificio del diccionario, respetando los pesos."""
        return random.choices(population=list(type_weights_dict.keys()),
                              weights=list(type_weights_dict.values()))[0]

    @staticmethod
    def try_loop(person, max_attempts=5):
        """Una persona intenta ejecutar el método move() de su clase. Si tras varios intentos no logra encontrar un sitio con sitio, se va a casa."""
        # todo es feo, arreglar
        if isinstance(person.building, Hospital):
            if person in person.building.hospitalized:
                return None
        person.at_place = person.building == person.place
        if person.at_place and random.random() > 0.3 * type(person.building).leave_chance:  # todo cambiar esto¿?
            # día normal
            return None
        # ¿se va de donde está?
        if random.random() > type(person.building).leave_chance:
            # se queda donde está
            return None
        person.building.exit(person)
        for attempt in range(max_attempts):
            try:
                # escoger a qué tipo de edificio ir
                # hay que hacer varios intentos en caso de que todos los de ese tipo estén llenos
                building_type = Person.select_type(type(person).type_weights)
                if building_type == "Home":
                    person.__enter_home()
                    return None
                # escoger el edificio
                # hay que hacer varios intentos en caso de que esté lleno
                final_building = Person.select_building(building_type)
                final_building.enter(person)
            except:
                continue
            else:
                break
        else:
            person.__enter_home()


# clase Worker
class Worker(Person):
    type_weights = {"Trabajo": 6, "Hospital": 1, "Farmacia": 3, "Centro Educativo": 5, "Supermercado": 10,
                    "Centro Comercial": 8, "Home": 9}  # peso en las probabilidades sobre a qué tipo de edificio ir

    def __init__(self, id):
        self.place = Person.select_building("Trabajo")
        self.at_place = False
        super().__init__(id)

    def move(self):
        """El trabajador se mueve."""
        Person.try_loop(self)


# clase Student
class Student(Person):
    type_weights = {"Trabajo": 3, "Hospital": 1, "Farmacia": 2, "Centro Educativo": 6, "Supermercado": 3,
                    "Centro Comercial": 4, "Home": 8}  # peso en las probabilidades sobre a qué tipo de edificio ir

    def __init__(self, id):
        self.place = Person.select_building("Centro Educativo")
        self.at_place = False
        super().__init__(id)

    def move(self):
        """El estudiante se mueve."""
        Person.try_loop(self)

    # clase Stay_at_home


class Stay_at_home(Person):
    type_weights = {"Trabajo": 1, "Hospital": 1, "Farmacia": 3, "Centro Educativo": 1, "Supermercado": 6,
                    "Centro Comercial": 7, "Home": 8}  # peso en las probabilidades sobre a qué tipo de edificio ir

    def __init__(self, id):
        self.place = Person.home
        self.at_place = True
        super().__init__(id)

    def move(self):
        """El amo de casa se mueve."""
        Person.try_loop(self)


# funciones útiles
def daterange(start_date, end_date):
    """Generar rango de fechas entre las fechas indicadas."""
    for n in range(int((end_date - start_date).total_seconds() / 3600)):
        yield start_date + timedelta(hours=n)


def time_in_range(start, end, x):
    """Comprobar si una fecha está entre las indicadas."""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def daily_test(people_list, masks_df, data_db):
    """Perform a COVID-19 test and store the result. Call daily"""
    # todo masks_df usa pandas, y eso es lento, usar listas
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
    masks_df[date] = col_masks_df


# iniciamos la ejecución
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG, filename='log.txt', filemode='w', format='%(message)s')

# parámetros de la simulación
random.seed(4862)
n = 5000  # número de gente
person_types = ["Worker", "Student", "Stay at home"]  # probabilidad de tipo de persona
person_weights = [4, 3, 2]

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
Person.p_infect = 0.0001  # probabilidad de ser infectado durante una hora por una persona positiva
Person.p_mortality = 0.034  # probabilidad de fallecer por la infección
Person.hospital_chance = 0.001  # probabilidad de ir al hospital cuando se tiene un pcr positivo
Person.immunity = 30  # días de inmunidad después de recuperarte
Person.incubation_time = 5  # tiempo de incubación
Person.current_datetime = start_date  # debe ser actualizada cada hora

# creamos los edificios en Person.building_dict
# contiene keys con los tipos de edificios, y los valores son listas de los edificios de cada tipo
Person.building_dict = {"Trabajo": [Workplace("Trabajo 1", 1, n * 0.1),
                                    Workplace("Trabajo 2", 1, n * 0.1),
                                    Workplace("Trabajo 3", 2, n * 0.2),
                                    Workplace("Trabajo 4", 2, n * 0.15)],
                        "Hospital": [Hospital("Hospital 1", 2, n * 0.35, n * 0.2),
                                     Hospital("Hospital 2", 3, n * 0.4, n * 0.3)],
                        "Farmacia": [Pharmacy("Farmacia", 3, n * 0.2)],
                        "Centro Educativo": [Learning_Center("Colegio 1", 2, n * 0.2),
                                             Learning_Center("Colegio 2", 2, n * 0.2),
                                             Learning_Center("Universidad", 3, n * 0.3)],
                        "Supermercado": [Market("Supermercado", 3, n * 0.2)],
                        "Centro Comercial": [Mall("Centro Comercial", 1, n * 0.5)],
                        "Home": [Person.home]
                        }

# creamos la gente
Person.alive = []  # borramos la gente de la ejecución anterior
Person.dead = []
for i in range(n):
    person_type = random.choices(population=person_types, weights=person_weights)[0]
    if person_type == "Worker":
        Worker(i)
    elif person_type == "Student":
        Student(i)
    elif person_type == "Stay at home":
        Stay_at_home(i)
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
dataframes = {edificio.name: pandas.DataFrame(columns=["fecha y hora", "id"]) for edificio in edificios}
mascarillas = pandas.DataFrame(index=range(n))
datos = {"Fallecidos": [], "Contagiados": [], "Inmunizados": [], "Fecha": []}

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
        # todos a casa
        for persona in Person.alive:
            persona.back_home()
        # hacemos tests
        datos["Fecha"].append(single_date.date())
        daily_test(poblacion, mascarillas, datos)
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

# guardamos los datos
for edificio in edificios:
    df = pandas.DataFrame.from_dict(edificio.db)
    df.to_csv(edificio.name + ".csv", sep=";")
mascarillas.to_csv("mascarillas.csv", sep=";")
datos_df = pandas.DataFrame.from_dict(datos).set_index("Fecha")
datos_df.to_csv("datos_diarios.csv", sep=";")
print("Terminado.")
