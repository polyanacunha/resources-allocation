# from flask import Flask
# from app.models import db, Professor, Disciplina, Turma, Curso, Professor_Disponibilidade, Disciplina_Professor, Curso_Disciplina, Turma_Disciplina
# from config import Config
# import random
# import json

# app = Flask(__name__)
# app.config.from_object(Config)

# db.init_app(app)

# def generate_schedule():
#     with app.app_context():
#         try:
#             disciplinas = Disciplina.query.all()
#             turmas = Turma.query.all()
#             schedule = []

#             # Dicionário para rastrear horários ocupados pelos professores
#             professor_schedule = {}

#             print("Iniciando a geração de horários...")
#             for turma in turmas:
#                 schedule_map = {f"{dia}_{periodo}": None for dia in ['segunda', 'terça', 'quarta', 'quinta', 'sexta'] for periodo in ['manhã', 'noite']}

#                 for disciplina in disciplinas:
#                     curso_disciplina = Curso_Disciplina.query.filter_by(
#                         disciplina_id=disciplina.id, semestre=turma.semestre
#                     ).first()
#                     if not curso_disciplina:
#                         continue

#                     for key in schedule_map:
#                         day, period = key.split('_')
#                         if schedule_map[key] is None:
#                             available_profs = Professor_Disponibilidade.query \
#                                 .join(Disciplina_Professor, Disciplina_Professor.professor_id == Professor_Disponibilidade.professor_id) \
#                                 .filter(Disciplina_Professor.disciplina_id == disciplina.id,
#                                         Professor_Disponibilidade.dia == day,
#                                         Professor_Disponibilidade.periodo == period).all()

#                             for prof in available_profs:
#                                 # Verifica se o professor já está ocupado no mesmo horário
#                                 if f"{prof.professor_id}_{day}_{period}" not in professor_schedule:
#                                     prof_choice = prof
#                                     nova_turma_disciplina = Turma_Disciplina(
#                                         turma_id=turma.id,
#                                         disciplina_id=disciplina.id,
#                                         professor_id=prof_choice.professor_id,
#                                         dia=day,
#                                         periodo=period
#                                     )
#                                     db.session.add(nova_turma_disciplina)

#                                     schedule_detail = {
#                                         "turma": turma.id,
#                                         "disciplina": disciplina.nome,
#                                         "professor": prof_choice.professor.nome,
#                                         "dia": day,
#                                         "periodo": period
#                                     }
#                                     schedule.append(schedule_detail)
#                                     schedule_map[key] = disciplina.nome  # Marca como ocupado
#                                     professor_schedule[f"{prof_choice.professor_id}_{day}_{period}"] = True  # Marca o professor como ocupado

#                                     print(f"Configuração escolhida: {schedule_detail}")
#                                     break

#             db.session.commit()
#             print("Horários gerados e salvos com sucesso.")
            
#             # Salvando a configuração no arquivo JSON
#             with open('schedule.json', 'w') as f:
#                 json.dump(schedule, f, indent=4)
#             print("Configuração salva em 'schedule.json'.")

#             return "Schedule generated and saved successfully"
#         except Exception as e:
#             db.session.rollback()
#             print(f"Error: {e}")
#             return str(e)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # Cria tabelas do banco de dados se ainda não estiverem criadas
#         result = generate_schedule()  # Gera o horário e salva no banco
#         print(result)  # Imprime o resultado da operação


from flask import Flask
from app.models import db, Disciplina, Turma, Professor_Disponibilidade, Disciplina_Professor, Curso_Disciplina, Turma_Disciplina
from config import Config
import random
import json

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def generate_schedule():
    with app.app_context():
        try:
            disciplinas = Disciplina.query.all()
            turmas = Turma.query.all()
            schedule = []

            print("Iniciando a geração de horários...")
            for turma in turmas:
                # Inicia um mapa para controlar os horários ocupados e os professores designados por disciplina
                schedule_map = {f"{dia}_{turma.periodo}": None for dia in ['segunda', 'terça', 'quarta', 'quinta', 'sexta']}
                assigned_professors = {}  # Dicionário para rastrear os professores designados para cada disciplina

                for disciplina in disciplinas:
                    curso_disciplina = Curso_Disciplina.query.filter_by(
                        disciplina_id=disciplina.id, semestre=turma.semestre
                    ).first()
                    if not curso_disciplina:
                        continue

                    # Cálculo de quantas sessões são necessárias
                    sessions_needed = disciplina.carga_horaria_semanal // 2
                    while sessions_needed > 0:
                        # Verifica se já temos um professor designado para essa disciplina
                        if disciplina.id in assigned_professors:
                            prof_choice = assigned_professors[disciplina.id]
                        else:
                            # Procura por professores disponíveis que ensinam a disciplina e estão disponíveis no período da turma
                            available_profs = db.session.query(Professor_Disponibilidade).\
                                join(Disciplina_Professor, Disciplina_Professor.professor_id == Professor_Disponibilidade.professor_id).\
                                filter(Disciplina_Professor.disciplina_id == disciplina.id,
                                       Professor_Disponibilidade.periodo == turma.periodo).all()

                            if not available_profs:
                                break  # Se não encontrar professores disponíveis, interrompe a tentativa de agendamento

                            prof_choice = random.choice(available_profs)
                            assigned_professors[disciplina.id] = prof_choice  # Atribui o professor para todas as sessões dessa disciplina

                        # Encontra um horário disponível
                        for key in schedule_map:
                            if schedule_map[key] is None:
                                day, _ = key.split('_')
                                nova_turma_disciplina = Turma_Disciplina(
                                    turma_id=turma.id,
                                    disciplina_id=disciplina.id,
                                    professor_id=prof_choice.professor_id,
                                    dia=day,
                                    periodo=turma.periodo
                                )
                                db.session.add(nova_turma_disciplina)

                                schedule_detail = {
                                    "turma": turma.id,
                                    "disciplina": disciplina.nome,
                                    "professor": prof_choice.professor.nome,
                                    "dia": day,
                                    "periodo": turma.periodo
                                }
                                schedule.append(schedule_detail)
                                schedule_map[key] = disciplina.nome  # Marca o horário como ocupado

                                sessions_needed -= 1
                                if sessions_needed == 0:
                                    break

            db.session.commit()
            print("Horários gerados e salvos com sucesso.")

            # Salvando a configuração no arquivo JSON
            with open('schedule.json', 'w') as f:
                json.dump(schedule, f, indent=4)
            print("Configuração salva em 'schedule.json'.")

            return "Schedule generated and saved successfully"
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return str(e)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        result = generate_schedule()
        print(result)