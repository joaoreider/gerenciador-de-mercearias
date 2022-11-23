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

            with open('dados/categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')
            

        estoque = DaoEstoque.ler()
        estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, "Sem categoria"), x.quantidade)
                        if (x.produto.categoria == categoriaRemover) else (x), estoque))
        
        
        with open('dados/estoque.txt', 'w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + "|" + i.produto.preco +
                               "|" + i.produto.categoria + "|" + str(i.quantidade))
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

                estoque = DaoEstoque.ler()
                estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, categoriaAlterada), x.quantidade)
                                if (x.produto.categoria == categoriaAlterar) else (x), estoque))
                
                
                with open('dados/estoque.txt', 'w') as arq:
                    for i in estoque:
                        arq.writelines(i.produto.nome + "|" + i.produto.preco +
                                        "|" + i.produto.categoria + "|" + str(i.quantidade))
                        arq.writelines('\n')


            else:
                print('A categoria para qual deseja alterar já existe')
        else:
            print('A categoria que deseja alterar não existe.')

        with open('dados/categoria.txt', 'w') as arq:
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

        with open('dados/estoque.txt', 'w') as arq:
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

        with open('dados/estoque.txt', 'w') as arq:
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
        arq = open('dados\estoque.txt', 'w')
        arq.write("")

        for i in temp:
            with open('dados/estoque.txt', 'a') as arq:
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
    
    def mostrarVenda(self, dataInicio, dataTermino):
        vendas = DaoVenda.ler()
        dataInicio1 = datetime.strptime(dataInicio, '%d/%m/%Y')
        dataTermino1 = datetime.strptime(dataTermino, '%d/%m/%Y')

        vendasSelecionadas = list(filter(lambda x: datetime.strptime(x.data, '%d/%m/%Y') >= dataInicio1
                                        and datetime.strptime(x.data, '%d/%m/%Y') <= dataTermino1, vendas))
        

        count = 1
        total = 0
        for i in vendasSelecionadas:
            print(f"---------- VENDA [{count}] ----------")
            print(f"Nome: {i.itensVendido.nome}\n"
                    f"Categoria: {i.itensVendido.categoria}\n"
                    f"Data: {i.data}\n"
                    f"Quantidade: {i.quantidadeVendida}\n"
                    f"Cliente: {i.comprador}\n"
                    f"Vendedor: {i.vendedor}\n")
            total+=int(i.itensVendido.preco) * int(i.quantidadeVendida)
            count+=1
        print(f"TOTAL: {total}\n")

class ControllerFornecedor():
    def cadastrarFornecedor(self, nome, cnpj, telefone, categoria):
        x = DaoFornecedor.ler()
        listaCnpj = list(filter(lambda x: x.cnpj == cnpj, x))
        listaTelefone = list(filter(lambda x: x.telefone == telefone, x))

        if len(listaCnpj)>0:
            print('O Cnpj já está cadastrado no sistema.')
        elif len(listaTelefone) > 0:
            print('O telefone já existe')
        else:
            if len(cnpj) == 14 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFornecedor.salvar(Fornecedor(nome, cnpj, telefone, categoria))
            else:
                print("Digite um cnpj ou telefone válido")
    
    def alterarFornecedor(self, nomeAlterar, novoNome, novoCnpj, novoTelefone, novoCategoria):
        x = DaoFornecedor.ler()
        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est)>0:
            est = list(filter(lambda x: x.cnpj == novoCnpj, x))
            if len(est) == 0:
                x = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone, novoCategoria)
                if(x.nome == nomeAlterar) else (x), x))
            else:
                print('CNPJ já existe.')
        else:
            print('O fornecedor que deseja alterar não existe')
        
        with open('dados/fornecedores.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cnpj+
                               "|" + i.telefone + "|" + str(i.categoria))
                arq.writelines('\n')
            print('Fornecedor alterado com sucesso')
        
    
    def removerFornecedor(self, nome):
        x = DaoFornecedor.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
            print('Fornecedor removido com sucesso.')
        else:
            print(f"O Fornecedor não pode ser removido porque não está cadastrado.")

        with open('dados/forncedores.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cnpj+
                               "|" + i.telefone + "|" + str(i.categoria))
                arq.writelines('\n')
            print('Fornecedor removido com sucesso')
    

    def mostrarFornecedores(self):
        fornecedores = DaoFornecedor.ler()
        if len(fornecedores) == 0:
            print('A lista de fornecedores está vazia.')
        else:

            print('-------------- FORNECEDORES --------------')
            for i in fornecedores:
                print(f'Categoria: {i.categoria}\n'
                      f'Nome {i.nome}\n'
                      f'Telefone: {i.telefone}\n'
                      f'CNPJ {i.cnpj}')
                print()
            print('--------- Mercearia do João ---------')


class ControllerCliente:
    def cadastrarCliente(self, nome, telefone, cpf, email, endereco):
        x = DaoPessoa.ler()
        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
  
        if len(listaCpf)>0:
            print('O Cpf já está cadastrado no sistema.')
        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <= 11:
                DaoPessoa.salvar(Pessoa(nome, telefone, cpf, email, endereco))
                print('Cliente cadastrado com sucesso')
            else:
                print("Digite um cpf ou telefone válido")
    
    def alterarCliente(self, nomeAlterar, novoNome, novoTelefone,novoCpf, novoEmail, novoEndereco):
        x = DaoPessoa.ler()
        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est)>0:

            x = list(map(lambda x: Pessoa(novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco)
            if(x.nome == nomeAlterar) else (x), x))

        else:
            print('O Cliente que deseja alterar não existe')
        
        with open('dados/clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone+
                               "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Cliente alterado com sucesso')

    def removerCliente(self, nome):
        x = DaoPessoa.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
            print('Cliente removido com sucesso.')
        else:
            print(f"O Cliente não pode ser removido porque não está cadastrado.")
            return None

        with open('dados/clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone+
                               "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Cliente removido com sucesso')
    
    def mostrarClientes(self):
        clientes = DaoPessoa.ler()
        if len(clientes) == 0:
            print('A lista de clientes está vazia.')
        else:

            print('-------------- CLIENTES --------------')
            for i in clientes:
                print(f'Nome {i.nome}\n'
                      f'Telefone: {i.telefone}\n'
                      f'Endereço: {i.endereco}\n'
                      f'Email {i.email}'
                      f'CPF: {i.cpf}\n')

                print()
            print('--------- Mercearia do João ---------')


class ControllerFuncionario:
    def cadastrarFuncionario(self, clt, nome, telefone, cpf, email, endereco):
        x = DaoFuncionario.ler()
        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        listaClt = list(filter(lambda x: x.clt == clt, x))
        if len(listaCpf)>0:
            print('O Cpf já está cadastrado no sistema.')
        elif len(listaClt) > 0:
            print('CLT já está cadastrada no sistema.')

        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <= 11:
                DaoFuncionario.salvar(Funcionario(clt, nome, telefone, cpf, email, endereco))
                print('Funcionário cadastrado com sucesso')
            else:
                print("Digite um cpf ou telefone válido")
    
    def alterarFuncionario(self, nomeAlterar, novoClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        x = DaoFuncionario.ler()
        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est)>0:

            x = list(map(lambda x: Funcionario(novoClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco)
            if(x.nome == nomeAlterar) else (x), x))

        else:
            print('O Funcionário que deseja alterar não existe')
        
        with open('dados/funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.clt + "|" + i.nome + "|" + i.telefone+
                               "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Funcionário alterado com sucesso')

    def removerCliente(self, nome):
        x = DaoFuncionario.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
            print('Funcionário removido com sucesso.')
        else:
            print(f"O Funcionário não pode ser removido porque não está cadastrado.")
            return None

        with open('dados/funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.clt + "|" + i.nome + "|" + i.telefone+
                               "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Funcionário removido com sucesso')
    
    def mostrarFuncionarios(self):
        funcionarios = DaoFuncionario.ler()
        if len(funcionarios) == 0:
            print('A lista de funcionários está vazia.')
        else:

            print('-------------- Funcionários --------------')
            for i in funcionarios:
                print(f'Nome {i.nome}\n'
                      f'Telefone: {i.telefone}\n'
                      f'Endereço: {i.endereco}\n'
                      f'Email {i.email}'
                      f'CPF: {i.cpf}\n'
                      f'CLT: {i.clt}')

                print()
            print('--------- Mercearia do João ---------')

    
