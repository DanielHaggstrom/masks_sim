class FullBuilding(Exception):
    """Error lanzado cuando una persona intenta entrar en un edificio lleno."""
    pass


class ClosedBuilding(Exception):
    """Error lanzado cuando una persona intenta entrar en un edificio cerrado."""
    pass
