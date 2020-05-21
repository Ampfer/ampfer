# -*- coding: utf-8 -*-

from restapi import RestAPI, Policy

policy = Policy()
#policy.set('superhero', 'GET', authorize=True, allowed_patterns=['*'])
policy.set('*', 'GET', authorize=True, allowed_patterns=['*'])
policy.set('*', 'PUT', authorize=True)
policy.set('*', 'POST', authorize=True)
policy.set('*', 'DELETE', authorize=True)

def api():
    return RestAPI(db, policy)(request.method, request.args(0), request.args(1),
                            request.get_vars, request.post_vars)