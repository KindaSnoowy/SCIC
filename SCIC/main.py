from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import random
from libs.network import Network, Login, Client_Message, Arquivo_req
from _thread import start_new_thread

network = Network()
network.connect()

class Gerenciador(ScreenManager):
    pass

class Popup_BOMBA(Popup):
    def enviar(self):
        tela = self.parent.children[1].children[0]

        x = self.ids.x_bomba.text
        y = self.ids.y_bomba.text
        tela.network.send(Client_Message(f"{x} {y}", bomba = True))
        self.dismiss()

text_inicial = ''
class Chat(Screen):
    def __init__(self, mensagens = [], network = network, **kwargs):
        super().__init__(**kwargs)
        self.msgs = 0
        self.network = network

    def on_enter(self):
        self.ids.label_msg.text = text_inicial
        start_new_thread(self.receive_message, ())
        
    def send_BOMBA(self):
        popup = Popup_BOMBA()
        popup.open()

    def send_message(self):
        texto = self.ids.mensagem.text
        self.ids.mensagem.text = ''
        self.network.send(Client_Message(texto))

    def receive_message(self):
        while True:
            data = self.network.recv(2048).decode()
            
            if self.ids.label_msg.text == '':
                self.ids.label_msg.text += data
            else: 
                self.ids.label_msg.text += "\n"+data

class Popup_txt(Popup):
    def sim(self):
        self.dismiss()
        
        tela = self.parent.children[1].children[0]

        tela.network.send(Arquivo_req())

        data = tela.network.recv(2048)
        global text_inicial

        text_inicial = data.decode()

        self.parent.children[1].current = 'chat'

    def nao(self):
        self.dismiss()
        self.parent.children[1].current = 'chat'

    def talvez(self):
        talvez = random.randint(1,2)
        if talvez == 1:
            self.sim()
        else:
            self.nao()

class Popup_error_login(Popup):
    def ok(self):
        self.dismiss()

class TelaInicial(Screen):
    def __init__(self, network = network, **kwargs):
        super().__init__(**kwargs)
        self.network = network

    def entrar(self):
        self.click_entrar = True
        self.network.send(Login(self.ids.nome.text))

        data = self.network.recv(2048).decode()
        if data == 'CONFIRMADO':
            popup = Popup_txt()
            popup.open()
        else:
            popup = Popup_error_login()
            popup.open()

class Main(App):
    def build(self):
        return Gerenciador()
        
if __name__ == '__main__':  
    Main().run()

