from twilio.rest import Client
from UnhasECafe.models import Usuario
from UnhasECafe import database
from UnhasECafe import account_sid_twilio, auth_token_twilio
def enviar_mensagem(codigo: str, para: str):
    client = Client(account_sid_twilio, auth_token_twilio)
    message = client.messages.create(
        from_='+12297380312',
        body=f'Seu código de verificação é: {codigo}',
        to='+55'+para
    )

    print(message.sid)

def cadastrar_usuario(usuario: Usuario):
    database.session.add(usuario)
    database.session.commit()

    #Cadastrou -> apareceu pra confirmar -> colocou certo -> foi pra área de login