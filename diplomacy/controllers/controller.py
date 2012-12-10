# -*- coding: utf-8 -*-
"""Sample controller module"""

# turbogears imports
from tg import expose
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from diplomacy.lib.base import BaseController
#from diplomacy.model import DBSession, metadata


class RootController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('diplomacy.templates.index')
    def index(self):
        return dict(page='index')
