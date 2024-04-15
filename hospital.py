from datetime import datetime

class Patient:
    def __init__(self, patient_id, gender, race, age, ethnicity, insurance, zip_code):
        self.patient_id = patient_id
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

class Visit:
    def __init__(self, visit_id, visit_time, department, chief_complaint):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.department = department
        self.chief_complaint = chief_complaint
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

class Note:
    def __init__(self, note_id, note_type):
        self.note_id = note_id
        self.note_type = note_type

class Hospital:
    def __init__(self):
        self.patients = {}

    def add_patient(self, patient):
        self.patients[patient.patient_id] = patient

    def remove_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]

    def retrieve_patient(self, patient_id):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            print("Patient information for ID:", patient_id)
            print("Gender:", patient.gender)
            print("Race:", patient.race)
            print("Age:", patient.age)
            print("Ethnicity:", patient.ethnicity)
            print("Insurance:", patient.insurance)
            print("Zip code:", patient.zip_code)
            print("Visits:")
            for visit in patient.visits:
                print("Visit ID:", visit.visit_id)
                print("Visit time:", visit.visit_time.strftime('%Y-%m-%d'))
                print("Department:", visit.department)
                print("Chief complaint:", visit.chief_complaint)
                # Additional loop to print notes for each visit
                print("Notes:")
                for note in visit.notes:
                    print("Note ID:", note.note_id)
                    print("Note Type:", note.note_type)
        else:
            print("Patient not found.")

    def count_visits_on_date(self, date):
        total_visits = 0
        for patient in self.patients.values():
            for visit in patient.visits:
                if visit.visit_time.date() == date.date():
                    total_visits += 1
        return total_visits
