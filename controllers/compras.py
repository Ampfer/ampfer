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
    
    extrato = ''
    titulo = 'Ficha de Estoque'

    btnPesquisar = pesquisar('compras','pesquisar_produto','Pesquisar Produto')

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
        
        extrato = LOAD('compras','extrato_estoque',args=[produto,dtinicial,dtfinal,deposito], 
            target='extrato', ajax=True,content='Aguarde, carregando...')
        
        titulo = Produtos[produto].nompro

    elif form_pesq.errors:
        response.flash = 'Erro no Formulário'

    return dict(form_pesq=form_pesq,extrato=extrato, 
                titulo=titulo,btnPesquisar=btnPesquisar)

@auth.requires_membership('admin')
def extrato_estoque():

    produto = int(request.args[0])
    dtinicial = request.args[1]
    dtfinal = request.args[2]
    deposito = None if request.args[3] == 'None' else int(request.args[3])
    resultado = filtrar_ficha_estoque(produto,dtinicial,dtfinal,deposito)
    saldo_atual = saldo_estoque(produto,request.now,deposito)

    return dict(resultado=resultado,saldo_atual=saldo_atual)

@auth.requires_membership('admin')
def filtrar_ficha_estoque(produtoId,dtinicial,dtfinal, deposito):

    query1 = (Pedidos1.numdoc == Pedidos2.numdoc) & (Pedidos2.codpro == produtoId) & (Pedidos1.datdoc >= dtinicial) & (Pedidos1.datdoc <= dtfinal) 
    query2 = (Entradas1.numdoc == Entradas2.numdoc) & (Entradas2.codpro == produtoId) & (Entradas1.datdoc >= dtinicial) & (Entradas1.datdoc <= dtfinal)
    query3 = (Devolucoes1.numdev == Devolucoes2.numdev) & (Devolucoes2.codpro == produtoId) & (Devolucoes1.datdev >= dtinicial) & (Devolucoes1.datdev <= dtfinal)
    query4 = (Mestoque.codpro == produtoId) & (Mestoque.datest >= dtinicial) & (Mestoque.datest <= dtfinal)

    if deposito:
        query1 = query1 & (Pedidos2.locest == deposito)
        query2 = query2 & (Entradas2.locest == deposito)
        query3 = query3 & (Devolucoes2.locest == deposito)
        query4 = query4 & (Mestoque.locest == deposito)
       
    pedidos = db(query1).select(orderby = Pedidos1.datdoc)
    entradas = db(query2).select(orderby = Entradas1.datdoc)
    devolucoes = db(query3).select(orderby = Devolucoes1.datdev)
    movimentos = db(query4).select(orderby = Mestoque.datest)

    extrato = []
    for entrada in entradas:
        fornecedor = Fornecedores[entrada.entradas1.codfor].nomfor
        dt = entrada.entradas1.datdoc
        dcto = entrada.entradas1.numdoc
        historico = fornecedor
        qtde = entrada.entradas2.qntent
        tipo = 'Compra'
        extrato.append(dict(data=dt,dcto=dcto,tipo=tipo, historico=historico, ent = qtde, sai = 0, saldo = 0))

    for devolucao in devolucoes:
        cliente = Clientes[devolucao.devolucoes1.codcli].nomcli
        dt = devolucao.devolucoes1.datdev
        dcto = devolucao.devolucoes1.numdev
        historico = cliente
        qtde = devolucao.devolucoes2.qntpro
        tipo = 'Devolição'
        extrato.append(dict(data=dt,dcto=dcto,tipo=tipo, historico=historico, ent = qtde, sai = 0, saldo = 0))

    for movimento in movimentos:
        dt = movimento.datest
        dcto = movimento.codide
        historico = movimento.obsest
        qtde = movimento.qntpro
        tipo = 'Manual'
        if movimento.entsai == 'S':
            extrato.append(dict(data=dt,dcto=dcto,tipo=tipo, historico=historico, ent = 0, sai = qtde, saldo = 0))
        else:
            extrato.append(dict(data=dt,dcto=dcto,tipo=tipo, historico=historico, ent = qtde, sai = 0, saldo = 0))
    
    for pedido in pedidos:
        cliente = Clientes[pedido.pedidos1.codcli].nomcli
        dt = pedido.pedidos1.datdoc
        dcto = pedido.pedidos1.numdoc
        historico = cliente
        qtde = pedido.pedidos2.qntpro
        tipo = 'Venda'
        extrato.append(dict(data=dt,dcto=dcto,tipo=tipo, historico=historico, ent = 0, sai = qtde, saldo = 0))

  
    dtAnt = datetime.strptime(dtinicial, '%Y-%m-%d').date()  - timedelta(days=1)

    anterior = saldo_estoque(produtoId,dtAnt,deposito)
    extrato.append(dict(data=dtAnt,dcto = '',tipo='', historico='Saldo Anterior', ent=0,sai=0,saldo = anterior ))
 
    extrato = sorted(extrato,  key=lambda k: k['data'])
 
    resultado = (extrato,anterior)

    return resultado

@auth.requires_membership('admin')
def saldo_estoque(produto,dt,deposito):
    q1 = (Entradas1.numdoc == Entradas2.numdoc) & (Entradas2.codpro == produto) & (Entradas1.datdoc <= dt) 
    q2 = (Pedidos1.numdoc == Pedidos2.numdoc) & (Pedidos2.codpro == produto) & (Pedidos1.datdoc <= dt) 
    q3 = (Mestoque.codpro == produto) & (Mestoque.datest <= dt) & (Mestoque.entsai == 'E')
    q4 = (Mestoque.codpro == produto) & (Mestoque.datest <= dt) & (Mestoque.entsai == 'S')
    q5 = (Devolucoes1.numdev == Devolucoes2.numdev) & (Devolucoes2.codpro == produto) & (Devolucoes1.datdev <= dt) 
    if deposito:
        q1 = q1 & (Entradas2.locest == deposito)
        q2 = q2 & (Pedidos2.locest == deposito)
        q3 = q3 & (Mestoque.locest == deposito)
        q4 = q4 & (Mestoque.locest == deposito)
        q5 = q5 & (Devolucoes2.locest == deposito)
    
    sum = Entradas2.qntent.sum()
    qtEnt = db(q1).select(sum).first()[sum] or 0
    sum =Pedidos2.qntpro.sum()
    qtPed = db(q2).select(sum).first()[sum] or 0
    sum = Mestoque.qntpro.sum()
    qtMvE = db(q3).select(sum).first()[sum] or 0
    qtMvS = db(q4).select(sum).first()[sum] or 0
    sum = Devolucoes2.qntpro.sum()
    qtDev = db(q5).select(sum).first()[sum] or 0

    sd = qtEnt-qtPed+qtMvE-qtMvS+qtDev

    return sd
    
@auth.requires_membership('admin') 
def ficha_novo():
    Mestoque.codpro.default = int(request.args[0]) 
    Mestoque.locest.default = 1
    Mestoque.datest.default = request.now
    Mestoque.obsest.default = 'Acerto'

    form = SQLFORM(Mestoque,field_id='codide', _id='formEstoque')
    
    def validar(form):
        if not form.vars.codide:
            newId = int(db.executesql("select gen_id(GEN_MESTOQUE, 1) from rdb$database;")[0][0])
            Mestoque.codide.default = newId

    if form.process(onvalidation=validar).accepted:
        response.flash = 'Salvo com Sucesso!'
        response.js = "hide_modal(%s);" %("'extrato'")

    elif form.errors:
        response.flash = 'Erro no Formulário Principal!'

    return dict(form = form)

@auth.requires_membership('admin')
def pesquisar_produto():
    produtos = db(Produtos.tabela == 'S').select(Produtos.codpro,Produtos.nompro,Produtos.modelo, orderby = Produtos.nompro).as_list()
    return dict(produtos=produtos)    

def teste():

    produtoId = int(request.args[0])
    dtinicial = request.args[1]
    dtfinal = request.args[2]
    deposito = request.args[3]

    query2 = (Entradas1.numdoc == Entradas2.numdoc) & (Entradas2.codpro == produtoId) & (Entradas1.datdoc >= dtinicial) & (Entradas1.datdoc <= dtfinal)
    entradas = db(query2).select(orderby = Entradas1.datdoc)
    query4 = (Mestoque.codpro == produtoId) & (Mestoque.datest >= dtinicial) & (Mestoque.datest <= dtfinal)
    movimentos = db(query4).select(orderby = Mestoque.datest)
    extrato = []
    for entrada in entradas:
        fornecedor = Fornecedores[entrada.entradas1.codfor].nomfor
        dt = str(entrada.entradas1.datdoc)
        dcto = entrada.entradas1.numdoc
        historico = fornecedor
        qtde = float(entrada.entradas2.qntent)
        tipo = 'Compra'
        extrato.append(dict(data=dt,dcto=dcto,tipo=tipo, historico=historico, ent = qtde, sai = 0, saldo = 0))
    for movimento in movimentos:
        dt = str(movimento.datest)
        dcto = movimento.codide
        historico = movimento.obsest
        qtde = float(movimento.qntpro)
        tipo = 'Manual'
        if movimento.entsai == 'S':
            extrato.append(dict(data=dt,dcto=dcto,tipo=tipo, historico=historico, ent = 0, sai = qtde, saldo = 0))
        else:
            extrato.append(dict(data=dt,dcto=dcto,tipo=tipo, historico=historico, ent = qtde, sai = 0, saldo = 0))
    
    
    #extrato = []
    #extrato.append(dict(dcto = '1', data = '01/05/2020',tipo='b', historico = 'xxx', ent=0,sai=1, saldo = 0))
    #extrato.append(dict(dcto = '2', data = '02/05/2020',tipo='a', historico = 'xxx', ent=1,sai=0, saldo = 0))
    import json
    extrato = json.dumps(extrato)
    
    return extrato


def vue():
    return dict()

def vue1():
    codpro = request.args[0] if request.args else None
    if codpro:
        rows = db(db.produtos.codpro==codpro).select().as_list()
    else:
        rows = db(db.produtos.codpro<100).select().as_list()
    return response.json(rows)





