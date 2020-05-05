# -*- coding: utf-8 -*-

from datetime import datetime

@auth.requires_membership('admin')
def vendas_relatorio():

    tipo = request.vars.tipo if request.vars.tipo else 'Orçamentos'
    vendedor = request.vars.vendedor if request.vars.vendedor else None
    
    dtfinal = datetime.strptime(request.vars.dtfinal,'%d/%m/%Y').date() if request.vars.dtfinal else request.now
    if request.vars.dtinicial:
        dtinicial = datetime.strptime(request.vars.dtinicial,'%d/%m/%Y').date()
    else:
        today = datetime.today()
        dtinicial = datetime(today.year, today.month, 1)

    form_pesq = SQLFORM.factory(
        Field('tipo','String',requires=IS_IN_SET(['Orçamentos','Pedidos'],zero=None),label='Tipo',default = tipo),
        Field('vendedor','integer',requires=IS_EMPTY_OR(IS_IN_DB(db,'vendedores.codven','%(nomven)s',zero='Todos')),label='Vendedor',default = vendedor),
        Field('dtinicial','date',requires=data,label='Data Inicial', default = dtinicial),
        Field('dtfinal','date',requires=data,label='Data Final', default = dtfinal),
        table_name='pesquisar',
        submit_button=' Filtrar ',
        keepvalues = True,
    )

    resultado = filtrar_vendas(tipo,vendedor,dtinicial,dtfinal)
    vendas = resultado[0]
    total = resultado[1]

    if form_pesq.process().accepted:
        tipo = form_pesq.vars.tipo
        vendedor = form_pesq.vars.vendedor
        dtinicial= form_pesq.vars.dtinicial
        dtfinal = form_pesq.vars.dtfinal
        resultado = filtrar_vendas(tipo,vendedor,dtinicial,dtfinal)
        vendas = resultado[0]
        total = resultado[1]

    elif form_pesq.errors:
        response.flash = 'Erro no Formulário'

    return dict(form_pesq=form_pesq,vendas=vendas, total = total)

@auth.requires_membership('admin')
def filtrar_vendas(tipo,vendedor,dtinicial,dtfinal):
    tabela1 = "Orcamentos1" if tipo == 'Orçamentos' else "Pedidos1"
    tabela2 = "Orcamentos2" if tipo == 'Orçamentos' else "Pedidos2"
    
    query = (eval(tabela1).datdoc >= dtinicial) & (eval(tabela1).datdoc <= dtfinal)

    if vendedor:
        query = query & (eval(tabela1).codven == vendedor)

    if tipo == 'Orçamentos':
        query = query & (Orcamentos1.tiporc == 'P')

    rows = db(query).select()
    vendas = []
    total = 0
    for row in rows:
        cliente = Clientes[row.codcli].nomcli
        vendedor = Vendedores[row.codven].nomven
        valor = 0

        for item in db(eval(tabela2).numdoc == row.numdoc).select():
            valor = valor + round(item.qntpro * item.prepro, 2)

        total = total + valor

        vendas.append(dict(dcto = row.numdoc, data=row.datdoc, cliente = cliente,vendedor = vendedor, valor = valor, total=total))
    
    resultado = (vendas,moeda(total))

    return resultado