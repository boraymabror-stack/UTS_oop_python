import json
from abc import ABC, abstractmethod


# CLASS INDUK
class DataProcessor(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process(self):
        pass


# CLASS KARYAWAN
class Employee(DataProcessor):
    def process(self):
        print("\n=== LAPORAN DATA KARYAWAN ===")
        for item in self.data:
            employee = PermanentEmployee(item) if item["is_permanent"] else ContractEmployee(item)
            employee.display()


# CLASS INDUK UNTUK DETAIL KARYAWAN
class EmployeeDetail:
    def __init__(self, data):
        self.emp_id = data["emp_id"]
        self.name = data["name"]
        self.base_salary = data["base_salary"]
        self.bonus_code = data["bonus_code"]

    def calculate_bonus(self):
        # Aturan bonus perlu disesuaikan jika dosen
        # memberikan persentase resmi.
        rates = {
            "PERF2026": 0.10,
            "SENIOR10": 0.10,
            "LEAD2026": 0.15
        }
        return self.base_salary * rates.get(self.bonus_code, 0)

    def display(self):
        pass


# INHERITANCE DAN OVERRIDE
class PermanentEmployee(EmployeeDetail):
    def display(self):
        bonus = self.calculate_bonus()
        total = self.base_salary + bonus
        print(f"{self.emp_id} | {self.name}")
        print("Status: Karyawan Tetap")
        print(f"Gaji Pokok : Rp{self.base_salary:,.0f}")
        print(f"Bonus      : Rp{bonus:,.0f}")
        print(f"Total Gaji : Rp{total:,.0f}")
        print("-" * 45)


class ContractEmployee(EmployeeDetail):
    def calculate_bonus(self):
        return 0

    def display(self):
        print(f"{self.emp_id} | {self.name}")
        print("Status: Karyawan Kontrak")
        print(f"Gaji Pokok : Rp{self.base_salary:,.0f}")
        print("Bonus      : Rp0")
        print(f"Total Gaji : Rp{self.base_salary:,.0f}")
        print("-" * 45)


# CLASS SENSOR
class Sensor(DataProcessor):
    def process(self):
        print("\n=== LAPORAN DATA SENSOR ===")
        for item in self.data:
            reading = TemperatureSensor(item)
            reading.display()


class TemperatureSensor:
    def __init__(self, data):
        self.sensor_id = data["sensor_id"]
        self.location = data["location"]
        self.temperature = data["temperature"]
        self.status = data["status"]
        self.operator_id = data["operator_id"]

    def display(self):
        print(
            f"{self.sensor_id} | {self.location} | "
            f"{self.temperature} C | {self.status} | "
            f"Operator: {self.operator_id if self.operator_id is not None else 'Tidak ada'}"
        )


# PROGRAM UTAMA
def main():
    try:
        with open("employee.json", "r", encoding="utf-8") as file:
            employee_data = json.load(file)

        with open("sensor_logs.json", "r", encoding="utf-8") as file:
            sensor_data = json.load(file)

        employee_processor = Employee(employee_data["employees"])
        sensor_processor = Sensor(sensor_data["readings"])

        employee_processor.process()
        sensor_processor.process()

        print("\n=== RINGKASAN ===")
        print("Jumlah karyawan:", len(employee_data["employees"]))
        print("Jumlah sensor:", len(sensor_data["readings"]))

    except FileNotFoundError as error:
        print("File tidak ditemukan:", error.filename)
        print("Pastikan file JSON dan main.py berada dalam folder yang sama.")
    except json.JSONDecodeError as error:
        print("Format JSON salah:", error)


if __name__ == "__main__":
    main()