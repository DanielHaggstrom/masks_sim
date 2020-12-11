from errors import FullBuilding


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

    def roll(self, mod_infection):
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
            self.db["pcr"].append(person.pcr)  # todo esto no es correcto


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
            raise FullBuilding("Edificio Lleno.")
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
        person.isHospitalized = True

    def discharge(self, person):
        """Un paciente es dado de alta."""
        self.hospitalized.remove(person)
        person.building = None
        person.isHospitalized = False

    def contact(self):
        """Contagios entre todos los visitantes del hospital."""
        super().roll(Hospital.mod_infection)  # todo implementar correctamente el contagio en un hospital

    def update(self):
        """Registra a todos los visitantes y enfermos en la base de datos."""
        for person in self.hospitalized:
            self.db["datetime"].append(type(person).current_datetime)
            self.db["id"].append(person.id)
            self.db["pcr"].append(person.pcr)  # todo esto no es correcto
        super().update()


# clase Pharmacy
class Pharmacy(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().roll(Pharmacy.mod_infection)


# clase Centro Educativo
class Learning_Center(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().roll(Learning_Center.mod_infection)


# clase Workplace
class Workplace(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().roll(Workplace.mod_infection)


# Clase Market
class Market(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().roll(Market.mod_infection)


# Clase Mall
class Mall(Building):
    leave_chance = None
    mod_infection = None

    def __init__(self, name, weight, capacity):
        super().__init__(name, weight, capacity)

    def contact(self):
        super().roll(Market.mod_infection)
