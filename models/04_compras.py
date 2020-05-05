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
