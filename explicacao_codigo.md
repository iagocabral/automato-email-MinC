# Explicação Detalhada do Código

Este documento explica o funcionamento do script `baixar_arquivo.py` linha por linha.

## Importações

```python
from imap_tools import MailBox, MailboxLoginError
from dotenv import load_dotenv
import os
```

- `imap_tools`: Biblioteca para trabalhar com o protocolo IMAP, permitindo acessar caixas de email
- `MailboxLoginError`: Exceção específica para erros de login
- `load_dotenv`: Função para carregar variáveis de ambiente de um arquivo .env
- `os`: Módulo para interagir com o sistema operacional (manipulação de arquivos e diretórios)

## Carregamento das Variáveis de Ambiente

```python
load_dotenv()
```

Carrega as variáveis definidas no arquivo `.env` para o ambiente.

## Configurações

```python
PASTA_DESTINO = os.getenv("PASTA_DESTINO", "./anexos")
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")
```

- `PASTA_DESTINO`: Define onde os anexos serão salvos. Se não especificado no `.env`, usa "./anexos"
- `EMAIL`: Obtém o email do arquivo `.env`
- `SENHA`: Obtém a senha do arquivo `.env`

## Conexão e Processamento de Emails

```python
try:
    with MailBox('imap.gmail.com').login(EMAIL, SENHA) as mailbox:
        folders = mailbox.folder.list()
        print("✅ Conexão com Gmail IMAP foi bem-sucedida!")
```

- O código tenta se conectar ao servidor IMAP do Gmail usando as credenciais fornecidas
- Usa o padrão `with` para garantir que a conexão seja fechada adequadamente
- `folders = mailbox.folder.list()`: Lista as pastas disponíveis (não utilizado diretamente)
- Exibe mensagem de confirmação se a conexão for bem-sucedida

## Busca e Filtragem de Emails

```python
for msg in mailbox.fetch(reverse=True, limit=10):
    if (msg.from_ == "svc.qliksense@cultura.gov.br" and 
        ("naoresponda@serpro.gov.br" in msg.text or msg.from_ == "naoresponda@serpro.gov.br") and 
        msg.attachments):
```

- `mailbox.fetch(reverse=True, limit=10)`: Busca as 10 mensagens mais recentes
- O `if` verifica três condições:
  1. O remetente é "svc.qliksense@cultura.gov.br"
  2. E ("naoresponda@serpro.gov.br" está no texto do email OU o remetente é "naoresponda@serpro.gov.br")
  3. E a mensagem contém anexos

## Salvamento dos Anexos

```python
for anexo in msg.attachments:
    caminho = os.path.join(PASTA_DESTINO, anexo.filename)
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    with open(caminho, "wb") as f:
        f.write(anexo.payload)
    print(f"📎 Anexo salvo em: {caminho}")
```

- Percorre cada anexo da mensagem que atende aos critérios
- `caminho`: Constrói o caminho completo onde o arquivo será salvo
- `os.makedirs(PASTA_DESTINO, exist_ok=True)`: Cria a pasta de destino se não existir
- Abre um arquivo em modo de escrita binária e salva o conteúdo do anexo
- Exibe mensagem confirmando que o anexo foi salvo

## Tratamento de Erros

```python
except MailboxLoginError as e:
    print("❌ Falha de login:", e)
except Exception as e:
    print("❌ Erro inesperado:", e)
```

- Tratamento específico para erros de login
- Captura genérica para outros erros que possam ocorrer durante a execução
