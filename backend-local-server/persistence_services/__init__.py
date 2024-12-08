from persistence_services.google_drive_services import GoogleDriveServices


class PeristenceServices:

    def __init__(self):
        self.google_drive_services = GoogleDriveServices()
    

    def connect_drive(self):
        self.google_drive_services.connect_drive()

