# -*- coding: utf-8 -*-

from datetime import datetime,timedelta

@auth.requires_membership('admin')
def estoque_relatorio():

    fornecedor = request.vars.fornecedor if request.vars.fornecedor else None
    grupo = request.vars.grupo if request.vars.grupo else 1
    dtestoque = datetime.strptime(request.vars.dtestoque,'%d/%m/%Y').date() if request.vars.dtestoque else request.now

    form_pesq = SQLFORM.factory(
        Field('fornecedor','integer',requires=IS_EMPTY_OR(IS_IN_DB(db,'fornecedores.codfor','%(nomfor)s',zero='Todos')),label='Fornecedor',default = fornecedor),
        Field('grupo','integer',requires=IS_EMPTY_OR(IS_IN_DB(db,'grupos.codgru','%(nomgru)s',zero='Todos')),label='Grupo',default = grupo),
        Field('dtestoque','date',requires=data,label='Data:', default = dtestoque),
        table_name='pesquisar',
        submit_button=' Filtrar ',
        keepvalues = True,
    )
    
    inventario = []
    estoque = total = 0

    if form_pesq.process().accepted:
        fornecedor = form_pesq.vars.fornecedor
        grupo = form_pesq.vars.grupo
        dtestoque = form_pesq.vars.dtestoque

        resultado = filtrar_estoque(fornecedor,grupo,dtestoque)
        inventario = resultado[0]
        estoque = resultado[1]
        total = resultado[2]

    elif form_pesq.errors:
        response.flash = 'Erro no Formulário'

    return dict(form_pesq=form_pesq,inventario=inventario, estoque = estoque, total=total)

@auth.requires_membership('admin')
def filtrar_estoque(fornecedor,grupo,dtestoque):

    query = (Produtos.tabela == 'S')
    if fornecedor:
        query = query & (Produtos.forpri == fornecedor)
    if grupo:
        query = query & (Produtos.codgru == grupo)

    rows = db(query).select(orderby = Produtos.nompro)
    inventario = []
    total = 0
    estoque = 0
    for row in rows:
        q = (Cuspro.codpro == row.codpro) & (Cuspro.codfor == row.forpri)
        precus = db(q).select().first()['precus'] or 0
        grupo = Grupos[row.codgru].nomgru
        fornecedor = Fornecedores[row.forpri].nomfan
    
        if row.qntest > 0:
            estoque = estoque + row.qntest
            valor = round(row.qntest * precus, 2)
            total = total + valor
        else:
            valor = 0

        inventario.append(dict(codigo = row.codpro, produto=row.nompro, fornecedor = fornecedor,grupo = grupo, estoque= row.qntest,total=valor))
    
    resultado = (inventario,estoque,moeda(total))

    return resultado

@auth.requires_membership('admin')
def ficha_estoque():

    produto = request.vars.produto if request.vars.produto else None
    dtfinal = datetime.strptime(request.vars.dtfinal,'%d/%m/%Y').date() if request.vars.dtfinal else request.now
    if request.vars.dtinicial:
        dtinicial = datetime.strptime(request.vars.dtinicial,'%d/%m/%Y').date()
    else:
        today = datetime.today()
        dtinicial = datetime(today.year, today.month, 1)
    deposito = request.vars.deposito if request.vars.deposito else None
    
    extrato = []
    saldo = 0

    form_pesq = SQLFORM.factory(
        Field('produto','integer',requires=IS_EMPTY_OR(IS_IN_DB(db,'produtos.codpro','%(nompro)s',zero=None)),label='Produto',default = produto),
        Field('dtinicial','date',requires=data,label='Data Inicial:', default = dtinicial),
        Field('dtfinal','date',requires=data,label='Data Final:', default = dtfinal),
        Field('deposito','integer',requires=IS_EMPTY_OR(IS_IN_DB(db,'local.codloc','%(locest)s',zero='Todos')),label='Depósito',default = deposito),
        table_name='pesquisar',
        submit_button=' Filtrar ',
        keepvalues = True,
    )

    if form_pesq.process().accepted:
        produto = form_pesq.vars.produto
        dtinicial= form_pesq.vars.dtinicial
        dtfinal = form_pesq.vars.dtfinal
        deposito = form_pesq.vars.deposito

        resultado = filtrar_ficha_estoque(produto,dtinicial,dtfinal)
        extrato = resultado[0]
        saldo = resultado[1]

    elif form_pesq.errors:
        response.flash = 'Erro no Formulário'

    return dict(form_pesq=form_pesq,extrato=extrato, saldo = saldo)

@auth.requires_membership('admin')
def filtrar_ficha_estoque(produtoId,dtinicial,dtfinal):

    produto = Produtos[produtoId]

    query = (Pedidos1.numdoc == Pedidos2.numdoc) & (Pedidos2.codpro == produtoId) & (Pedidos1.datdoc >= dtinicial) & (Pedidos1.datdoc <= dtfinal)
    pedidos = db(query).select(orderby = Pedidos1.datdoc)
    query = (Entradas1.numdoc == Entradas2.numdoc) & (Entradas2.codpro == produtoId) & (Entradas1.datdoc >= dtinicial) & (Entradas1.datdoc <= dtfinal)
    entradas = db(query).select(orderby = Entradas1.datdoc)
    query = (Devolucoes1.numdev == Devolucoes2.numdev) & (Devolucoes2.codpro == produtoId) & (Devolucoes1.datdev >= dtinicial) & (Devolucoes1.datdev <= dtfinal)
    devolucoes = db(query).select(orderby = Devolucoes1.datdev)
    query = (Mestoque.codpro == produtoId) & (Mestoque.datest >= dtinicial) & (Mestoque.datest <= dtfinal)
    movimentos = db(query).select(orderby = Mestoque.datest)

    extrato = []
    for entrada in entradas:
        fornecedor = Fornecedores[entrada.entradas1.codfor].nomfor
        dt = entrada.entradas1.datdoc
        dcto = entrada.entradas1.numdoc
        historico = fornecedor
        qtde = entrada.entradas2.qntent
        extrato.append(dict(data=dt,dcto=dcto, historico=historico, ent = qtde, sai = 0, saldo = 0))

    for devolucao in devolucoes:
        cliente = Clientes[devolucao.devolucoes1.codcli].nomcli
        dt = devolucao.devolucoes1.datdev
        dcto = devolucao.devolucoes1.numdev
        historico = cliente
        qtde = devolucao.devolucoes2.qntpro
        extrato.append(dict(data=dt,dcto=dcto, historico=historico, ent = qtde, sai = 0, saldo = 0))

    for movimento in movimentos:
        dt = movimento.movimentos1.datest
        dcto = movimento.movimentos1.codide
        historico = movimento.movimentos1.obsest
        qtde = movimento.movimentos2.qntpro
        if movimento.movimentos1.entsai == 'S':
            extrato.append(dict(data=dt,dcto=dcto, historico=historico, ent = 0, sai = qtde, saldo = 0))
        else:
            extrato.append(dict(data=dt,dcto=dcto, historico=historico, ent = qtde, sai = 0, saldo = 0))
    
    for pedido in pedidos:
        cliente = Clientes[pedido.pedidos1.codcli].nomcli
        dt = pedido.pedidos1.datdoc
        dcto = pedido.pedidos1.numdoc
        historico = cliente
        qtde = pedido.pedidos2.qntpro
        extrato.append(dict(data=dt,dcto=dcto, historico=historico, ent = 0, sai = qtde, saldo = 0))


    dt = dtinicial - timedelta(1)
    saldo = produto.qntest 
    extrato.append(dict(data=dt,dcto = '0',historico='Saldo Anterior', ent=0,sai=0,saldo = saldo ))
    
    extrato = sorted(extrato,  key=lambda k: k['data'])

    resultado = (extrato,saldo)


    return resultado