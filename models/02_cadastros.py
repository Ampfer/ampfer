# -*- coding: utf-8 -*-

'''
from gluon.sql import DAL, Field

db1=DAL('firebird://sysdba:masterkey@127.0.0.1:3050//fdb/erp.fdb',
	migrate_enabled=False,
	ignore_field_case=True,
	entity_quoting=False
	)
'''
data = IS_NULL_OR(IS_DATE(format=T("%d/%m/%Y")))
TIPOCLIENTE = {'J':"Jurídica","F":"Física"}
CLIENTEFINAL = {'S':"Sim","N":"Não"}

Tipos_Clientes = db.define_table('tiposclientes',
    Field('codtip','integer',label='Código:'),
    Field('nomtip','string',label='Nome:',length=50),
    Field('clifin','string',label='Nome:',length=1),
    primarykey = ['codtip'],
    migrate = False,
    format='%(nomtip)s',
    )
Tipos_Clientes.clifin.requires = IS_IN_SET(CLIENTEFINAL,zero=None)

Vendedores = db.define_table('vendedores',
    Field('codven','integer',label='Código:'),
    Field('nomven','string',label='Vendedor:',length=50),
    primarykey = ['codven'],
    migrate = False,
    format='%(nomven)s',
    )

Clientes = db.define_table('clientes',
	Field('codcli','integer',label='Código:'),
    Field('nomcli','string',label='Nome:',length=50),
    Field('nomfan','string',label='Nome Fantasia:',length=30),
    Field('fisjur','string',label='Tipo:', length=1),
    Field('emacli','string',label='Email:', length=40),
    Field('telcli','string',label='Fone:', length=40),
    Field('celcli','string',label='Celular:', length=15),
    Field('contat','string',label='Contato:', length=35),
    Field('cgccpf','string',label='Cnpj/Cpf:', length=17),
    Field('insnrg','string',label='IE/RG:', length=17),
    Field('codtip','integer',label='Tipo Cliente:'),
    Field('endcli','string',label='Endereço:',length=50),
    Field('numcli','string',label='Número:',length=10),
    Field('baicli','string',label='Bairro:',length=35),
    Field('cidcli','string',label='Cidade:',length=35),
    Field('estcli','string',label='Estado:',length=2),
    Field('cepcli','string',label='Cep:',length=9),
    Field('endcob','string',label='Endereço:',length=50),
    Field('numcob','string',label='Número:',length=10),
    Field('baicob','string',label='Bairro:',length=35),
    Field('cidcob','string',label='Cidade:',length=35),
    Field('estcob','string',label='Estado:',length=50),
    Field('cepcob','string',label='Cep:',length=9),
    Field('endent','string',label='Endereço:',length=50),
    Field('nument','string',label='Número:',length=10),
    Field('baient','string',label='Bairro:',length=35),
    Field('cident','string',label='Cidade:',length=35),
    Field('estent','string',label='Estado:',length=50),
    Field('cepent','string',label='Cep:',length=9),
    Field('datcad','date',label='Fundação:'),
    Field('datalt','date',label='Cadastro:'),
    Field('datfun','date',label='Atualização:'),
    primarykey = ['codcli'],
    migrate = False
    )
Clientes.fisjur.requires = IS_IN_SET(TIPOCLIENTE,zero=None)
Clientes.datcad.requires = data
Clientes.datalt.requires = data
Clientes.datfun.requires = data
Clientes.codtip.requires = IS_IN_DB(db,'tiposclientes.codtip','%(nomtip)s')

Fornecedores = db.define_table('fornecedores',
    Field('codfor','integer',label='Código:'),
    Field('nomfor','string',label='Produto:',length=50),
    Field('nomfan','string',label='Fantasia:',length=50),
    Field('fisjur','string)',label='Tipo:'),
    primarykey = ['codfor'],
    migrate = False,
    format='%(nomfor)s',
    )

Grupos = db.define_table('grupos',
    Field('codgru','integer',label='Código:'),
    Field('nomgru','string',label='Produto:',length=50),
    primarykey = ['codgru'],
    migrate = False,
    format='%(nomgru)s',
    )

Produtos = db.define_table('produtos',
    Field('codpro','integer',label='Código:'),
    Field('nompro','string',label='Produto:',length=50),
    Field('modelo','string',label='Produto:',length=20),
    Field('unipro','string',label='Unidade:',length=2),
    Field('qntest','decimal(12,4)',label='Estoque:'),
    Field('precus','decimal(15,5)',label='Custo:'),
    Field('forpri','integer',label='Fornecedor:'),
    Field('codgru','integer',label='Grupo:'),
    Field('tabela','string',label='Tabela:',length=1),
    primarykey = ['codpro'],
    migrate = False,
    format='%(nompro)s',
    )
Produtos.forpri.requires = IS_IN_DB(db,'fornecedores.codfor','%(nomfor)s')
Produtos.codgru.requires = IS_IN_DB(db,'grupos.codgru','%(nomgru)s')

Local = db.define_table('local',
    Field('codloc','integer',label='Id:'),
    Field('locest','string',label='Fornecedor:',length=20),
    primarykey = ['codloc'],
    migrate = False,
    format='%(locest)s',
    )

#Clientes.codcli.writable = False

#Clientes[None] = dict(codcli=22579, nomcli= 'teste2')

