# Controller é a responsável pela lógica do programa

from Models import *
from DAO import *
from datetime import datetime


class ControllerCategoria:
    def cadastrarCategoria(self, novaCategoria):
        # Testa se existe a nova categoria no catálogo
        existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe = True
        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso!')
        else:
            print('A categoria já existe no sistema.')

    def removerCategoria(self, categoriaRemover):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))
        if len(cat) <= 0:
            print('A categoria não pode ser removida porque não existe no sistema')
        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break
            print('Categoria removida com sucesso!')

            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat2 = list(filter(lambda x: x.categoria == categoriaAlterada, x))
            if len(cat2) == 0:
                x = list(map(lambda x: Categoria(categoriaAlterada)
                         if (x.categoria == categoriaAlterar) else(x), x))
                print('Alteração efetuada com sucesso.')
            else:
                print('A categoria para qual deseja alterar já existe')
        else:
            print('A categoria que deseja alterar não existe.')

        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostrarCategoria(self):
        categorias = DaoCategoria.ler()
        if len(categorias) == 0:
            print('Categoria vazia')
        else:
            for i in categorias:
                print('Categoria: {}'.format(i.categoria))


class ControllerEstoque:
    def cadastrarProduto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()

        # verifica se existe a categoria do produto
        h = list(filter(lambda x: x.categoria == categoria, y))

        # verifica se existe o produto no estoque
        est = list(filter(lambda x: x.produto.nome == nome, x))
        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print('Produto cadastrado com sucesso')
            else:
                print('Produto já existe no estoque')
        else:
            print('Categoria não existe')

    def removerProduto(self, nome):
        x = DaoEstoque.ler()
        # verifica se existe o produto no estoque
        est = list(filter(lambda x: x.produto.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    break
            print('Produto removido com sucesso.')
        else:
            print(
                f"O Produto '{nome}' não pode ser removido porque não está cadastrado.")

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco +
                               "|" + i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')

    def alterarProduto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == novaCategoria, y))
        if len(h) > 0:
            est = list(filter(lambda x: x.produto.nome == nomeAlterar, x))
            if len(est) > 0:
                est = list(filter(lambda x: x.produto.nome == novoNome, x))
                if len(est) == 0:
                    x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if (
                        x.produto.nome == nomeAlterar) else (x), x))
                    print('Produto alterado com sucesso!')
                else:
                    print('O produto já está cadastrado.')

            else:
                print('O produto que deseja alterar não existe.')
        else:
            print('A categoria informada não existe.')

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco +
                               "|" + i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')

    def mostrarEstoque(self):
        estoque = DaoEstoque.ler()
        if len(estoque) == 0:
            print('Estoque vazio')
        else:
            print('-------------- PRODUTO --------------')
            for i in estoque:
                print(f'Nome: {i.produto.nome}\n'
                      f'Preco: R$ {i.produto.preco}\n'
                      f'Categoria: {i.produto.categoria}\n'
                      f'Quantidade {i.quantidade}')
                print()
            print('--------- Mercearia do João ---------')


class ControllerVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):

        x = DaoEstoque().ler()
        temp = []
        existe = False
        quantidade = False
        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= int(quantidadeVendida):
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                    vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)
                    valorCompra = int(quantidadeVendida) * int(i.produto.preco)
                    DaoVenda.salvar(vendido)
            temp.append(Estoque(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade))
            
        # Limpar o arquivo
        arq = open('estoque.txt', 'w')
        arq.write("")

        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(i.produto.nome +"|"+ i.produto.preco +"|"+ i.produto.categoria +"|"+ str(i.quantidade))
                arq.writelines('\n')
        
        if existe == False:
            print('O produto não existe')
            return None
        elif not quantidade:
            print('Estoque indisponível para a quantidade solicitada.')
            return None
        else:
            print('Venda realizada com sucesso!')
            return valorCompra

    def relatorioProdutos(self):
        vendas = DaoVenda.ler()
        produtos = []
  
        for i in vendas:
            nome = i.itensVendido.nome
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)}
                if (x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': int(quantidade)})

        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)

        print('Produtos mais vendidos: ')
        a = 1
        for j in ordenado:
            print(f'PRODUTO N° {a}')
            print(f"Produto: {j['produto']}\n"
                    f"Quantidade: {j['quantidade']}\n")
            a+=1

a = ControllerVenda()
a.relatorioProdutos()