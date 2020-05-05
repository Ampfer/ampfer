# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Cadastros'), False, '#', [
            (T('Clientes'), False, URL('cadastros', 'clientes')),
        ]),
        (T('Compras'), False, '#', [
            (T('Relatório de Estoque'), False, URL('compras', 'estoque_relatorio')),
        ]),
        (T('Vendas'), False, '#', [
            (T('Relatório de Vendas'), False, URL('vendas', 'vendas_relatorio')),
        ]),
        (T('Financeiro'), False, '#', [
            (T('Design'), False, URL('admin', 'default', 'design/%s' % _app)),
        ]),
    ]

