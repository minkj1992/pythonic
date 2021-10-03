import random
import string


class VehicleRegistry:
    def generate_vehicle_id(self, length) -> str:
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id):
        license_prefix = id[:2]
        return f"{license_prefix}-{''.join(random.choices(string.digits, k=2))}-{''.join(random.choices(string.ascii_uppercase, k=2))}"


class Application:
    def register_vehicle(self, brand: str):
        # init
        registry = VehicleRegistry()
        vehicle_id = registry.generate_vehicle_id(12)
        license_plate = registry.generate_vehicle_license(vehicle_id)

        # compute the catalogue price
        catalogue_price = 0
        if brand == "Tesla Model 3":
            catalogue_price = 60000
        elif brand == "Volkswagen ID3":
            catalogue_price = 35000
        elif brand == "BMW 5":
            catalogue_price = 45000

        # compute the tax percentage
        # (default 5% of the catalogue price, except for electric cars where it is 2%)
        tax_percentage = 0.05 if brand == "Tesla Model 3" or brand == "Volkswagen ID3" else 0.02

        # compute the payable tax
        payable_tax = tax_percentage * catalogue_price

        # print out the vehicle registration information
        # print out the vehicle registration information
        print("Registration complete. Vehicle information:")
        print(f"Brand: {brand}")
        print(f"Id: {vehicle_id}")
        print(f"License plate: {license_plate}")
        print(f"Payable tax: {payable_tax}")


if __name__ == '__main__':
    brand = 'Volkswagen ID3'

    app = Application()
    app.register_vehicle(brand)
