import os
from datetime import date

# Patient Functions

def register_patient(patients):
    print("--- Register patient ---")

    name = input("Enter patient name: ")
    age = input("Enter patient age: ")
    symptoms = input("Enter patient symptoms: ")
    priority = input("Enter patient priority (1=Normal / 2=Emergency): ")

    if priority == "1":
        priority = "Normal"
    else:
        priority = "Emergency"

    patient_id = "P" + str(len(patients) + 1).zfill(3)
    department = suggest_department(symptoms)

    new_patient = {
        "id": patient_id,
        "name": name,
        "age": age,
        "symptoms": symptoms,
        "priority": priority,
        "department": department,
        "status": "waiting",
        "notes": "",
        "date": str(date.today())
    }

    if priority == "Emergency":
        patients.insert(0, new_patient)
        print("Emergency! " + name + " (" + patient_id + ") placed at front of queue.")
    else:
        patients.append(new_patient)
        print("Registered: " + name + " (" + patient_id + ") -> " + department)

    save_patients(patients)
    return patients


def view_queue(patients):
    print("--- Patient queue ---")

    found = False
    for i in range(len(patients)):
        p = patients[i]

        if p["status"] == "waiting":
            found = True
            print(f"{i+1}. [{p['id']}] {p['name']} | Age: {p['age']} | {p['priority']} | {p['department']}")

    if not found:
        print("Queue is empty")


def view_all_patients(patients):
    print("--- All patients ---")

    if len(patients) == 0:
        print("No patients registered")
        return

    for i in range(len(patients)):
        p = patients[i]
        print(f"{i+1}. [{p['id']}] {p['name']} | Age: {p['age']} | {p['priority']} | "
              f"{p['department']} | {p['status']}")


def call_next_patient(patients):
    print("--- Call next patient ---")

    for i in range(len(patients)):
        p = patients[i]

        if p["status"] == "waiting":
            notes = input("Add medical notes for " + p["name"] + " (or press Enter to skip): ")
            patients[i]["status"] = "seen"
            patients[i]["notes"] = notes
            save_patients(patients)
            print(f"Now seeing: {p['name']} ({p['id']}) -> {p['department']}")
            return patients

    print("No patients waiting")
    return patients


def update_patient(patients):
    print("--- Update patient ---")

    patient_id = input("Enter patient ID to update: ").upper()

    found_index = -1
    for i in range(len(patients)):
        if patients[i]["id"] == patient_id:
            found_index = i
            break

    if found_index == -1:
        print("Patient not found")
        return patients

    p = patients[found_index]
    print("Current info: " + p["name"] + " | Age: " + p["age"] + " | " +
          p["symptoms"] + " | " + p["priority"])

    print("What to update?")
    print("1. Name")
    print("2. Age")
    print("3. Symptoms")
    print("4. Priority")
    print("5. Notes")

    choice = input("Choose (1-5): ")

    if choice == "1":
        patients[found_index]["name"] = input("New name: ")
        print("Name updated")
    elif choice == "2":
        patients[found_index]["age"] = input("New age: ")
        print("Age updated")
    elif choice == "3":
        new_symptoms = input("New symptoms: ")
        patients[found_index]["symptoms"] = new_symptoms
        patients[found_index]["department"] = suggest_department(new_symptoms)
        print("Symptoms updated -> " + patients[found_index]["department"])
    elif choice == "4":
        new_priority = input("New priority (1=Normal / 2=Emergency): ")
        if new_priority == "1":
            patients[found_index]["priority"] = "Normal"
        else:
            patients[found_index]["priority"] = "Emergency"
        print("Priority updated")
    elif choice == "5":
        patients[found_index]["notes"] = input("New notes: ")
        print("Notes updated")
    else:
        print("Invalid choice")
        return patients

    save_patients(patients)
    return patients


def view_history(patients):
    print("--- Patient history (Seen) ---")

    found = False
    for p in patients:
        if p["status"] == "seen":
            found = True
            print(f"[{p['id']}] {p['name']} | Age: {p['age']} | "
                  f"{p['department']} | Notes: {p['notes']} | Date: {p['date']}")

    if not found:
        print("No patients seen yet")

# Appointment Functions

def book_appointment(patients, appointments):
    print("--- Book appointment ---")

    patient_id = input("Enter patient id: ").upper()

    found_patient = None
    for p in patients:
        if p["id"] == patient_id:
            found_patient = p
            break

    if found_patient is None:
        print("Patient not found")
        return appointments

    print("\nDoctors:")
    print("1. Dr. Vattey - Cardiology")
    print("2. Dr. Votey - General Medicine")
    print("3. Dr. Likaa - Orthopedics")
    print("4. Dr. Inna - Pediatrics")
    print("5. Dr. HaHa - Neurology")

    doctor_choice = input("Choose your doctor (1-5): ")

    if doctor_choice == "1":
        doctor = "Dr. Vattey - Cardiology"
    elif doctor_choice == "2":
        doctor = "Dr. Votey - General Medicine"
    elif doctor_choice == "3":
        doctor = "Dr. Likaa - Orthopedics"
    elif doctor_choice == "4":
        doctor = "Dr. Inna - Pediatrics"
    elif doctor_choice == "5":
        doctor = "Dr. HaHa - Neurology"
    else:
        print("Invalid choice")
        return appointments

    appointment_date = input("Appointment date (YYYY-MM-DD or "
                             "press Enter for today): ")
    if appointment_date == "":
        appointment_date = str(date.today())

    time = input("Time (e.g. 09:00): ")

    booking = doctor + "|" + appointment_date + "|" + time

    if booking in appointments:
        print("Time slot already booked!")
        return appointments

    appointments[booking] = {
        "patient_id": patient_id,
        "patient_name": found_patient["name"],
        "doctor": doctor,
        "date": appointment_date,
        "time": time
    }

    save_appointments(appointments)
    print(f"Appointment confirmed: {found_patient['name']} with "
          f"{doctor} on {appointment_date} at {time}")
    return appointments


def view_appointments(appointments):
    print("--- View appointments ---")

    if len(appointments) == 0:
        print("No appointments booked")
        return

    for key in appointments:
        a = appointments[key]
        print(f"{a['date']} | {a['time']} | {a['patient_name']} | {a['doctor']}")


def cancel_appointment(appointments):
    print("--- Cancel appointment ---")

    if len(appointments) == 0:
        print("No appointments to cancel")
        return appointments

    view_appointments(appointments)

    patient_name = input("Enter patient name to cancel: ")

    key_to_remove = None
    for key in appointments:
        if appointments[key]["patient_name"].lower() == patient_name.lower():
            key_to_remove = key
            break

    if key_to_remove is None:
        print("Appointment not found")
        return appointments

    a = appointments.pop(key_to_remove)
    save_appointments(appointments)
    print("Cancelled: " + a["patient_name"] + " with " + a["doctor"] + " on " + a["date"])
    return appointments

# Utility Functions

def symptoms_check(patients):
    print("--- Symptoms check ---")
    symptoms = input("Describe symptoms: ")
    dept = suggest_department(symptoms)
    print("Suggested department:", dept)


def daily_summary(patients, appointments):
    print("--- Daily summary ---")

    total = len(patients)
    normal = emergency = waiting = seen = 0
    dept_count = {}

    for p in patients:
        if p["priority"] == "Emergency":
            emergency += 1
        else:
            normal += 1

        if p["status"] == "waiting":
            waiting += 1
        else:
            seen += 1

        dept = p["department"]
        dept_count[dept] = dept_count.get(dept, 0) + 1

    print("Total patients:", total)
    print("Normal patients:", normal)
    print("Emergency patients:", emergency)
    print("===============================")
    print("Waiting patients:", waiting)
    print("Seen patients:", seen)
    print("Appointments:", len(appointments))

    print("\nPatients by department:")
    for dept, count in dept_count.items():
        print(f"{dept}: {'|' * count} ({count})")


def delete_patient(patients):
    print("--- Delete patient ---")

    patient_id = input("Enter patient ID: ").upper()
    new_list = [p for p in patients if p["id"] != patient_id]

    if len(new_list) == len(patients):
        print("Patient not found")
        return patients

    save_patients(new_list)
    print("Patient deleted")
    return new_list

# Department Suggestion

def suggest_department(symptoms):
    symptoms = symptoms.lower()

    if "chest" in symptoms or "heart" in symptoms:
        return "Cardiology"
    elif "headache" in symptoms or "dizziness" in symptoms:
        return "Neurology"
    elif "bone" in symptoms or "fracture" in symptoms:
        return "Orthopedics"
    elif "child" in symptoms or "baby" in symptoms:
        return "Pediatrics"
    elif "skin" in symptoms or "rash" in symptoms:
        return "Dermatology"
    elif "stomach" in symptoms or "nausea" in symptoms:
        return "Gastroenterology"
    else:
        return "General Medicine"

# File Handling

def load_patients():
    patients = []

    if not os.path.exists("patients.txt"):
        return patients

    with open("patients.txt", "r") as file:
        for line in file:
            parts = line.strip().split("|")
            if len(parts) == 9:
                patients.append({
                    "id": parts[0],
                    "name": parts[1],
                    "age": parts[2],
                    "symptoms": parts[3],
                    "priority": parts[4],
                    "department": parts[5],
                    "status": parts[6],
                    "notes": parts[7],
                    "date": parts[8],
                })
    return patients


def save_patients(patients):
    with open("patients.txt", "w") as file:
        for p in patients:
            file.write("|".join([
                p["id"],
                p["name"],
                p["age"],
                p["symptoms"],
                p["priority"],
                p["department"],
                p["status"],
                p["notes"],
                p["date"]
            ]) + "\n")


def load_appointments():
    appointments = {}

    if not os.path.exists("appointments.txt"):
        return appointments

    with open("appointments.txt", "r") as file:
        for line in file:
            parts = line.strip().split("|")
            if len(parts) == 5:
                key = parts[2] + "|" + parts[3] + "|" + parts[4]
                appointments[key] = {
                    "patient_id": parts[0],
                    "patient_name": parts[1],
                    "doctor": parts[2],
                    "date": parts[3],
                    "time": parts[4],
                }
    return appointments


def save_appointments(appointments):
    with open("appointments.txt", "w") as file:
        for a in appointments.values():
            file.write("|".join([
                a["patient_id"],
                a["patient_name"],
                a["doctor"],
                a["date"],
                a["time"]
            ]) + "\n")

# Main Program

def main():
    patients = load_patients()
    appointments = load_appointments()

    while True:
        print("\n--- Smart Hospital Management ---")
        print("1. Register patient")
        print("2. View patient queue")
        print("3. Call next patient")
        print("4. Update patient")
        print("5. View patient history")
        print("6. View all patients")
        print("7. Book appointment")
        print("8. View appointments")
        print("9. Cancel appointment")
        print("10. Symptom checker")
        print("11. Daily summary")
        print("12. Delete patient")
        print("13. Exit")

        choice = input("Choose (1-13): ")

        if choice == "1":
            patients = register_patient(patients)
        elif choice == "2":
            view_queue(patients)
        elif choice == "3":
            patients = call_next_patient(patients)
        elif choice == "4":
            patients = update_patient(patients)
        elif choice == "5":
            view_history(patients)
        elif choice == "6":
            view_all_patients(patients)
        elif choice == "7":
            appointments = book_appointment(patients, appointments)
        elif choice == "8":
            view_appointments(appointments)
        elif choice == "9":
            appointments = cancel_appointment(appointments)
        elif choice == "10":
            symptoms_check(patients)
        elif choice == "11":
            daily_summary(patients, appointments)
        elif choice == "12":
            patients = delete_patient(patients)
        elif choice == "13":
            save_patients(patients)
            save_appointments(appointments)
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()