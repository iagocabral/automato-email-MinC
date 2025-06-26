from imap_tools import MailBox, MailboxLoginError, AND # Importa classes e funções necessárias da biblioteca imap_tools
from dotenv import load_dotenv # Para carregar variáveis de ambiente de um arquivo .env
import os # Para interagir com o sistema operacional (caminhos de arquivo, diretórios)
import datetime # Não usado no script atual, mas útil para manipulação de datas

load_dotenv() # Carrega as variáveis do arquivo .env

# Define o caminho para a pasta onde os anexos serão salvos.
# Pega do ambiente ou usa './anexos' como padrão.
PASTA_DESTINO = os.getenv("PASTA_DESTINO", "./anexos")

# Pega as credenciais de e-mail das variáveis de ambiente.
# ATENÇÃO: Se sua conta possui Autenticação de Dois Fatores (MFA/2FA) ativada,
# você pode precisar de uma "senha de aplicativo" em vez da sua senha normal.
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

# Servidor IMAP para Gmail
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")

try:
    # Tenta conectar à caixa de e-mail IMAP usando as credenciais e o servidor especificado.
    print(f"🔄 Tentando conectar ao servidor IMAP: {IMAP_SERVER} com o e-mail: {EMAIL}...")
    with MailBox(IMAP_SERVER).login(EMAIL, SENHA) as mailbox:
        # Opcional: listar pastas para verificar conexão (pode ser removido em produção).
        folders = mailbox.folder.list()
        print(f"✅ Conexão IMAP com {IMAP_SERVER} foi bem-sucedida para {EMAIL}!")

        # Buscar emails não lidos (seen=False) que tenham anexos.
        # reverse=False busca do mais antigo para o mais novo, garantindo que o último do dia sobrescreva.
        # limit=10 busca nos últimos 10 e-mails não lidos.
        print("🔎 Buscando e-mails não lidos com anexos do remetente 'SERPRO' (do mais antigo para o mais novo)...")
        for msg in mailbox.fetch(AND(all=True), reverse=False, limit=10):
            # Condição de filtro: o e-mail deve ser do remetente "SERPRO" E deve ter anexos.
            # O conteúdo da mensagem (assunto ou texto) não é mais considerado.
            if (msg.from_ == "naoresponda@serpro.gov.br" and msg.attachments):
                
                print(f"📧 E-mail encontrado de: {msg.from_} com assunto: {msg.subject}")
                # Itera sobre cada anexo do e-mail
                for anexo in msg.attachments:
                    # Constrói o caminho completo para salvar o anexo, mantendo o nome original.
                    # O modo "wb" (write binary) sobrescreverá o arquivo se ele já existir,
                    # o que é desejado para manter os dados sempre atualizados com a última versão do dia.
                    caminho = os.path.join(PASTA_DESTINO, anexo.filename)
                    # Cria o diretório de destino se ele não existir
                    os.makedirs(PASTA_DESTINO, exist_ok=True)
                    
                    try:
                        with open(caminho, "wb") as f:
                            f.write(anexo.payload)
                        print(f"📎 Anexo '{anexo.filename}' salvo/sobrescrito em: {caminho}")
                    except IOError as io_err:
                        print(f"❌ Erro ao salvar o anexo '{anexo.filename}': {io_err}")
                
            else:
                # Mensagem para e-mails que não correspondem aos critérios de filtro (não são do SERPRO ou não têm anexos).
                print(f"⏭️ E-mail '{msg.subject}' (de: {msg.from_}) não corresponde aos critérios ou não possui anexos.")

except MailboxLoginError as e:
    # Captura erros de login. Fornece dicas para solução de problemas.
    print(f"❌ Falha de login ao conectar a {IMAP_SERVER}: {e}")
    print("Por favor, verifique:")
    print("1. Se o e-mail e a senha nas variáveis de ambiente (.env) estão corretos.")
    print("2. Se sua conta possui Autenticação de Dois Fatores (MFA/2FA) ativada e, se sim, se você precisa de uma 'senha de aplicativo' (App Password).")
    print("3. Se o acesso IMAP está habilitado para sua conta nas configurações do provedor de e-mail.")
except Exception as e:
    # Captura outros erros inesperados durante o processo.
    print(f"❌ Erro inesperado: {e}")
    print("Certifique-se de que o servidor IMAP está correto e que não há problemas de rede ou permissões de arquivo.")
