from ZODB import DB
import ZODB.FileStorage
import transaction
from persistent import Persistent
from persistent.list import PersistentList

# Classes para representar os registros
class Cliente(Persistent):
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def __repr__(self):
        return f"Cliente(nome='{self.nome}', idade={self.idade})"

class Produto(Persistent):
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def __repr__(self):
        return f"Produto(nome='{self.nome}', preco={self.preco})"

# Função para inicializar tabelas
def inicializar_tabela(root, nome):
    if nome not in root:
        root[nome] = PersistentList()
    return root[nome]

# Funções simples para manipular registros
def listar(tabela):
    if not tabela:
        print("Nenhum registro encontrado.")
    else:
        for registro in tabela:
            print(registro)

def adicionar(tabela, registro):
    tabela.append(registro)
    transaction.commit()

def atualizar(tabela, filtro, novos_dados):
    for registro in tabela:
        if all(getattr(registro, k) == v for k, v in filtro.items()):
            for k, v in novos_dados.items():
                setattr(registro, k, v)
            transaction.commit()
            return
    print(f"Registro com filtro {filtro} não encontrado.")

def remover(tabela, filtro):
    # Filtra os registros que NÃO correspondem ao filtro
    novos_registros = []
    for registro in tabela:
        corresponde = all(getattr(registro, k) == v for k, v in filtro.items())
        if not corresponde:
            novos_registros.append(registro)
    
    # Atualiza a tabela com os registros restantes
    tabela[:] = novos_registros
    transaction.commit()


# Configuração do ZODB
storage = ZODB.FileStorage.FileStorage('meu_banco.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# Inicializando tabelas
clientes = inicializar_tabela(root, 'clientes')
produtos = inicializar_tabela(root, 'produtos')

# Adicionando registros
adicionar(clientes, Cliente('João', 30))
adicionar(clientes, Cliente('Rodrigo', 20))
adicionar(clientes, Cliente('Laura', 25))

adicionar(produtos, Produto('Notebook', 3500.00))
adicionar(produtos, Produto('Mouse', 50.00))
adicionar(produtos, Produto('Teclado', 150.00))

# Listando registros
print('--------------Clientes--------------')
listar(clientes)

print('--------------Produtos--------------')
listar(produtos)

# Atualizando registros
atualizar(clientes, {'nome': 'João'}, {'idade': 31})
atualizar(produtos, {'nome': 'Notebook'}, {'preco': 3400.00})

print('--------------Após Atualizações--------------')
print('Clientes:')
listar(clientes)
print('Produtos:')
listar(produtos)

# Removendo registros
remover(clientes, {'nome': 'Rodrigo'})
remover(produtos, {'nome': 'Mouse'})

print('--------------Após Remoções--------------')
print('Clientes:')
listar(clientes)
print('Produtos:')
listar(produtos)

# Inspeção do root (opcional, para depuração)
print('--------------Root Info--------------')
print(f"Chaves: {list(root.keys())}")
print(f"Valores: {list(root.values())}")
print(f"Clientes: {root.get('clientes')}")
print(f"Produtos: {root.get('produtos')}")


# Fecha conexão e banco
connection.close()
db.close()





