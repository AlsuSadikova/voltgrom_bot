# помощник для расчёта мощности по электроприборам
user_data = {}
device_specs = {
    "TV": {"power": 300, "cos_phi": 0.75, "multiplier": 1},
    "toaster": {"power": 800, "cos_phi": 1, "multiplier": 1},
    "kettle": {"power": 2000, "cos_phi": 1, "multiplier": 1},
    "PC": {"power": 500, "cos_phi": 0.75, "multiplier": 1},
    "coffeeMaker": {"power": 1000, "cos_phi": 1, "multiplier": 1},
    "printer": {"power": 500, "cos_phi": 0.75, "multiplier": 1},
    "fridge": {"power": 600, "cos_phi": 0.75, "multiplier": 3},
    "microwave": {"power": 1400, "cos_phi": 0.9, "multiplier": 1},
    "iron": {"power": 1700, "cos_phi": 1, "multiplier": 1},
    "fans": {"power": 1000, "cos_phi": 0.9, "multiplier": 1},
    "hairDryer": {"power": 1200, "cos_phi": 0.9, "multiplier": 1},
    "heater": {"power": 1500, "cos_phi": 1, "multiplier": 1},
    "washingMachine": {"power": 2500, "cos_phi": 0.75, "multiplier": 3},
    "vacuum": {"power": 1700, "cos_phi": 0.75, "multiplier": 3},
    "oven": {"power": 2000, "cos_phi": 1, "multiplier": 1},
    "lighting": {"power": 1000, "cos_phi": 0.9, "multiplier": 1},
    "airConditioner": {"power": 1500, "cos_phi": 0.75, "multiplier": 3},
    "electric_stove": {"power": 3000, "cos_phi": 1, "multiplier": 1},
    "boiler": {"power": 1500, "cos_phi": 1, "multiplier": 1},
    "drill": {"power": 800, "cos_phi": 0.75, "multiplier": 3},
    "grinder": {"power": 900, "cos_phi": 0.75, "multiplier": 3},
    "perforator": {"power": 1200, "cos_phi": 0.75, "multiplier": 3},
    "circularSaw": {"power": 1300, "cos_phi": 0.75, "multiplier": 3},
    "jigsaw": {"power": 700, "cos_phi": 0.75, "multiplier": 3},
    "sander": {"power": 1700, "cos_phi": 0.75, "multiplier": 3},
    "planer": {"power": 900, "cos_phi": 0.75, "multiplier": 3},
    "compressor": {"power": 2000, "cos_phi": 0.75, "multiplier": 3},
    "waterPump": {"power": 1000, "cos_phi": 0.75, "multiplier": 3},
    "lawnMower": {"power": 1500, "cos_phi": 0.75, "multiplier": 3},
    "electric_motors": {"power": 1500, "cos_phi": 0.75, "multiplier": 3},
    "flowHeater": {"power": 5000, "cos_phi": 1, "multiplier": 1},
    "weldingMachine": {"power": 2300, "cos_phi": 0.75, "multiplier": 1},
}


def calculate_power(devices):
    total_power = 0
    for device_name, quantity in devices.items():
        if device_name in device_specs:
            specs = device_specs[device_name]
            active_power = specs["power"] * quantity
            full_power = (active_power * specs["multiplier"]) / specs["cos_phi"]
            total_power += full_power
        else:
            print(f"Устройство {device_name} не найдено в спецификациях.")
    return total_power
