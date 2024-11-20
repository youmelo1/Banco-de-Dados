from ZODB import DB
from ZODB.FileStorage import FileStorage
from persistent import Persistent
import transaction

# Classe para representar um contato
class Contato(Persistent):
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email

    def atualizar_telefone(self, novo_telefone):
        self.telefone = novo_telefone

    def atualizar_email(self, novo_email):
        self.email = novo_email

    def __repr__(self):
        return f"Contato(nome={self.nome}, telefone={self.telefone}, email={self.email})"

# Funções CRUD para gerenciar os contatos
def adicionar_contato(root, nome, telefone, email):
    contato = Contato(nome, telefone, email)
    root.contatos[nome] = contato
    transaction.commit()
    print(f"Contato '{nome}' adicionado com sucesso.")

def listar_contatos(root):
    if root.contatos:
        print("Lista de contatos:")
        for nome, contato in root.contatos.items():
            print(contato)
    else:
        print("Nenhum contato encontrado.")

def atualizar_contato(root, nome, telefone=None, email=None):
    contato = root.contatos.get(nome)
    if contato:
        if telefone:
            contato.atualizar_telefone(telefone)
        if email:
            contato.atualizar_email(email)
        transaction.commit()
        print(f"Contato '{nome}' atualizado.")
    else:
        print(f"Contato '{nome}' não encontrado.")

def remover_contato(root, nome):
    if nome in root.contatos:
        del root.contatos[nome]
        transaction.commit()
        print(f"Contato '{nome}' removido.")
    else:
        print(f"Contato '{nome}' não encontrado.")

# Configurações de Banco de Dados e Estrutura Inicial
storage = FileStorage('ContatosData.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# Inicializa o dicionário de contatos, se não existir
if not hasattr(root, 'contatos'):
    root.contatos = {}

# Menu de Opções
while True:
    print("\nMenu de Opções:")
    print("1. Adicionar contato")
    print("2. Listar contatos")
    print("3. Atualizar contato")
    print("4. Remover contato")
    print("5. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        adicionar_contato(root, nome, telefone, email)
    elif opcao == "2":
        listar_contatos(root)
    elif opcao == "3":
        nome = input("Nome do contato a atualizar: ")
        telefone = input("Novo telefone (ou deixe em branco): ")
        email = input("Novo email (ou deixe em branco): ")
        atualizar_contato(root, nome, telefone if telefone else None, email if email else None)
    elif opcao == "4":
        nome = input("Nome do contato a remover: ")
        remover_contato(root, nome)
    elif opcao == "5":
        print("Saindo...")
        break
    else:
        print("Opção inválida.")

# Fecha a conexão e o banco de dados
connection.close()
db.close()
