from tkinter import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob, random, bcrypt
from datetime import datetime
from pathlib import Path
Builder.load_file('design.kv')

class LoginScreen(Screen):

    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def login(self, username, password):
        with open("users.json",'r') as file:
            users = json.load(file)
            if username in users and bcrypt.checkpw(str.encode(password), str.encode(users[username]['password']) ):
                self.manager.current = "login_screen_success"   
                self.ids.login_wrong.text = ""
            else:
                self.ids.login_wrong.text = "Wrong username or password"
    def go_to_forget_password(self):
        self.manager.current = "forget_password_screen"

class SignUpScreen(Screen):

    def add_user(self, username, password):
        print(username,password)
        with open("users.json") as file:
                users = json.load(file)
        if  not username in users and  password and username:
            password_hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode()
            with open("users.json") as file:
                users = json.load(file)

            users[username] = {"username":username,
            "password":password_hashed,
            "created":datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            }
            with open('users.json','w') as file:
                json.dump(users,file)
            self.manager.current = 'sign_up_screen_success'
        else:
            self.ids.signup_wrong.text = "Please Enter Valid Usernames Or Passwords"
            
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

class ForgetPasswordScreen(Screen):
        
    def update_password(self, username, new_password):
        with open("users.json") as file:
            users = json.load(file)
        if username in users and new_password and username:
            password_hashed = bcrypt.hashpw(str.encode(new_password), bcrypt.gensalt()).decode()
            users[username]['password'] = password_hashed
            with open("users.json",'w') as file:
                json.dump(users,file)
            self.manager.current = "forget_password_screen_success"
        elif not new_password or not username:
            self.ids.username_wrong.text = "Please Don't Leave any TextFields Empty "
        else:
            self.ids.username_wrong.text = "Please Enter valid username"
class ForgetPasswordScreenSuccess(Screen):
    def go_to_login(self):

        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

class RootWidget(ScreenManager):
    pass
 
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()