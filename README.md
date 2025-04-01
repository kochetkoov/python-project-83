### Hexlet tests and linter status:
[![Actions Status](https://github.com/kochetkoov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kochetkoov/python-project-83/actions)
[![CI Status](https://github.com/kochetkoov/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/kochetkoov/python-project-83/actions)

### Description

Page Analyzer is a simple web application that checks the basic page-level elements of websites valuable for on-page SEO.
Installation

Clone this repository to your local machine.
```
git clone git@github.com:kochetkoov/python-project-83.git
cd page-analyzer
```

Install dependencies using UV.
```
make install
```

Create the new .env file and define SECRET_KEY and DATABASE_URL variables there. For example,
```
echo "SECRET_KEY=secret_key" >> .env
echo "DATABASE_URL=postgresql://user:password@host:port/database_name" >> .env
```
Initialize the database manualy or using provided bash script.
```
make build
```
Run the app.
```
# using Gunicorn
make start
# then open http://0.0.0.0:8000 in your browser

# or using the Flask development server with debug mode
make dev
# then open http://localhost:8000 in your browser
```

### Demonstration of a project
You can try out Page Analyzer by clicking here. [click](https://python-project-83-b0x2.onrender.com/)