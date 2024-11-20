from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from gestao_projeto import Departamento, Funcionario, Projeto, Orcamento, Tarefa, FuncionariosProjetos, TarefasFuncionarios

# Conectando ao banco de dados
db_url = 'sqlite:///gestao_projetos.db'

# Conectando ao PostgreSQL
#db_url = 'postgresql+psycopg2://-nome de usuario do postgres-:-senha do postgres-@localhost/-nome da base de dados-'
#db_url = 'postgresql+psycopg2://postgres:admin@localhost/gestao_projetos'

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

def funcionario_departamento():
    
    # Com Join
    funcionarios = (
        session.query(Funcionario, Departamento).join(Departamento, Departamento.id==Funcionario.id_departamento)
    )   
    for funcionario, departamento in funcionarios:
        print(f'ID {funcionario.id}, NOME {funcionario.nome}, IDADE {funcionario.idade}, DEPARTAMENTO {departamento.nome}')
#------------------------------------------------------------------------------------------------------------------------------------------#
    # Sem Join
    funcionarios = (
        session.query(Funcionario)
    )
    for funcionario in funcionarios:
        print(f'ID {funcionario.id}, NOME {funcionario.nome}, IDADE {funcionario.idade}, DEPARTAMENTO {funcionario.departamento.nome}')

def funcionario_projeto():
#com sqlite = func.group_concat
#com postgresql = func.array_agg 
    # Com Join
    from sqlalchemy import func

    funcionarios_com_projetos = (
        session.query(
            Funcionario.nome, 
            func.array_agg(Projeto.nome)
        )
        .join(FuncionariosProjetos, Funcionario.id == FuncionariosProjetos.id_funcionario) 
        .join(Projeto, FuncionariosProjetos.id_projeto == Projeto.id) 
        .group_by(Funcionario.nome)
    )

    for funcionario_nome, projetos in funcionarios_com_projetos:
        print(f"NOME FUNCIONARIO {funcionario_nome}, PROJETOS {projetos}")

#------------------------------------------------------------------------------------------------------------#

    # Sem Join
        funcionarios_com_projetos = (
        session.query(Funcionario)
    )

    for funcionario in funcionarios_com_projetos:
        projetos = [projetos.projeto.nome for projetos in funcionario.projetos]
        print(f"NOME FUNCIONARIO {funcionario.nome}, PROJETOS {projetos}")
    
def projeto_orcamento():
    projetos = (
        session.query(Projeto)
        .join(Orcamento).where(Orcamento.valor_total>=40000)
    )    
    
    for projeto in projetos:
        print(f'NOME: {projeto.nome} VALOR TOTAL {projeto.orcamento.valor_total}')
    
def funcionarios_tarefas():
    tarefas_com_funcionarios = (
        session.query(
            Tarefa.descricao, 
            Tarefa.status, 
            Projeto.nome,
            func.array_agg(Funcionario.nome)
        )
        .join(TarefasFuncionarios, Tarefa.id == TarefasFuncionarios.id_tarefa)
        .join(Funcionario, TarefasFuncionarios.id_funcionario == Funcionario.id)
        .join(Projeto, Tarefa.id_projeto == Projeto.id)
        .where((Tarefa.status == 'Em progresso') | (Tarefa.status == 'Concluída'))
        .group_by(Tarefa.descricao, Tarefa.status, Projeto.nome)
        
    )

    for descricao, status, projeto_nome, funcionarios in tarefas_com_funcionarios:
        print(f"TAREFA: {descricao}, STATUS: {status}, PROJETO: {projeto_nome}, FUNCIONARIOS: {funcionarios}")

def projeto_orcamento_ordem():
    
    #ordem crescente
    projetos = (
        session.query(Projeto.nome, Orcamento)
        .join(Orcamento, Projeto.id == Orcamento.id_projeto)
        .order_by(Orcamento.saldo_disponivel)
    )

    # Iterando sobre os resultados e imprimindo
    for nome_projeto, orcamento in projetos:
        print(f"PROJETO: {nome_projeto}, SALDO DISPONÍVEL: {orcamento.saldo_disponivel}, VALOR TOTAL: {orcamento.valor_total}")

    #ordem decrescente
    projetos = (
        session.query(Projeto.nome, Orcamento)
        .join(Orcamento, Projeto.id == Orcamento.id_projeto)
        .order_by(Orcamento.saldo_disponivel.desc())
    )

    # Iterando sobre os resultados e imprimindo
    for nome_projeto, orcamento in projetos:
        print(f"PROJETO: {nome_projeto}, SALDO DISPONÍVEL: {orcamento.saldo_disponivel}, VALOR TOTAL: {orcamento.valor_total}")




