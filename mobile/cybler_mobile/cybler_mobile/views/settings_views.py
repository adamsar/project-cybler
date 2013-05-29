"""
Views for static content more or less on the settings page
"""

from pyramid.view import view_config

@view_config(route_name="info", renderer="settings/about.mako")
def info(request):
    return {}

@view_config(route_name="privacy", renderer="settings/privacy.mako")
def privacy(request):
    return {}

@view_config(route_name="tos", renderer="settings/tos.mako")
def tos(request):
    return {}    
