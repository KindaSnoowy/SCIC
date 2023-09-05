from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import random
from libs.network import Network, Login, Client_Message, Arquivo_req
from _thread import start_new_thread



class Gerenciador(ScreenManager):
    pass

class Popup_error_ip(Popup):
    def fechar(self):
        self.dismiss()

class Popup_IP(Popup):
    def __init__(self, nome, **kwargs):
        super().__init__(**kwargs)
        self.nome = nome
    def enviar(self):
        global network
        network = Network()
        conectado = network.connect(HOST = self.ids.ip.text)

        if conectado:
            self.dismiss()
            network.send(Login(self.nome))

            data = network.recv(2048).decode()
            if data == 'CONFIRMADO':
                popup = Popup_txt()
                popup.open()
            else:
                popup = Popup_error_login()
                popup.open()
        else:
            Popup_error_ip().open()

class Popup_BOMBA(Popup):
    def enviar(self):
        tela = self.parent.children[1].children[0]

        x = self.ids.x_bomba.text
        y = self.ids.y_bomba.text
        tela.network.send(Client_Message(f"{x} {y}", bomba = True))
        self.dismiss()

text_inicial = ''
class Chat(Screen):
    def on_enter(self):
        self.network = network
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
        network.send(Arquivo_req())

        data = network.recv(2048)
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
    def entrar(self):
        Popup_IP(self.ids.nome.text).open()
        

class Main(App):
    def build(self):
        return Gerenciador()
        
if __name__ == '__main__':  
    Main().run()

