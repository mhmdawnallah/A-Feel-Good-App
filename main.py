from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob, random
from datetime import datetime
from pathlib import Path
Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def login(self, username, password):
        with open("users.json",'r') as file:
            users = json.load(file)
            if username.strip() in users and users[username]['password'] == password.strip():
                self.manager.current = "login_screen_success"   
                self.ids.login_wrong.text = ""
            else:
                self.ids.login_wrong.text = "Wrong username or password"

class SignUpScreen(Screen):
    def add_user(self, username, password):
        print(username,password)
        if  username and  password:
            with open("users.json",'r') as file:
                users = json.load(file)

            users[username] = {"username":username.strip(),
            "password":password.strip(),
            "created":datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            }
            with open('users.json','w') as file:
                json.dump(users,file)
            self.manager.current = 'sign_up_screen_success'
        else:
            self.ids.signup_wrong.text = "Please Don't leave empty fields"
            
class SignUpScreenSuccess(Screen):
    def go_to_login(self):

        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

class LoginScreenSuccess(Screen):

    def logout(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    def get_quote(self, feeling):
        feeling = feeling.lower()
        avaliable_feelings = glob.glob("quotes/*txt")

        avaliable_feelings = [Path(filename).stem for
         filename in avaliable_feelings]

        if feeling in avaliable_feelings:
            with open(f"quotes/{feeling}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another Feeling"
       
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()