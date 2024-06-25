## Activate virtual env python :
python3.11 -m venv .
. ./bin/activate

## Install dependencies
pip install Flask SQLAlchemy psycopg2 flask_cors

## Send request
curl -X GET http://127.0.0.1:5000/generate-schedule -H "Content-Type: application/json"

## Para rodar as migrations:
flask db init
flask db migrate -m "Descrição da migração"
flask db upgrade

## Apagar todos os dados de todas as tabelas sem apagar as tabelas
TRUNCATE TABLE professor_disponibilidade, curso_disciplina, disciplina_professor, turma, turma_disciplina, curso, disciplina, professor, turma_disciplina

## Limpar dados da tabela turma_disciplina
delete from turma_disciplina;

## Para rodar o frontend:
npm run start

## Para rodar o backend:
python -m flask run

## Para rodar o arquivo com a lógica de negócio:
python main.py

## script para popular o banco
python seed.py

## add your own SQLALCHEMY_DATABASE_URI on config.py file