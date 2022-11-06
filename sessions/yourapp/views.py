from django.views.generic import TemplateView
from datetime import datetime 

class firstView(TemplateView):
    template_name = 'yourapp/View.html'

    def get_context_data(self, **kwargs) :
        ctx = super().get_context_data(**kwargs)
        session = self.request.session.session_key
        if not session :
            self.request.session.create()
        
        if not ( self.request.session.get('firstView', None) or self.request.session.get('secondView', None)) :
            self.request.session['firstView'] = 0
            self.request.session['secondView'] = 0
        
        # add a one each time you refresh or move to this page
        self.request.session['info in session , doesn\'t matter which one'] = 'you can use it while user browser is open'
        self.request.session['firstView'] += 1

        ctx['in_view'] = {
            'firstView' : self.request.session['firstView'],
            'secondView' : self.request.session['secondView'],
        }
        return ctx

class secondView(TemplateView):
    template_name = 'yourapp/View.html'

    def get_context_data(self, **kwargs) :
        ctx = super().get_context_data(**kwargs)
        session = self.request.session.session_key
        if not session :
            self.request.session.create()
            # this proccess only is nessasary when you want to differ between users
            # it\'s only a way to know which user is , if you save 'self.request.session.session_key' in your temporary database
        
        if not ( self.request.session.get('firstView', None) or self.request.session.get('secondView', None)) :
            self.request.session['firstView'] = 0
            self.request.session['secondView'] = 0
        # add a one each time you refresh or move to this page
        
        self.request.session['info in session , doesn\'t matter which one'] = 'you can use it while user browser is open'
        self.request.session['secondView'] += 1

        ctx['in_view'] = {
            'firstView' : self.request.session['firstView'],
            'secondView' : self.request.session['secondView'],
        }

        self.request.session.modified = True # after each changes in session you need to set modify to True
        return ctx

class clearSession(TemplateView):
    template_name = 'yourapp/View.html'

    def get_context_data(self, **kwargs) :
        ctx = super().get_context_data(**kwargs)

        self.request.session['info in session , doesn\'t matter which one'] = 'you can use it while user browser is open'

        self.request.session['firstView'] = 0
        self.request.session['secondView'] = 0

        ctx['in_view'] = {
            'firstView' : self.request.session['firstView'],
            'secondView' : self.request.session['secondView'],
        }

        self.request.session.modified = True # after each changes in session you need to set modify to True
        return ctx
