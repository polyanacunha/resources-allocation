from flask_sqlalchemy import SQLAlchemy
from . import db
from sqlalchemy import Enum

db = SQLAlchemy()

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    carga_horaria_semanal = db.Column(db.Integer)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semestre = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.Enum('manhã', 'noite', name='periodo_enum'))

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)

class Professor_Disponibilidade(db.Model):
    __tablename__ = 'professor_disponibilidade'
    
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), primary_key=True)
    dia = db.Column(Enum('segunda', 'terça', 'quarta', 'quinta', 'sexta', name='dia_enum'), primary_key=True)
    periodo = db.Column(Enum('manhã', 'noite', name='periodo_enum'), primary_key=True)

    professor = db.relationship('Professor', backref=db.backref('disponibilidades', lazy=True))

class Disciplina_Professor(db.Model):
    __tablename__ = 'disciplina_professor'
    
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), primary_key=True)

    disciplina = db.relationship('Disciplina', backref=db.backref('professores', lazy=True))
    professor = db.relationship('Professor', backref=db.backref('disciplinas', lazy=True))

class Curso_Disciplina(db.Model):
    __tablename__ = 'curso_disciplina'
    
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), primary_key=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
    semestre = db.Column(db.Integer, primary_key=True)

    curso = db.relationship('Curso', backref=db.backref('disciplinas', lazy=True))
    disciplina = db.relationship('Disciplina', backref=db.backref('cursos', lazy=True))

class Turma_Disciplina(db.Model):
    __tablename__ = 'turma_disciplina'
    
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), primary_key=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), primary_key=True)
    dia = db.Column(Enum('segunda', 'terça', 'quarta', 'quinta', 'sexta', name='dia_enum'), primary_key=True)
    periodo = db.Column(Enum('manhã', 'noite', name='periodo_enum'), primary_key=True)

    turma = db.relationship('Turma', backref=db.backref('disciplinas', lazy='dynamic'))
    disciplina = db.relationship('Disciplina', backref=db.backref('turmas', lazy='dynamic'))
    professor = db.relationship('Professor', backref=db.backref('turmas', lazy='dynamic'))