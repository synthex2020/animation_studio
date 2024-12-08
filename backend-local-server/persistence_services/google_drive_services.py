import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

class GoogleDriveServices:

    def __init__(self):
        #   AUTHENTICATION PROCESS 
        self.creds = None

         # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        #   IF NO (VALID) CREDENTIALS PRESENT LET USER LOGIN 
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentails.json" , SCOPES
            )
                self.creds = flow.run_local_server(port=0)

            #   Save the credentials for next run 
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
        self.service = build("drive", "v3", credentials=self.creds)


    #   CONNECT TO GOOGLE DRIVE TEST

    def connect_drive(self):
        try:
            current_service = self.service
            
            #   CALL THE DRIVE API V3
            results = (
                current_service.files().list(
                    pageSize=10, fields="nextPageToken, files(id, name)"
                ).execute()
            )   
            items = results.get("files", [])

            if not items:
                print("No files found ")
                return
            print("Files: ")
            for item in items:
                print(f"{item['name']} ({item['id']})")

        except HttpError as error:
            print(f'An error occured {error}') 

    #   UPLOAD A FILE TO GOOGLE DRIVE 

    #   DOWLOAD A FILE FROM GOOGLE DRIVE 

    


