import random
import string
from typing import Dict


class VehicleInfo:
    def __init__(self, brand, electric, catalogue_price):
        self.brand: str = brand
        self.electric: bool = electric
        self.catalogue_price: float = catalogue_price

    def compute_tax(self):
        pass

    def __repr__(self):
        return f"""
        [Vehicle Info]
        brand: {self.brand}
        electric: {self.electric}
        catalogue_price: {self.catalogue_price}"""


class Vehicle:
    def __init__(self, id, license_plate, info):
        self.id = id
        self.license_plate = license_plate
        self.info = info

    def __repr__(self):
        return f"""
        [Vehicle]
        id: {self.id}
        license_plate: {self.license_plate}
        {str(self.info)}
                """


class VehicleRegistry:
    db: Dict[str, VehicleInfo] = {}

    @staticmethod
    def insert_vehicle_info(brand, electric, catalogue_price):
        VehicleRegistry.db[brand] = VehicleInfo(brand, electric, catalogue_price)

    @staticmethod
    def get_vehicle_info(brand):
        return VehicleRegistry.db[brand]

    def __init__(self):
        VehicleRegistry.insert_vehicle_info("Tesla Model 3", True, 60000)
        VehicleRegistry.insert_vehicle_info("Volkswagen ID3", True, 35000)
        VehicleRegistry.insert_vehicle_info("BMW 5", False, 45000)
        VehicleRegistry.insert_vehicle_info("Tesla Model Y", True, 75000)

    def generate_vehicle_id(self, length) -> str:
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id):
        license_prefix = id[:2]
        return f"{license_prefix}-{''.join(random.choices(string.digits, k=2))}-{''.join(random.choices(string.ascii_uppercase, k=2))}"

    def create_vehicle(self, brand):
        id = self.generate_vehicle_id(length=12)
        license_plate = self.generate_vehicle_license(id)
        return Vehicle(id, license_plate, VehicleRegistry.get_vehicle_info(brand))


class Application:
    def register_vehicle(self, brand: str):
        registry = VehicleRegistry()
        vehicle = registry.create_vehicle(brand)
        print(vehicle)


if __name__ == '__main__':
    brand = 'Volkswagen ID3'

    app = Application()
    app.register_vehicle(brand)
