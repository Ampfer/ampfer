# -*- coding: utf-8 -*-

Orcamentos1 = db.define_table('orcamentos1',
    Field('numdoc','integer',label='Número:'),
    Field('codcli','reference clientes',label='Cliente:'),
    Field('datdoc','date',label='Data:'),
    Field('codven','reference vendedores',label='Vendedor:'),
    Field('tiporc','string',label='Tipo:'),   
    primarykey = ['numdoc'],
    migrate = False,
    )

Orcamentos2 = db.define_table('orcamentos2',
    Field('numdoc','integer',label='Número:'),
    Field('codpro','reference produtos',label='Código:'),
    Field('nompro','string',label='Produto:',lenght=50),
    Field('qntpro','decimal(10,2)',label='Quantidade:'),
    Field('prepro','decimal(10,2)',label='Preço:'),  
    primarykey = ['numdoc'],
    migrate = False,
    )

Pedidos1 = db.define_table('pedidos1',
    Field('numdoc','integer',label='Número:'),
    Field('codcli','reference clientes',label='Cliente:'),
    Field('datdoc','date',label='Data:'),
    Field('codven','reference vendedores',label='Vendedor:'),  
    primarykey = ['numdoc'],
    migrate = False,
    )
    
Pedidos2 = db.define_table('pedidos2',
    Field('numdoc','integer',label='Número:'),
    Field('codpro','reference produtos',label='Código:'),
    Field('nompro','string',label='Produto:',lenght=50),
    Field('qntpro','decimal(10,2)',label='Quantidade:'),
    Field('prepro','decimal(10,2)',label='Preço:'),
    Field('locest','reference local',label='Depósito:'),  
    primarykey = ['numdoc'],
    migrate = False,
    )
