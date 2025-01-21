##Criar e Ativar o Ambiente Virtual##

python -m venv venv_nome
source venv_nome/bin/activate  # Linux/MacOS

##Instalar Dependências##

pip install pip-tools
pip-sync

##Configurar o Certificado do Banco de Dados (se necessário)##

    Baixe o certificado do Tembo, caso seja necessário.

##Ajustar o Arquivo .env##

    Configure as variáveis: SECRET_KEY, informações de banco de dados (host, nome, usuário, senha) e SSL, se necessário.

##Rodar o Servidor de Desenvolvimento##

python manage.py runserver

Reativar o Ambiente Virtual (sempre que necessário)
Navegue até a pasta do ambiente virtual e execute:

source bin/activate  # Linux/MacOS
