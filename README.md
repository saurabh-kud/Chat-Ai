<h2 align='center'>Chat-Ai</h2>
<br/>

<p align="center">
   Chat-AI LLM powered advanced chat app 
</p>

#

An advanced Retrieval-Augmented Generation (RAG) powered chat application that allows users to interact with various file types using LLMs. It supports seamless communication with documents like PDFs, DOCX, Txt and CSV, providing accurate responses based on file content.

# tech stack used

Backend

- Python, FastApi, SqlAlchemy, langchain

Database

- postgres(sql)

VectorStore

- Qdrant-vector

## Installation

```sh

# Clone the repo
$ git clone https://github.com/saurabh-kud/Chat-Ai


# Setting Up ENV
> setup .env file for database and llm

APP_NAME="CHAT AI"
APP_VERSION=0.0.1
APP_HOST = "0.0.0.0"
PORT=8000
PYTHON_ENV=development
DOCS_ENABLED=True

GOOGLE_API_KEY=AI******************ohd
OPENAI_API_KEY=sk-**************************Prx

POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456


# Install Virtual Env
$ pip install virtualenv

# Create Virtual Environment
$ py -3 -m venv v_env

# Activate Virtual Env [Windows]
$ .\v_env\Scripts\activate

# Activate Virtual Env [Linux]
$ source v_env/bin/activate

# go to working directory
$ cd backend

# Install dependencies
$ pip install -r requirements.txt

# NOTE- if you are not running through docker then you have to run you psql server and qdrant-db seperately
$ docker run -p 6333:6333 qdrant/qdrant --name qdrant-db

# Migrate Using Alembic
$ alembic upgrade head

# Start server
$ uvicorn app.main:app

# Access
$ http://localhost:${PORT}/api/docs

# Using Docker
$ docker compose -f docker-compose.yml -p chatai-stack up -d --build --force-recreate --remove-orphans

# Access
$ http://localhost:${PORT}/api/docs

# Access your app
$ http://localhost:${PORT}

```

## Author

👤 **Saurabh kumar**

- Github: [@saurabh-kud](https://github.com/saurabh-kud)
- LinkedIN: [@saurabh-kud](https://www.linkedin.com/in/saurabh-kud/)

---

## License

&copy; Saurabh Kumar | MIT
