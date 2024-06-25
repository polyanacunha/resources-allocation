from flask import request, jsonify
from flask_cors import CORS
from app import app, db
from app.models import Professor, Disciplina, Turma, Curso, Professor_Disponibilidade, Disciplina_Professor, Curso_Disciplina


CORS(app)

@app.route('/submit-data', methods=['POST'])
def submit_data():
    data = request.get_json()

    try:
        # Adicionando Professor
        professor = Professor(nome=data['professor']['nome'], email=data['professor']['email'])
        db.session.add(professor)

        # Adicionando Disciplina
        disciplina = Disciplina(
            nome=data['disciplina']['nome'],
            carga_horaria_semanal=data['disciplina']['cargaHorariaSemanal']
        )
        db.session.add(disciplina)

        # Adicionando Turma
        turma = Turma(
            semestre=data['turma']['semestre'],
            periodo=data['turma']['periodo']
        )
        db.session.add(turma)

        # Adicionando Curso
        curso = Curso(nome=data['curso']['nome'])
        db.session.add(curso)

        # Salvando tudo para obter IDs
        db.session.commit()

        # Adicionando relações
        professor_disponibilidade = Professor_Disponibilidade(
            professor_id=professor.id,
            dia=data['disponibilidade']['dia'],
            periodo=data['disponibilidade']['periodo']
        )
        db.session.add(professor_disponibilidade)

        disciplina_professor = Disciplina_Professor(
            disciplina_id=disciplina.id,
            professor_id=professor.id
        )
        db.session.add(disciplina_professor)

        curso_disciplina = Curso_Disciplina(
            curso_id=curso.id,
            disciplina_id=disciplina.id,
            semestre=data['cursoDisciplina']['semestre']
        )
        db.session.add(curso_disciplina)

        db.session.commit()

        return jsonify({'message': 'Dados salvos com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
