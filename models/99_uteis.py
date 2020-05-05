# -*- coding: utf-8 -*-

def moeda(valor):
    from locale import setlocale, currency, LC_ALL
    try:
        setlocale(LC_ALL, 'pt_BR.UTF-8')
    except:
        setlocale(LC_ALL, 'portuguese')
    return '%s' % currency(valor, grouping=True, symbol=False)