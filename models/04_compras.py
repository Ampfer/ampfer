# -*- coding: utf-8 -*-

Cuspro = db.define_table('cuspro',
    Field('codpro','reference produtos',label='Produto:'),
    Field('codfor','reference fornecedores',label='Fornecedor:'),
    Field('pordes','decimal(6,2)',label='Desconto:'),
    Field('prebru','decimal(10,2)',label='Preço Bruto:'),
    Field('precus','decimal(10,2)',label='Custo:'),  
    primarykey = ['codpro','codfor'],
    migrate = False,
    )

Entradas1 = db.define_table('entradas1',
    Field('numdoc','integer',label='Documento:'),
    Field('tipdoc','string',label='Tipo:', length=1),
    Field('codfor','reference fornecedores',label='Fornecedor:'),
    Field('datdoc','date',label='Data:'),
    Field('datemi','date',label='Data:'),
    primarykey = ['numdoc'],
    migrate = False,
    )

Entradas2 = db.define_table('entradas2',
    Field('numide','integer',label='Id:'),
    Field('numdoc','reference entradas1',label='Documento:'),
    Field('codpro','referente produtos',label='Produtos:'),
    Field('qntent','decimal(12,4)',label='Quantidade:'), 
    Field('precus','decimal(15,5)',label='Custo:'),   
    primarykey = ['numide'],
    migrate = False,
)

Devolucoes1 = db.define_table('devolucoes1',
    Field('numdev','integer',label='Número:'),
    Field('datdev','date',label='Data:'), 
    Field('codcli','reference clientes',label='Cliente:'),
    primarykey = ['numdev'],
    migrate = False,
)

Devolucoes2 = db.define_table('devolucoes2',
    Field('numdev','integer',label='Número:'),
    Field('codpro','referente produtos',label='Produtos:'), 
    Field('qntpro','decimal(12,4)',label='Quantidade:'), 
    primarykey = ['numdev'],
    migrate = False,
)

Mestoque = db.define_table('mestoque',
    Field('codide','integer',label='Id:'),
    Field('datest','date',label='Data:'), 
    Field('codpro','referente produtos',label='Produtos:'), 
    Field('qntpro','decimal(12,4)',label='Quantidade:'), 
    Field('entsai','string',label='Tipo:', length=1),
    Field('obsest','string',label='Obs:', length=30),
    primarykey = ['codide'],
    migrate = False,
)