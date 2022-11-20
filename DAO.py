
# Camada mais inferior da model, a DAO é o Data Acess Object
# (Objeto de acesso ao dados)

from Models import *

class DaoCategoria:
    @classmethod
    def salvar(cls, categoria):
        with open("categoria.txt", 'a') as arq:
            arq.writelines(categoria)
            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open("categoria.txt", 'r') as arq:
           cls.categoria = arq.readlines()

        cls.categoria = list(map(lambda x: x.replace('\n', ''), cls.categoria))

        cat = []

        for i in cls.categoria:
            cat.append(Categoria(i))
        
        return cat

class DaoVenda:
    @classmethod
    def salvar(cls, venda: Venda):
        with open('venda.txt', 'a') as arq:
            arq.writelines(venda.itensVendido.nome + "|" + venda.itensVendido.preco + "|" +
            venda.itensVendido.categoria + "|" + venda.vendedor + 
            "|"+ venda.comprador + "|" + str(venda.quantidadeVendida) + 
            "|" + venda.data)

            arq.writelines('\n')

    @classmethod
    def ler(cls):
        with open('venda.txt', 'r') as arq:
            cls.venda = arq.readlines()

        cls.venda = list(map(lambda x: x.replace('\n', ''), cls.venda))
        cls.venda = list(map(lambda x: x.split('|'), cls.venda))
        
        vend = []
        for i in cls.venda:
            vend.append(Venda(Produtos(i[0], i[1], i[2], i[3], i[4], i[5], i[6])))
        return vend


DaoVenda.ler()