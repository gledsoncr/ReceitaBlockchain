import hashlib
import datetime as date


class Block:
    # Propriedades do Bloco
    def __init__(self, index, timestamp, previous_hash, validation_key, data):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.validation_key = validation_key
        self.search_id = self.calculate_search_id()
        self.hash = self.calculate_hash()

    # Gera um hash curto baseado no index do bloco
    def calculate_search_id(self):
        shake = hashlib.shake_128()
        shake.update(str(self.index).encode('utf-8'))
        return shake.hexdigest(3)

    # Gera um hash para o bloco, considerando suas propriedades
    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8') +
                   str(self.validation_key).encode('utf-8'))
        return sha.hexdigest()

    # Imprime no console de comando as propriedades do bloco
    def print(self):
        print()
        print(f'Block: {self.index}')
        print(f'Timestamp: {self.timestamp}')
        print(f'Hash anterior: {self.previous_hash}')
        print(f'Hash: {self.hash}')
        print(f'Chave de validação: {self.validation_key}')
        print(f'Código de consulta: {self.search_id}')
        print(f'Dados: {self.data}')


class Blockchain:
    # Propriedades da Blockchain
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    # Gera o bloco genesis, que representa o bloco 0 da blockchain
    def create_genesis_block(self):
        return Block(0, date.datetime.now(), '0', '00000', 'Genesis Block')

    # Adiciona um novo bloco na blockchain com uma chave de validação
    def add_block(self, validation_key, data):
        new_block = Block(self.last_index() + 1,
                          date.datetime.now(),
                          self.last_hash(),
                          validation_key,
                          data)
        self.chain.append(new_block)

    # Consulta a blockchain e retorna um bloco que tenha um search_id correspondente
    def get_block_by_search_id(self, search_id):
        block = None
        for b in self.chain:
            if b.search_id == search_id:
                block = b
                break
        return block

    # Verifica se uma chave de validação é válida para um determinado bloco
    def validation_key_is_valid(self, search_id, validation_key):
        block = self.get_block_by_search_id(search_id)
        if block == None:
            return False
        if block.validation_key != validation_key:
            return False
        return True

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

data1 = {'info': 'Info 1'}
my_blockchain.add_block(41235, data1)

data2 = {'info': 'Info 2'}
my_blockchain.add_block(65236, data2)

print('\n', '='*100, '\n')
print('- TESTANDO A VALIDAÇÃO DA ESTRUTURA DE DADOS DA BLOCKCHAIN')
print(f'Essa blockchain está válida? {str(my_blockchain.is_valid())}')

print('\n', '='*100, '\n')
print('- VISUALIZANDO A BLOCKCHAIN')
my_blockchain.print()

print('\n', '='*100, '\n')
print('- VERIFICANDO SE UMA CHAVE DE VALIDAÇÃO É VÁLIDA')
print(
    f'\nChave de validação: {65236}\nCódigo de consulta: 4e9e38\nÉ válida? {my_blockchain.validation_key_is_valid("4e9e38", 65236)}')
print(
    f'\nChave de validação: 56321\nCódigo de consulta: b35269\nÉ válida? {my_blockchain.validation_key_is_valid("b35269", 56321)}')
