from persistent import Persistent
from persistent.mapping import PersistentMapping
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction

class Cliente(Persistent):
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def __repr__(self):
        return f'<Cliente {self.nome}, idade {self.idade}>'
    

storage = FileStorage('Data.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

if 'clientes' not in root:
    root['clientes'] = PersistentMapping()

clientes = root['clientes'] 


clientes['alice'] = Cliente('Alice', 30)
clientes['bob'] = Cliente('Bob', 25)
transaction.commit()


clientes['alice'].idade = 31
transaction.commit()


del clientes['alice']
transaction.abort()


for cliente in clientes.items():
    print(f"{cliente}")


print(root.keys())

connection.close()
db.close()
