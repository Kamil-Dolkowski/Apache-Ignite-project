from pyignite import Client, exceptions
import json


def print_choices():
    print("\n======== OPERACJE ========")
    print("dp - dodaj pacjenta")
    print("ip - informacje o pacjencie")
    print("dw - dodaj wizytę")
    print("dr - dodaj receptę")
    print("ds - dodaj skierowanie")
    print("all - informacje o wszystkich pacjentach")
    print("q - zakończ program")

def add_patient(patients_cache):
    print("\n======== DODAWANIE PACJENTA ========")
    name = input("Imię: ")
    surname = input("Nazwisko: ")
    pesel = input("Pesel: ")

    data = {
        "name": name,
        "surname": surname,
        "pesel": pesel,
        "visits": [],
        "prescriptions": [],
        "referrals": []
    }

    json_data = json.dumps(data)
    patients_cache.put(pesel, json_data)

def patient_info(patients_cache):
    print("\n======== INFO O PACJENCIE ========")
    pesel = input("Podaj pesel: ")

    json_data = patients_cache.get(pesel)

    if json_data is not None:
        data = json.loads(json_data)

        print(f"\nImię: {data["name"]}")
        print(f"Nazwisko: {data["surname"]}")
        print(f"Pesel: {data["pesel"]}")

        print("Wizyty:")
        for visit in data["visits"]:
            print(f"- Data: {visit["timestamp"]}, Lekarz: {visit["doctor"]}")
        
        print("Recepty:")
        for prescription in data["prescriptions"]:
            print(f"- Data: {prescription["date"]}, Lekarz: {prescription["doctor"]}, Leki {prescription["medicines"]}")

        print("Skierowania:")
        for referral in data["referrals"]:
            print(f"- Data: {referral["date"]}, Lekarz: {referral["doctor"]}, Badanie: {referral["test"]}")

    else:
        print("\nBrak informacji")

def add_visit(patients_cache):
    print("\n======== DODAWANIE WIZYTY ========")
    pesel = input("Podaj pesel: ")

    json_data = patients_cache.get(pesel)
    
    if json_data is not None:
        data = json.loads(json_data)

        date = input("\nPodaj datę [DD.MM.RRRR]: ")
        time = input("Podaj godzinę [HH:MM]: ")
        doctor = input("Podaj lekarza: ")

        visit = {
            "timestamp": f"{date} {time}",
            "doctor": doctor
        }

        data["visits"].append(visit)

        json_data = json.dumps(data)
        patients_cache.put(pesel, json_data)

    else:
        print("\nBrak takiego pacjenta")

def add_prescription(patients_cache):
    print("\n======== DODAWANIE RECEPTY ========")
    pesel = input("Podaj pesel: ")

    json_data = patients_cache.get(pesel)
    
    if json_data is not None:
        data = json.loads(json_data)

        date = input("\nPodaj datę [DD.MM.RRRR]: ")
        doctor = input("Podaj lekarza: ")
        medicines = input("Podaj leki: ")

        prescription = {
            "date": date,
            "doctor": doctor,
            "medicines": medicines
        }

        data["prescriptions"].append(prescription)

        json_data = json.dumps(data)
        patients_cache.put(pesel, json_data)

    else:
        print("\nBrak takiego pacjenta")

def add_referral(patients_cache):
    print("\n======== DODAWANIE SKIEROWANIA ========")
    pesel = input("Podaj pesel: ")

    json_data = patients_cache.get(pesel)
    
    if json_data is not None:
        data = json.loads(json_data)

        date = input("\nPodaj datę [DD.MM.RRRR]: ")
        doctor = input("Podaj lekarza: ")
        test = input("Podaj badanie: ")

        referral = {
            "date": date,
            "doctor": doctor,
            "test": test
        }

        data["referrals"].append(referral)

        json_data = json.dumps(data)
        patients_cache.put(pesel, json_data)

    else:
        print("\nBrak takiego pacjenta")

def all_patients_info(patients_cache):
    print("\n======== INFO O WSZYSTKICH PACJENTACH ========")
    for key, value in patients_cache.scan():
        if value is not None:
            data = json.loads(value)
            print(f"\nPESEL: {key}")
            print(f"Imię: {data['name']}")
            print(f"Nazwisko: {data['surname']}")

            print("Wizyty:")
            for visit in data["visits"]:
                print(f"- Data: {visit['timestamp']}, Lekarz: {visit['doctor']}")

            print("Recepty:")
            for prescription in data["prescriptions"]:
                print(f"- Data: {prescription["date"]}, Lekarz: {prescription["doctor"]}, Leki {prescription["medicines"]}")

            print("Skierowania:")
            for referral in data["referrals"]:
                print(f"- Data: {referral["date"]}, Lekarz: {referral["doctor"]}, Badanie: {referral["test"]}")
        else:
            print(f"\nPESEL: {key} – Brak informacji")


# ==================== MAIN ====================

def main():
    try:
        client = Client()
        client.connect('127.0.0.1', 10800)
    except (exceptions.ReconnectError):
        print("\nBłąd: Nie można połączyć z Apache Ignite")
        return 


    patients_cache = client.get_or_create_cache('patients')

    # Dane przykładowe

    data = {
        "name": 'Piotr',
        "surname": 'Fulmański',
        "pesel": '1',
        "visits": [
            {"timestamp": '12.04.2025 10:00', "doctor": 'Anna Nowak'},
            {"timestamp": '10.05.2025 9:00', "doctor": 'Anna Nowak'}
        ],
        "prescriptions": [],
        "referrals": []
    }
    
    json_data = json.dumps(data)
    patients_cache.put('1', json_data)



    choice = ""
    while (choice != "q"):
        print_choices()
        choice = input("\nWybrane polecenie: ")

        if choice == "dp":
            add_patient(patients_cache)

        elif choice == "ip":
            patient_info(patients_cache)

        elif choice == "dw":
            add_visit(patients_cache)

        elif choice == "dr":
            add_prescription(patients_cache)

        elif choice == "ds":
            add_referral(patients_cache)

        elif choice == "all":
            all_patients_info(patients_cache)
            
        elif choice == "q":
            # patients_cache.destroy()
            break

        else:
            print("\nBłąd: Niepoprawne polecenie")
    

if __name__ == "__main__":
    main()
    print("\nZakończono program")