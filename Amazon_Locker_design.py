from datetime import datetime, timedelta
from enum import Enum
import random

class LockerSize(Enum):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'

class LockerStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    OCCUPIED = 'OCCUPIED'
    FAULTY = 'FAULTY'

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

class Package:
    def __init__(self, package_id, size, user):
        self.package_id = package_id
        self.size = size # LockerSize
        self.user = user

class Locker:
    def __init__(self, locker_id, size):
        self.locker_id = locker_id
        self.size = size # LockerSize
        self.status = LockerStatus.AVAILABLE

    def is_available(self):
        return self.status == LockerStatus.AVAILABLE
    
    def mark_occupied(self):
        self.status = LockerStatus.OCCUPIED

    def mark_faulty(self):
        self.status = LockerStatus.FAULTY

    def mark_available(self):
        self.status = LockerStatus.AVAILABLE

class LockerLocation:
    def __init__(self, location_id, address):
        self.location_id = location_id
        self.address = address
        self.lockers = []

    def add_locker(self, locker):
        self.lockers.append(locker)

class LockerAssignment:
    def __init__(self, package, locker):
        self.assignment_id = f"{package.package_id}_{locker.locker_id}" # package_id = 1234 locker_id = L2 ==> 1234_L2  
        self.package = package
        self.locker = locker
        self.assigned_time = datetime.now()
        self.expiry_time = self.assigned_time + timedelta(days=3)
        self.otp = self._generate_otp()

    def _generate_otp(self):
        return str(random.randint(100000, 999999))

class LockerService:
    def __init__(self):
        self.assignments = {}
    def assign_locker(self, package, location):
        for locker in location.lockers:
            if locker.size == package.size and locker.is_available():
                locker.mark_occupied()
                assignment = LockerAssignment(package, locker)
                self.assignments[assignment.assignment_id] = assignment
                print(f"Assigned Locker: {locker.locker_id} to Package: {package.package_id}")
                return assignment
        print("No available locker found for this package.")
        return None
    def release_locker(self, locker_id, location, otp_input):
        for assignment_id, assignment in self.assignments.items():
            if assignment.locker.locker_id == locker_id:
                if assignment.otp == otp_input:
                    assignment.locker.mark_available()
                    print(f"Locker {locker_id} released successfully.")
                    del self.assignments[assignment_id]
                    return
                else:
                    print("❌ Incorrect OTP. Access denied.")
                    return
        print("⚠️ Locker not found or not assigned.")

            
    def verify_otp_and_release(self, assignment_id, otp_input):
        assignment = self.assignments.get(assignment_id)
        if not assignment:
            print("Invalid assignment.")
            return
        if assignment.otp_code == otp_input:
            assignment.locker.mark_available()
            print(f"Locker {assignment.locker.locker_id} released successfully.")
            del self.assignments[assignment_id]
        else:
            print("Invalid OTP. Access denied.")
            
    def check_expired_assignments(self):
        now = datetime.now()
        for assignment in list(self.assignments.values()):
            if now > assignment.expiry_time:
                assignment.locker.mark_available()
                print(f"Locker {assignment.locker.locker_id} expired and is now available.")
                del self.assignments[assignment.assignment_id]


if __name__ == "__main__":
    user = User("123U", "Drashti Mehta", "drashti@example.com")
    user2 = User("2133","XYZ","xyz@amazon.com")
    user3 = User("112","ABC","abc@amazon.com")


    package = Package("ABC", "S", user)
    package2 = Package("ABD", LockerSize.MEDIUM, user2)
    package3 = Package("ABBS", 'L', user3)




    location = LockerLocation("LOC001", "123 Main Street, Austin")
    locker1 = Locker("L1", LockerSize.SMALL)
    locker2 = Locker("L2", LockerSize.MEDIUM)
    locker3 = Locker("L3", LockerSize.LARGE)
    locker4 = Locker("l4", LockerSize.LARGE)
    locker5 = Locker("l5", LockerSize.MEDIUM)

    location.add_locker(locker1)
    location.add_locker(locker2)
    location.add_locker(locker3)
    location.add_locker(locker4)
    location.add_locker(locker5)
    
    locker3.mark_faulty()

    service = LockerService()

    # Assign locker
    assignment = service.assign_locker(package, location)
    assignment2 = service.assign_locker(package2,location)
    # Simulate package pickup
    if assignment:
        print(f"📬 OTP sent to user: {assignment.otp}")
        otp_entered = input("🔐 Enter OTP to unlock: ")
        service.release_locker(assignment.locker.locker_id, location, otp_entered)

    # Check expired (will not trigger in real-time)
    service.check_expired_assignments()
