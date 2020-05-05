# -*- coding: utf-8 -*-
@auth.requires_membership('admin')
def clientes():
	fields = [Clientes.codcli, Clientes.nomcli, Clientes.cidcli]
	gridClientes = grid(Clientes,alt='350px', orderby=Clientes.nomcli, fields=fields)
	btnNovo = novo('cliente')

	if request.args(-2) == 'new':
		redirect(URL('cliente'))
	elif request.args(-3) == 'edit':
		idCliente = request.args(-1)
		redirect(URL('cliente', args=idCliente ))

	return dict(gridClientes=gridClientes, btnNovo=btnNovo)

@auth.requires_membership('admin')
def cliente():

	idCliente = request.args(0) or "0"
	Clientes.codcli.default = int(db.executesql("select gen_id(GEN_CLIENTES, 1) from rdb$database;")[0][0])

	if idCliente == "0":
		formCliente = SQLFORM(db.clientes,field_id='id', _id='formCliente')

	else:
		formClienteCompras = " "
		formCliente = SQLFORM(db.clientes,idCliente,_id='formCliente',field_id='id')

	btnCancelar = cancelar("clientes")
	
	def validar(form):
		newId = int(db.executesql("select gen_id(GEN_CLIENTES, 1) from rdb$database;")[0][0])
		#form.vars.codcli = newId
		

	if formCliente.process(onvalidation = validar).accepted:
		session.flash = 'Cliente Salvo com Sucesso!'
		redirect(URL('clientes'))

	elif formCliente.errors:
		print formCliente.errors
		response.flash = 'Erro no Formulário Principal!'

	return dict(formCliente=formCliente, btnCancelar=btnCancelar)

