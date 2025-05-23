from pyignite import Client, exceptions
import json


def print_choices():
    print("\n======== OPERACJE ========")
    print("dp - dodaj pacjenta")
    print("ip - informacje o pacjencie")
    print("dw - dodaj wizytę")
    print("all - informacje o wszystkich pacjentach")
    print("up - usuń pacjenta")
    print("q - zakończ program")
    print("cl - usuń cache")

def add_patient(patients_cache):
    print("\n======== DODAWANIE PACJENTA ========")
    name = input("Imię: ").strip().capitalize()
    surname = input("Nazwisko: ").strip().capitalize()
    pesel = input("Pesel: ").strip()

    data = {
        "name": name,
        "surname": surname,
        "pesel": pesel,
        "visits": []
    }
    if patients_cache.get(pesel):
        print("\nPacjent o tym PESELu już istnieje.")
        return
    
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
        else:
            print(f"\nPESEL: {key} – Brak informacji")

def destroy_cache(patients_cache):
    print("\n======== DESTRUKCJA CACHE ========")
    patients_cache.destroy()
    print("Cache zniszczony")

def delete_patient(patients_cache):
    print("\n======== USUWANIE PACJENTA ========")
    pesel = input("Podaj pesel: ")

    json_data = patients_cache.get(pesel)

    if json_data is not None:
        patients_cache.remove_key(pesel)
        print("\nPacjent usunięty")
    else:
        print("\nBrak takiego pacjenta")
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
        ]
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

        elif choice == "all":
            all_patients_info(patients_cache)
        
        elif choice == "up":
            delete_patient(patients_cache)

        elif choice == "q":
            # patients_cache.destroy()
            break

        elif choice == "cl":
            destroy_cache(patients_cache)
            break
        else:
            print("\nBłąd: Niepoprawne polecenie")

    client.close()
    

if __name__ == "__main__":
    main()
    print("\nZakończono program")