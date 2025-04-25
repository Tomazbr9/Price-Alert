# 📉 Price Alert

O **Price Alert** é uma aplicação web desenvolvida com Django que permite aos usuários monitorar produtos online e receber alertas por e-mail sempre que houver uma alteração no preço. Ideal para quem deseja acompanhar ofertas e economizar em compras online.

---

## 🚀 Funcionalidades

- Cadastro de produtos por URL
- Rastreamento automático de preços via scraping
- Histórico de preços para cada produto
- Envio de alertas por e-mail quando o preço diminui
- Interface amigável com Bootstrap
- Execução de tarefas assíncronas com Celery

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11
- Django
- Celery + Redis
- Celery Beat
- Bootstrap 5
- SQLite (padrão) ou PostgreSQL
- SMTP para envio de e-mails

---

## ⚙️ Como Executar o Projeto

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/Tomazbr9/Price-Alert.git
    cd Price-Alert

2. **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt

4. **Configure as variáveis de ambiente:**
Crie um arquivo .env com as seguintes variáveis:
    ```bash
    EMAIL_HOST_USER=seu_email@example.com
    EMAIL_HOST_PASSWORD=sua_senha

5. **Aplique as migrações e inicie o servidor:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

6. **Inicie o worker e beat do Celery:**
    ```bash
    celery -A project worker --loglevel=info # Caso esteja no windows inclua --pool=solo
    celery -A project beat --loglevel=info

⏰ Configuração do Celery Beat no Admin
Para agendar tarefas periódicas:

Acesse o Django Admin (/admin)

Navegue até a seção "Periodic Tasks"

Clique em "Add periodic task" para criar um novo agendamento

Configure:

Task: Selecione a tarefa (ex: app.tasks.check_prices)

Schedule: Escolha um schedule existente ou crie um novo

Arguments: [Opcional] Argumentos para a tarefa

Enabled: Marque para ativar o agendamento

Exemplo de configuração para verificar preços a cada 2 horas:

Task: app.tasks.check_prices

Schedule: Crie um schedule do tipo "Crontab" com:

Minute: 0

Hour: */6

Day of week: *