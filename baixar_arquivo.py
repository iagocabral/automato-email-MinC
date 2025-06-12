from imap_tools import MailBox, MailboxLoginError, AND
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

PASTA_DESTINO = os.getenv("PASTA_DESTINO", "./anexos")

EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

try:
    with MailBox('imap.gmail.com').login(EMAIL, SENHA) as mailbox:
        folders = mailbox.folder.list()
        print("✅ Conexão com Gmail IMAP foi bem-sucedida!")

        # Buscar emails não lidos com anexo do remetente específico
        for msg in mailbox.fetch(AND(seen=False), reverse=True, limit=10):
            if (msg.from_ == "svc.qliksense@cultura.gov.br" and 
                ("naoresponda@serpro.gov.br" in msg.text or msg.from_ == "naoresponda@serpro.gov.br") and 
                msg.attachments):
                for anexo in msg.attachments:
                    # Mantém o nome original do arquivo
                    caminho = os.path.join(PASTA_DESTINO, anexo.filename)
                    os.makedirs(PASTA_DESTINO, exist_ok=True)
                    with open(caminho, "wb") as f:
                        f.write(anexo.payload)
                    print(f"📎 Anexo salvo em: {caminho}")
except MailboxLoginError as e:
    print("❌ Falha de login:", e)
except Exception as e:
    print("❌ Erro inesperado:", e)