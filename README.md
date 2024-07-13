# Simple fastAPI

## Local Setup

Prerequisites: Python, PostgreSQL and pgadmin4 should be installed on your system

### 1. Clone the repo

```bash
git clone <repo-url> project-name

cd project-name
```

### 2. Create a python virtual environment

```bash
python -m venv venv
```

### 3. Select a python interpreter

In visual studio code installing suggested python extensions should prompt you to select an interpreter. The recommended path is the python executable in your virtual environment folder:

- on windows:

```
venv/scripts/python.exe
```

### 4. Activate the virtual environment

In vscode's integrated terminal

- on windows:

```cmd
venv\scripts\activate
```

- on mac:

```bash
source venv/bin/activate 
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Setup Database

In pgadmin create a new database with the following connection details:

```
Host name/address: localhost
Port: 5432
Username: postgres
Password: postgres' password
```

### 7. Setup Environment variables

Save `.env.example` as `.env` and fill in the necessary values

### &. Start the server

- To run in **development**, server is reloaded when changes to python source files are saved

```bash
uvicorn app.main:app --reload
```

- To run in **production**, server won't be reloaded. A CI/CD pipeline will be need to update the server.

```bash
uvicorn app.main:app
```

## Documentation

Navigating to `http://localhost:8000/docs` in your browser should show the API documentation. HTTP requests can be sent to the server from the documentation page. 

If a blank page is displayed it means fastAPI couldn't reach the swagger cdn, just connect to the internet and reload page after that the docs should still be accessible when offline.
