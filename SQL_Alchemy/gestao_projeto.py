from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import date

#db_url = 'sqlite:///-nome do banco de dados-.db'
db_url = 'sqlite:///gestao_projetos.db'

# Conectando ao PostgreSQL
#db_url = 'postgresql+psycopg2://-nome de usuario do postgres-:-senha do postgres-@localhost/-nome da base de dados-'
#db_url = 'postgresql+psycopg2://postgres:admin@localhost/gestao_projetos'

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class Projeto(BaseModel):
    __tablename__ = 'projetos'
    
    nome = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)

    # 1 Projeto tem 1 Orcamento
    orcamento = relationship('Orcamento', back_populates='projeto', uselist=False)

    # N Projetos tem N Funcionarios
    funcionarios = relationship('FuncionariosProjetos', back_populates='projeto')

    # 1 Projeto tem N Tarefas
    tarefas = relationship('Tarefa', back_populates='projeto')
    
    
class Departamento(BaseModel):
    __tablename__ = 'departamentos'
    
    nome = Column(String(100), nullable=False)
    
    # 1 Departamento tem N Funcionarios
    funcionarios = relationship('Funcionario', back_populates='departamento')

    

class Funcionario(BaseModel):
    __tablename__ = 'funcionarios'
    
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    
    # N Funcionarios tem 1 Departamento
    id_departamento = Column(ForeignKey('departamentos.id'))
    departamento = relationship('Departamento', back_populates='funcionarios')

    # N Funcionarios tem N Projetos
    projetos = relationship('FuncionariosProjetos', back_populates='funcionario')

    # N Funcionarios tem N Tarefas
    tarefas = relationship('TarefasFuncionarios', back_populates='funcionario')


class Tarefa(BaseModel):
    __tablename__ = 'tarefas'
    
    descricao = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    
    # N Tarefas tem 1 Projeto
    id_projeto = Column(ForeignKey('projetos.id'))
    projeto = relationship('Projeto', back_populates='tarefas')

    # N Tarefas tem N Funcionarios
    funcionarios = relationship('TarefasFuncionarios', back_populates='tarefa')
    
    
class Orcamento(BaseModel):
    __tablename__ = 'orcamentos'
    
    saldo_disponivel = Column(Numeric(10, 2), nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    
    # 1 Orcamento tem 1 Projeto
    id_projeto = Column(ForeignKey('projetos.id'))
    projeto = relationship('Projeto', back_populates='orcamento')


class FuncionariosProjetos(Base):
    __tablename__ = 'funcionarios_projetos'
    
    id_funcionario = Column('id_funcionario', Integer, ForeignKey('funcionarios.id'), primary_key=True)
    id_projeto = Column('id_projeto', Integer, ForeignKey('projetos.id'), primary_key=True)

    funcionario = relationship('Funcionario', back_populates='projetos')
    projeto = relationship('Projeto', back_populates='funcionarios')


class TarefasFuncionarios(Base):
    __tablename__ = 'tarefas_funcionarios'
    
    id_tarefa = Column('id_tarefa', Integer, ForeignKey('tarefas.id'), primary_key=True)
    id_funcionario = Column('id_funcionario', Integer, ForeignKey('funcionarios.id'), primary_key=True)

    funcionario = relationship('Funcionario', back_populates='tarefas')
    tarefa = relationship('Tarefa', back_populates='funcionarios')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def addTeste():
    # Criando Departamentos
    departamento1 = Departamento(nome='TI')
    departamento2 = Departamento(nome='Marketing')

    # Criando Funcionários
    funcionario1 = Funcionario(nome='João Silva', idade=30, departamento=departamento1)
    funcionario2 = Funcionario(nome='Maria Oliveira', idade=28, departamento=departamento2)
    funcionario3 = Funcionario(nome='Carlos Pereira', idade=35, departamento=departamento1)
    funcionario4 = Funcionario(nome='Ana Costa', idade=32, departamento=departamento2)
    funcionario5 = Funcionario(nome='Roberto Souza', idade=40, departamento=departamento1)

    # Criando Projetos
    projeto1 = Projeto(nome='Projeto A', status='Em andamento', data_inicio=date(2024, 1, 1), data_fim=date(2024, 12, 31))
    projeto2 = Projeto(nome='Projeto B', status='Concluído', data_inicio=date(2023, 1, 1), data_fim=date(2023, 12, 31))
    projeto3 = Projeto(nome='Projeto C', status='Planejado', data_inicio=date(2024, 6, 1), data_fim=None)
    projeto4 = Projeto(nome='Projeto D', status='Em andamento', data_inicio=date(2024, 2, 1), data_fim=None)
    projeto5 = Projeto(nome='Projeto E', status='Planejado', data_inicio=date(2024, 5, 1), data_fim=None)

    # Criando Orçamentos para os Projetos
    orcamento1 = Orcamento(saldo_disponivel=10000.00, valor_total=20000.00, projeto=projeto1)
    orcamento2 = Orcamento(saldo_disponivel=0.00, valor_total=50000.00, projeto=projeto2)
    orcamento3 = Orcamento(saldo_disponivel=30000.00, valor_total=30000.00, projeto=projeto3)
    orcamento4 = Orcamento(saldo_disponivel=15000.00, valor_total=25000.00, projeto=projeto4)
    orcamento5 = Orcamento(saldo_disponivel=40000.00, valor_total=40000.00, projeto=projeto5)

    # Relacionamento N:N (associando Funcionários a Projetos)
    funcionarioprojeto1 = FuncionariosProjetos(funcionario=funcionario1, projeto=projeto1)
    funcionarioprojeto2 = FuncionariosProjetos(funcionario=funcionario2, projeto=projeto1)
    funcionarioprojeto3 = FuncionariosProjetos(funcionario=funcionario3, projeto=projeto2)
    funcionarioprojeto4 = FuncionariosProjetos(funcionario=funcionario4, projeto=projeto2)
    funcionarioprojeto5 = FuncionariosProjetos(funcionario=funcionario5, projeto=projeto3)
    funcionarioprojeto6 = FuncionariosProjetos(funcionario=funcionario1, projeto=projeto3)
    funcionarioprojeto7 = FuncionariosProjetos(funcionario=funcionario2, projeto=projeto4)
    funcionarioprojeto8 = FuncionariosProjetos(funcionario=funcionario3, projeto=projeto4)
    funcionarioprojeto9 = FuncionariosProjetos(funcionario=funcionario4, projeto=projeto5)
    funcionarioprojeto10 = FuncionariosProjetos(funcionario=funcionario5, projeto=projeto5)

    # Criando Tarefas para os Projetos
    tarefa1 = Tarefa(descricao='Desenvolver módulo A', status='Pendente', projeto=projeto1)
    tarefa2 = Tarefa(descricao='Testar módulo A', status='Em progresso', projeto=projeto1)
    tarefa3 = Tarefa(descricao='Documentação final', status='Concluída', projeto=projeto2)
    tarefa4 = Tarefa(descricao='Planejamento inicial', status='Planejado', projeto=projeto3)
    tarefa5 = Tarefa(descricao='Desenvolver módulo B', status='Em progresso', projeto=projeto4)
    tarefa6 = Tarefa(descricao='Reunião de início', status='Planejado', projeto=projeto5)

    # Relacionamento N:N (associando Funcionários a Tarefas)
    funcionariotarefa1 = TarefasFuncionarios(funcionario=funcionario1, tarefa=tarefa1)
    funcionariotarefa2 = TarefasFuncionarios(funcionario=funcionario2, tarefa=tarefa2)
    funcionariotarefa3 = TarefasFuncionarios(funcionario=funcionario4, tarefa=tarefa3)
    funcionariotarefa4 = TarefasFuncionarios(funcionario=funcionario5, tarefa=tarefa4)
    funcionariotarefa5 = TarefasFuncionarios(funcionario=funcionario3, tarefa=tarefa5)
    funcionariotarefa6 = TarefasFuncionarios(funcionario=funcionario5, tarefa=tarefa6)
    funcionariotarefa7 = TarefasFuncionarios(funcionario=funcionario1, tarefa=tarefa6)
    funcionariotarefa8 = TarefasFuncionarios(funcionario=funcionario2, tarefa=tarefa3)

    # Adicionando os objetos à sessão
    session.add_all([departamento1, departamento2, funcionario1, funcionario2, funcionario3, funcionario4, funcionario5])
    session.add_all([projeto1, projeto2, projeto3, projeto4, projeto5])
    session.add_all([orcamento1, orcamento2, orcamento3, orcamento4, orcamento5])
    session.add_all([funcionarioprojeto1, funcionarioprojeto2, funcionarioprojeto3, funcionarioprojeto4, funcionarioprojeto5, funcionarioprojeto6, funcionarioprojeto7, funcionarioprojeto8, funcionarioprojeto9, funcionarioprojeto10])
    session.add_all([tarefa1, tarefa2, tarefa3, tarefa4, tarefa5, tarefa6])
    session.add_all([funcionariotarefa1, funcionariotarefa2, funcionariotarefa3, funcionariotarefa4, funcionariotarefa5, funcionariotarefa6, funcionariotarefa7, funcionariotarefa8])

    session.commit()
    
    
if __name__ == '__main__':
    addTeste()

