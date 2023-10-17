import hashlib
import datetime as date


class Block:
    # Propriedades do Bloco
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    # Gera um hash para o bloco, considerando suas propriedades
    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

    # Imprime no console de comando as propriedades do bloco
    def print(self):
        print()
        print(f'Block: {self.index}')
        print(f'Timestamp: {self.timestamp}')
        print(f'Hash anterior: {self.previous_hash}')
        print(f'Hash: {self.hash}')
        print(f'Dados: {self.data}')


class Blockchain:
    # Propriedades da Blockchain
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    # Gera o bloco genesis, que representa o bloco 0 da blockchain
    def create_genesis_block(self):
        return Block(0, date.datetime.now(), 'Genesis Block', '0')

    # Adiciona um novo bloco na blockchain
    def add_block(self, new_block):
        new_block.previous_hash = self.last_hash()
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    # Adiciona uma prescrição dentro de um bloco e em seguida adiciona este bloco na blockchain
    def add_prescription(self, prescription):
        new_block = Block(self.last_index() + 1,
                          date.datetime.now(),
                          prescription,
                          self.last_hash())
        self.add_block(new_block)

    # Consulta a blockchain e retorna um bloco que tenha um hash correspondente
    def get_block_by_hash(self, hash):
        block = None
        for b in self.chain:
            if b.hash == hash:
                block = b
                break
        return block

    # Retorna o valor de index do último bloco da blockchain
    def last_index(self):
        return self.chain[-1].index

    # Retorna o valor de hash do último bloco da blockchain
    def last_hash(self):
        return self.chain[-1].hash

    # Verifica se a estrutura da blockchain está válida
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False

            return True

    # Imprime no console de comando as propriedades da blockchain
    def print(self):
        for block in self.chain:
            block.print()


my_blockchain = Blockchain()

receita1 = {'info': 'Info 1'}
receita2 = {'info': 'Info 2'}

my_blockchain.add_prescription(receita1)
my_blockchain.add_prescription(receita2)

print('\n', '='*100, '\n')
print(f'Essa blockchain está válida? {str(my_blockchain.is_valid())}')
print('\n', '='*100, '\n')
my_blockchain.print()
print('\n', '='*100, '\n')
my_blockchain.get_block_by_hash(my_blockchain.last_hash()).print()
