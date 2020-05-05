# -*- coding: utf-8 -*-

from datetime import datetime

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
    
    '''
    resultado = filtrar_estoque(fornecedor,grupo,dtestoque)
    inventario = resultado[0]
    estoque = resultado[1]
    total = resultado[2]
    '''
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