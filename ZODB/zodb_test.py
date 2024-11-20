from ZODB import DB
import ZODB.FileStorage
import transaction

# Configura o armazenamento e abre o banco de dados
storage = ZODB.FileStorage.FileStorage('meu_banco.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# Inicializa a lista de clientes, se não existir
root.setdefault('clientes', [])

# Função para listar todos os clientes
def listar_clientes():
    if not root['clientes']:
        print("Nenhum cliente encontrado.")
    else:
        for cliente in root['clientes']:
            print(f"Nome: {cliente['nome']}, Idade: {cliente['idade']}")

# Função para adicionar um novo cliente
def adicionar_cliente(nome, idade):
    root['clientes'].append({'nome': nome, 'idade': idade})
    transaction.commit()

# Função para atualizar a idade de um cliente existente
def atualizar_cliente(nome, nova_idade):
    for cliente in root['clientes']:
        if cliente['nome'] == nome:
            cliente['idade'] = nova_idade
            transaction.commit()
            return
    print(f"Cliente '{nome}' não encontrado.")

# Função para remover um cliente pelo nome
def remover_cliente(nome):
    root['clientes'] = [cliente for cliente in root['clientes'] if cliente['nome'] != nome]
    transaction.commit()

# Exemplo de operações
adicionar_cliente('João', 30)
adicionar_cliente('Rodrigo', 20)
adicionar_cliente('Laura', 25)
adicionar_cliente('Pedro', 12)
adicionar_cliente('Ana', 56)

print('--------------Insert--------------')
listar_clientes()

atualizar_cliente('João', 31)
atualizar_cliente('Ana', 6)

print('--------------Update--------------')
listar_clientes()

remover_cliente('Pedro')

print('--------------Remove--------------')
listar_clientes()


# Inspeção do root (opcional, para depuração)
print('--------------Root Info--------------')
print(f"Chaves: {list(root.keys())}")
print(f"Valores: {list(root.values())}")
print(f"Clientes: {root.get('clientes')}")

# Fecha a conexão e o banco
connection.close()
db.close()
