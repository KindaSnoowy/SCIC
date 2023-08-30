# S.C.I.C. <-> Projeto IFMG
Software Comunicativo Intracanhões

O Software Comunicativo Intracanhões foi feito para ajudar a Rússia em sua guerra contra a Venezuela, fornecendo um meio de comunicação via wi-fi local entre os canhões.
Segundo estatísticas depois de nossos testes, depois do uso de nosso programa, o desempenho da Rússia na guerra subiu em 345%, se provando bastante eficaz.

SCIC usa Kivy e Socket para um chat simples onde vários clientes se conectam à um servidor e podem se comunicar (e planejar envio de bombas 💣).
Todas as mensagens enviadas no SCIC ficam salvas em um log no servidor e toda vez que um cliente se conecta seu chat pode se atualizar de acordo com os arquivos no servidor.

O código deve funcionar corretamente em qualquer plataforma em que possa se rodar python, não se esqueça de baixar a biblioteca Kivy (https://pypi.org/project/Kivy/).
Depois de inúmeros gb de espaço gastos, não conseguimos criar uma build .apk pra celular, então algum dia, em algum momento, sai uma versão pra Android. 👍

Android deve funcionar corretamente se abrir o arquivo com acesso a pasta em alguma IDE como o PyDroid.
Windows e Linux funciona corretamente na build Desktop, MacOS não foi testado.
