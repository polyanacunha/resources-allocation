# seed.py
from app import create_app, db
from app.models import Professor, Disciplina, Curso, Turma, Professor_Disponibilidade, Disciplina_Professor, Curso_Disciplina, Turma_Disciplina

def add_data():
    # Criando alguns professores
    prof1 = Professor(nome='Prof. Eliel', email='eliel@example.com')
    prof2 = Professor(nome='Prof. Wilson', email='wilson@example.com')

    # Criando algumas disciplinas
    disc1 = Disciplina(nome='Teoria dos Grafos', carga_horaria_semanal=4)
    disc2 = Disciplina(nome='Processamento de Imagens', carga_horaria_semanal=3)
    disc3 = Disciplina(nome='HTML', carga_horaria_semanal=2)

    # Criando um curso
    curso1 = Curso(nome='Ciência da Computação')

    # Criando turmas
    turma1 = Turma(semestre=5, periodo='manhã')
    turma2 = Turma(semestre=5, periodo='noite')

    # Disponibilidades
    disp1 = Professor_Disponibilidade(dia='segunda', periodo='manhã', professor=prof1)
    disp2 = Professor_Disponibilidade(dia='quarta', periodo='noite', professor=prof2)

    # Relacionando professores e disciplinas
    dp1 = Disciplina_Professor(professor=prof1, disciplina=disc3)
    dp2 = Disciplina_Professor(professor=prof2, disciplina=disc1)
    dp3 = Disciplina_Professor(professor=prof2, disciplina=disc2)

    # Relacionando curso e disciplinas
    cd1 = Curso_Disciplina(curso=curso1, disciplina=disc1, semestre=5)
    cd2 = Curso_Disciplina(curso=curso1, disciplina=disc2, semestre=5)
    cd3 = Curso_Disciplina(curso=curso1, disciplina=disc3, semestre=5)
    
    
    # Associando turmas, disciplinas e professores
    td1 = Turma_Disciplina(turma_id=turma1.id, disciplina_id=disc1.id, professor_id=prof2.id, dia='segunda', periodo='manhã')
    td2 = Turma_Disciplina(turma_id=turma1.id, disciplina_id=disc2.id, professor_id=prof2.id, dia='terça', periodo='manhã')
    td3 = Turma_Disciplina(turma_id=turma2.id, disciplina_id=disc3.id, professor_id=prof1.id, dia='quarta', periodo='noite')

    # Adicionando tudo ao banco
    db.session.add_all([prof1, prof2, disc1, disc2, disc3, curso1, turma1, turma2, disp1, disp2, dp1, dp2, dp3, cd1, cd2, cd3])
    db.session.commit()

    print("Database populated with sample data!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        add_data()
