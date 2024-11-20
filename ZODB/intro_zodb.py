from persistent import Persistent
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction

class Birthday(Persistent):
    def __init__(self, name, birthdate):
        self.name = name
        self.birthday = birthdate

    def __repr__(self):
        return f'<Birthday {self.name}, {self.birthday}>'

# Configuração do banco
storage = FileStorage('Data.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# Adicionando objetos persistentes ao root
root['alice'] = Birthday('Alice', '01/01/1970')
root['bob'] = Birthday('Bob', '02/02/1980')
transaction.commit()

# Abortando uma transação para verificar o efeito
root['alice'] = 'Agora String!'
transaction.abort()  # Reverte a alteração
print(root['alice'])  # Deve imprimir o objeto Birthday original

# Alterando atributos dos objetos
root['alice'].birthday = '01/01/1990'
root['bob'].birthday = '01/01/2000'
transaction.commit()  # Salva as alterações

# Exibindo os resultados
print(root['alice'])
print(root['bob'])
print('Alice:', root['alice'].birthday)

del root['alice']
transaction.abort()


print(root.keys())
print(root.values())
# Fechando o banco
connection.close()
db.close()
