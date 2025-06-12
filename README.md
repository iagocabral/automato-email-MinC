# Email Automato

Este script automatiza o processo de baixar anexos de emails específicos de uma conta Gmail.

## Funcionalidade

O script conecta-se a uma conta de email via IMAP, verifica as 10 mensagens mais recentes e salva os anexos de emails que atendam aos seguintes critérios:
- Remetente é "svc.qliksense@cultura.gov.br" e contém "naoresponda@serpro.gov.br" no corpo do email
- O remetente é "naoresponda@serpro.gov.br" e contém anexos

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python listadas em `requirements.txt`
- Conta Gmail com acesso IMAP ativado
- Permissão para aplicativos menos seguros (ou uso de senha de aplicativo)

## Instalação

1. Clone este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um arquivo `.env` na pasta raiz do projeto com as seguintes variáveis:

```
EMAIL=seu.email@gmail.com
SENHA=sua_senha_ou_senha_de_aplicativo
PASTA_DESTINO=./caminho/para/salvar/anexos
```

Observações:
- EMAIL: seu endereço de email completo
- SENHA: sua senha de email ou senha de aplicativo (recomendado)
- PASTA_DESTINO: caminho onde os anexos serão salvos (padrão é "./anexos" se não especificado)

## Execução

Para executar o script:

```bash
python baixar_arquivo.py
```

O script irá:
1. Conectar à conta de email especificada
2. Verificar as 10 mensagens mais recentes
3. Baixar anexos de emails que correspondam aos critérios
4. Salvar os anexos na pasta configurada

# Sugestão de uso
É recomendável agendar a execução do script em horários definidos por meio de um agendador de tarefas (como cron, no Linux/macOS, ou o Agendador de Tarefas do Windows). Isso permite a automação do processo sem a necessidade de manter o script em execução contínua, otimizando o uso de recursos da máquina.