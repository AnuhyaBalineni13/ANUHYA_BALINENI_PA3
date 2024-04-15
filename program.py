from datetime import datetime
import csv
from credentials import CredentialManager
from hospital import Hospital, Patient, Visit, Note

class Program:
    def __init__(self, credential_file, patients_file):
        self.credential_manager = CredentialManager(credential_file)
        self.hospital = Hospital()
        self.load_patient_data(patients_file)

    def load_patient_data(self, file_path):
        with open(file_path, 'r') as file:
             reader = csv.DictReader(file)
             for row in reader:
                patient_id = row['Patient_ID']
                gender = row['Gender']
                race = row['Race']
                age = int(row['Age'])
                ethnicity = row['Ethnicity']
                insurance = row['Insurance']
                zip_code = row['Zip_code']
                visit_id = row['Visit_ID']
                visit_time = datetime.strptime(row['Visit_time'], '%Y-%m-%d')
                department = row['Visit_department']
                chief_complaint = row['Chief_complaint']
                visit = Visit(visit_id, visit_time, department, chief_complaint)
                
                # Check if patient already exists, if not, create new patient
                if patient_id not in self.hospital.patients:
                    patient = Patient(patient_id, gender, race, age, ethnicity, insurance, zip_code)
                    self.hospital.add_patient(patient)
                else:
                    patient = self.hospital.patients[patient_id]
                    
                # Associate visit with patient
                patient.add_visit(visit) 
                note_id = row['Note_ID']
                note_type = row['Note_type']
                note = Note(note_id, note_type)
                visit.add_note(note)

    def start(self):
        user = self.login()
        if user.role == 'admin':
            self.admin_actions()
        elif user.role == 'management':
            self.management_actions()
        elif user.role in ['clinician', 'nurse']:
            self.clinician_nurse_actions()

    def admin_actions(self):
        print("You are logged in as an admin.")
        print("You can only perform 'count_visits' action.")
        action = input("Enter 'count_visits' or 'stop': ").strip().lower()
        if action == 'count_visits':
            date_str = input("Enter date (YYYY-MM-DD): ")
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                total_visits = self.hospital.count_visits_on_date(date)
                print("Total visits on", date.strftime('%Y-%m-%d'), ":", total_visits)
            except ValueError:
                print("Invalid date format.")
        elif action == 'stop':
            print("Exiting program.")
            exit()
        else:
            print("Invalid action. Exiting program.")
            exit()

    def management_actions(self):
        print("You are logged in as management.")
        
        self.generate_key_statistics()
        print("Statistics generated. Exiting program.")
        exit()

    def clinician_nurse_actions(self):
        print("You are logged in as a clinician/nurse.")
        print("You can perform all actions.")
        while True:
            action = input("Enter 'add_patient', 'remove_patient', 'retrieve_patient', 'count_visits', or 'stop': ").strip().lower()
            if action == 'add_patient':
                self.add_patient()
            elif action == 'remove_patient':
                self.remove_patient()
            elif action == 'retrieve_patient':
                patient_id = input("Enter Patient_ID: ")
                self.hospital.retrieve_patient(patient_id)
            elif action == 'count_visits':
                date_str = input("Enter date (YYYY-MM-DD): ")
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    total_visits = self.hospital.count_visits_on_date(date)
                    print("Total visits on", date.strftime('%Y-%m-%d'), ":", total_visits)
                except ValueError:
                    print("Invalid date format.")
            elif action == 'stop':
                print("Exiting program.")
                exit()
            else:
                print("Invalid action. Please try again.")

    def add_patient(self):
        patient_id = input("Enter Patient_ID: ")
        if patient_id in self.hospital.patients:
            print("Patient already exists.")
            return
        gender = input("Enter Gender: ")
        race = input("Enter Race: ")
        age = int(input("Enter Age: "))
        ethnicity = input("Enter Ethnicity: ")
        insurance = input("Enter Insurance: ")
        zip_code = input("Enter Zip code: ")
        patient = Patient(patient_id, gender, race, age, ethnicity, insurance, zip_code)
        self.hospital.add_patient(patient)
        print("Patient added successfully.")

    def remove_patient(self):
        patient_id = input("Enter Patient_ID: ")
        if patient_id in self.hospital.patients:
            self.hospital.remove_patient(patient_id)
            print("Patient removed successfully.")
        else:
            print("Patient not found.")


    def generate_key_statistics(self):
        print("Generating key statistics reports...")
        # Initialize dictionaries to store statistics
        patients_count = {}
        insurance_count = {}
        demographics_count = {'age': {}, 'race': {}, 'gender': {}, 'ethnicity': {}}
        
        # Collect statistics from patient data
        for patient in self.hospital.patients.values():
            # Count total patients
            patients_count[patient.patient_id] = patients_count.get(patient.patient_id, 0) + 1
            
            # Count insurance types
            insurance_count[patient.insurance] = insurance_count.get(patient.insurance, 0) + 1
            
            # Count demographics
            demographics_count['age'][patient.age] = demographics_count['age'].get(patient.age, 0) + 1
            demographics_count['race'][patient.race] = demographics_count['race'].get(patient.race, 0) + 1
            demographics_count['gender'][patient.gender] = demographics_count['gender'].get(patient.gender, 0) + 1
            demographics_count['ethnicity'][patient.ethnicity] = demographics_count['ethnicity'].get(patient.ethnicity, 0) + 1

        # Print key statistics
               
        print("\n1. Temporal trend of the number of patients who visited the hospital with different types of insurances:")
        for insurance, count in insurance_count.items():
            print(f"   - Insurance: {insurance}, Number of patients: {count}")
        
        print("\n2. Temporal trend of the number of patients who visited the hospital in different demographics groups:")
        for category, data in demographics_count.items():
            print(f"   - Demographic category: {category}")
            for group, count in data.items():
                print(f"     - {group}: {count}")

        print("Key statistics reports generated successfully.")


    def login(self):
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = self.credential_manager.validate_user(username, password)
            if user:
                print("Login successful!")
                return user
            else:
                print("Invalid username or password. Please try again.")
