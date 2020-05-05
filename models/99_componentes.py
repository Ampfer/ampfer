def grid(query,maxtextlength=50,pag=100,alt='400px',**kwargs):
    
    grid = SQLFORM.grid(query,
                        user_signature=False,
                        showbuttontext=False,
                        csv=None,
                        maxtextlength=maxtextlength,
                        details=False,
                        paginate=pag,
                        **kwargs)
    try:
        grid.element('.web2py_grid .web2py_table .web2py_htmltable')['_style'] = 'overflow: scroll; height:%s' %(alt)
    except Exception as e:
        pass   
    
    return grid

def titulo(titulo,subTitulo,*args):
    subTitulo = '<small>%s</small>' %(subTitulo)
    btn = DIV(args,_class="btn-group btn-group-xs",_role = 'group') if args else ''
    return DIV(H3(titulo,XML(subTitulo)),btn,_class='page-header text-info') 

def subTitulo(subTitulo):
    sub = "<small class='text-muted'>%s</small>" %(subTitulo)
    return DIV(H3(XML(sub)),HR())

def btnRodape(*args):
    return DIV(HR(),DIV(args,_class="btn-group btn-group-sm",_role = 'group'))

def campo(col,label,widget):
    coluna = 'col-md-%s' %(col)
    div1 = DIV(label,widget,_class='form-group')  
    response = DIV(div1,_class=coluna)
    return response

def cancelar(url):
    return A('  Cancelar  ', _class="btn btn-secondary",_href=URL(url))

def voltar(url):
    return A(SPAN(_class="icon pen icon-pencil glyphicon glyphicon-pencil"), ' Voltar ', _class="btn btn-secondary",_href=URL(url))

def voltar1(target):
    return A(SPAN(_class="glyphicon glyphicon-arrow-left"), ' Voltar ', _class="btn btn-warning",
                 _onClick="jQuery(%s).get(0).reload()" %(target))
def voltar2():
    return A(SPAN(_class="glyphicon glyphicon-arrow-left"), ' Voltar ', _class="btn btn-warning",
                 _onClick="history.back()")
def excluir(url):
    return A(SPAN(_class="glyphicon glyphicon-trash"), ' Excluir ', _class="btn btn-danger", _href=url)
def novo(url):
    return A(SPAN(_class="glyphicon glyphicon-plus"), ' Novo ', _class="btn btn-info",_href=URL(url))
def proximo(url,id):
    return A(' Proximo ', SPAN(_class="glyphicon glyphicon-chevron-right"),  _class="btn btn-info",_href=URL(url,args=id))    
def anterior(url,id):
    return A(SPAN(_class="glyphicon glyphicon-chevron-left"), ' Anterior ', _class="btn btn-info",_href=URL(url,args=id))    
def pesquisar(controle,funcao,titulo):
    return A(SPAN(_class="btn btn-default glyphicon glyphicon-search"),'',_type="button",_id='pesquisar',
    _onclick="show_modal('%s','%s');" %(URL(controle,funcao,vars={'reload_div':'map'}),titulo))
def email(idcompra):
    return A(SPAN(_class="glyphicon glyphicon-file"),' Email',_class="btn btn-info",_id='email',
    _onclick="show_modal('%s','%s');" %(URL('pagar','enviarEmail',vars=dict(reload_div='map',id_compra=idcompra)),'Enviar Email de Pedido de Compra'))
def pdf(url,idpagar):
    return A(SPAN(_class="glyphicon glyphicon-file"), ' PDF ', _class="btn btn-info",_href=URL(url,vars=dict(id_pagar=idpagar)),_target = "_blank" )
def adicionar(controle,funcao,titulo):
    return A(SPAN(_class="glyphicon glyphicon-plus"),titulo,_class="btn btn-default",_id='adcionar',
    _onclick="show_modal('%s','%s');" %(URL(controle,funcao,vars={'reload_div':'map'}),titulo))
def atualizar(funcao,titulo,target):
    return A(SPAN(_class="glyphicon glyphicon-refresh"),titulo,_class="btn btn-default",_id='adcionar',
    _href='#', _onclick="ajax('%s',[],'%s');" % (URL(funcao, args=request.args(0)),target))
