import random
import math
from datetime import timedelta
import logging
import numpy as np
from buildings import *
from errors import *


class Covid:
    """Constantes que representan los distintos niveles de severidad de la enfermedad."""
    NEGATIVE = "NEGATIVE"
    ASINTOMATIC = "ASINTOMATIC"
    LOW = "LOW"
    HIGH = "HIGH"
    IMMUNE = "IMMUNE"


class PCR:
    """Constantes del test PCR."""
    NEGATIVE = False
    POSITIVE = True


# clase Person
class Person:
    p_covid = None  # probabilidad de tener covid al empezar la simulacion
    p_infect = None  # probabilidad de ser infectado durante una hora por una persona positiva
    p_mortality = None  # probabilidad de fallecer por la infección
    hospital_chance = None  # probabilidad de ir al hospital cuando se tiene un pcr positivo
    current_datetime = None  # debe ser actualizada cada hora, e inicializada al principio de la simulación
    building_dict = None  # keys con los tipos de edificios, y los valores son listas de los edificios de cada tipo
    covid_chances = {}
    alive = []  # contiene a la gente viva
    dead = []  # contiene a los fallecidos
    home = Home()  # el hogar

    def __init__(self, id):
        self.id = id
        self.current_building = Person.home  # edificio en el que se encuentra actualmente
        self.isAlive = True  # la persona empieza viva
        self.isHospitalized = False  # no empieza en el hospital
        Person.alive.append(self)
        self.buildings = {k: [math.ceil(random.triangular(0, 5, 2)) * x.weight for x in v]
                          for k, v in Person.building_dict.items()}
        # decidimos si empieza infectado o no, y con qué severidad
        self.covid = Person.__covid_decider()
        self.pcr = PCR.NEGATIVE
        if self.covid == Covid.NEGATIVE:
            self.pcr_datetime = None  # fecha a partir de la cual empieza a dar positivo en el PCR
            self.recovery_datetime = None  # fecha en la que se recupera, si no fallece
            self.immunity_datetime = None  # fecha en la que se termina la inmunidad
        else:
            self.pcr_datetime = Person.current_datetime + timedelta(days=Person.__get_incubation_length())
            self.recovery_datetime = self.pcr_datetime + timedelta(days=Person.__get_disease_length())
            self.immunity_datetime = self.recovery_datetime + timedelta(days=Person.__get_immunity_length())

    def __enter_home(self):
        """La persona entra en su casa."""
        Person.home.enter(self)

    def back_home(self):
        """La persona vuelve a su casa."""
        if self.current_building != Person.home:
            if self.isHospitalized:  # si está en el hospital, se queda allí
                return None
            self.current_building.exit(self)
            self.__enter_home()

    def move(self):
        """La persona se mueve, según sus circunstancias."""
        raise NotImplementedError("Método no implementado.")  # se implementa en cada clase hija

    def infect(self):
        """La persona se contagia de COVID-19."""
        logging.debug("persona " + str(self.id) + " ha sido infectada")
        self.covid = Person.__covid_decider(True)
        self.pcr_datetime = Person.current_datetime + timedelta(days=Person.__get_incubation_length())
        self.recovery_datetime = self.pcr_datetime + timedelta(days=Person.__get_disease_length())
        self.immunity_datetime = self.recovery_datetime + timedelta(days=Person.__get_immunity_length())

    def contact(self, number_of_infected, mod_infection):
        """La persona hace contacto con un número de infectados."""
        if self.covid != Covid.NEGATIVE:
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
            self.pcr = PCR.POSITIVE
        # si PCR es positivo y no está en un hospital, hay una probabilidad de ser ingresado
        if self.pcr == PCR.POSITIVE and not self.isHospitalized and\
                self.covid == Covid.HIGH and random.random() < Person.hospital_chance:
            hospital = Person.select_building(self, "Hospital")
            self.current_building.exit(self)
            try:
                hospital.admission(self)
            except FullBuilding:
                self.__enter_home()
        if self.pcr == PCR.POSITIVE and self.covid == Covid.LOW:
            self.back_home()
        # comprobamos si se recupera o fallece
        if Person.current_datetime == self.recovery_datetime:
            self.pcr = PCR.NEGATIVE
            if self.covid == Covid.HIGH and random.random() < Person.p_mortality:
                self.isAlive = False
                Person.alive.remove(self)
                Person.dead.append(self)
                if self.isHospitalized:
                    self.current_building.discharge(self)
                else:
                    self.current_building.exit(self)
                return None
            else:
                self.covid = Covid.IMMUNE
                # recibe el alta
                if self.isHospitalized:
                    self.current_building.discharge(self)
                else:
                    self.current_building.exit(self)
                self.__enter_home()
        # comprobamos si pierde la inmunidad
        if Person.current_datetime == self.immunity_datetime:
            self.covid = Covid.NEGATIVE

    @staticmethod
    def __get_disease_length():
        # todo cambiar para una longitud más realista
        length = 0
        while length <= 10:
            length = np.random.normal(loc=20, scale=7)
        length = math.floor(length)
        return length

    @staticmethod
    def __get_incubation_length():
        # todo cambiar para una longitud más realista
        length = 0
        while length <= 5:
            length = np.random.normal(loc=9, scale=2)
        length = math.floor(length)
        return length

    @staticmethod
    def __get_immunity_length():
        # todo cambiar para una longitud más realista
        length = 0
        while length <= 140:
            length = np.random.normal(loc=170, scale=30)
        length = math.floor(length)
        return length

    @staticmethod
    def __covid_decider(skip=False):
        """Decide si una persona tiene COVID-19 y la severidad."""
        # las probabilidades de la severidad asumen que la persona ya tiene coronavirus
        if random.random() > Person.p_covid or skip:
            return Covid.NEGATIVE
        # aquí necesitamos dos números para separar en tres segmentos nuestro resultado
        threshold_one = Person.covid_chances[0]
        threshold_two = Person.covid_chances[1]
        aux = random.random()
        if aux < threshold_one:
            return Covid.ASINTOMATIC
        if aux < threshold_two:
            return Covid.LOW
        return Covid.HIGH

    @staticmethod
    def select_building(person, building_type):
        """Selecciona un edificio del diccionario, dado el tipo, respetando los pesos."""
        return random.choices(population=Person.building_dict[building_type],
                              weights=person.buildings[building_type])[0]

    @staticmethod
    def select_type(type_weights_dict):
        """Selecciona un tipo de edificio del diccionario, respetando los pesos."""
        return random.choices(population=list(type_weights_dict.keys()),
                              weights=list(type_weights_dict.values()))[0]

    @staticmethod
    def try_loop(person, max_attempts=5):
        """Una persona intenta ejecutar el método move() de su clase.
        Si tras varios intentos no logra encontrar un sitio con sitio, se va a casa."""
        if person.isHospitalized:
            return None
        if person.pcr == PCR.POSITIVE and person.covid == Covid.LOW:
            return None
        person.at_place = person.current_building == person.place
        if person.at_place and random.random() > 0.3 * type(person.current_building).leave_chance:  # todo cambiar esto¿?
            # día normal
            return None
        # ¿se va de donde está?
        if random.random() > type(person.current_building).leave_chance:
            # se queda donde está
            return None
        person.current_building.exit(person)
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
                final_building = Person.select_building(person, building_type)
                final_building.enter(person)
            except FullBuilding:
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
        super().__init__(id)
        self.place = Person.select_building(self, "Trabajo")
        self.at_place = False

    def move(self):
        """El trabajador se mueve."""
        Person.try_loop(self)


# clase Student
class Student(Person):
    type_weights = {"Trabajo": 3, "Hospital": 1, "Farmacia": 2, "Centro Educativo": 6, "Supermercado": 3,
                    "Centro Comercial": 4, "Home": 8}  # peso en las probabilidades sobre a qué tipo de edificio ir

    def __init__(self, id):
        super().__init__(id)
        self.place = Person.select_building(self, "Centro Educativo")
        self.at_place = False

    def move(self):
        """El estudiante se mueve."""
        Person.try_loop(self)

    # clase Stay_at_home


class Stay_at_home(Person):
    type_weights = {"Trabajo": 1, "Hospital": 1, "Farmacia": 3, "Centro Educativo": 1, "Supermercado": 6,
                    "Centro Comercial": 7, "Home": 8}  # peso en las probabilidades sobre a qué tipo de edificio ir

    def __init__(self, id):
        super().__init__(id)
        self.place = Person.home
        self.at_place = True

    def move(self):
        """El amo de casa se mueve."""
        Person.try_loop(self)
