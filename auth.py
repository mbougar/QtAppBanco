import pyrebase
import requests
import json



class PyrebaseAuth:
    _instance = None

    firebaseConfig = {
                        "apiKey": "AIzaSyD7B2-5zafo7ZwjtvC7saCEBkQUE2CVYBA",
                        "authDomain": "banking-test-5dfae.firebaseapp.com",
                        "databaseURL": "https://banking-test-5dfae.firebaseio.com/",
                        "projectId": "banking-test-5dfae",
                        "storageBucket": "banking-test-5dfae.firebasestorage.app",
                        "messagingSenderId": "129454901827",
                        "appId": "1:129454901827:web:3b95a483160f7c2c7922f6"
                    }
    
    auth = pyrebase.initialize_app(firebaseConfig).auth()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PyrebaseAuth, cls).__new__(cls)
        return cls._instance


    def login(self,username, password):
        if len(username)== 0 or len(username) == 0:
            raise Exception("Ingrese todos los datos")
        else:
            # user = self.auth.create_user_with_email_and_password(name, passw)
            #try:
            #    user = self.auth.sign_in_with_email_and_password(username, password)
            #except requests.exceptions.HTTPError as e:
            #    error_json = e.args[1]
            #    error = json.loads(error_json)['error']['message']
            #    print("e: ", error)
            self.auth.sign_in_with_email_and_password(username, password)
            #Mejor hacer esto a pelo y controlar la excepcion en la interfaz, para poner un mensaje personalizado
    
    def register(self , username, password):
        if len(username)== 0 or len(username) == 0:
            raise Exception("Ingrese todos los datos")
        else:
            # user = self.auth.create_user_with_email_and_password(name, passw)
            #try:
            #    user = self.auth.create_user_with_email_and_password(username, password)
            #except requests.exceptions.HTTPError as e:
            #    error_json = e.args[1]
            #    error = json.loads(error_json)['error']['message']
            #    print("e: ", error)
            user = self.auth.create_user_with_email_and_password(username, password)
            #Mejor hacer esto a pelo y controlar la excepcion en la interfaz, para poner un mensaje personalizado