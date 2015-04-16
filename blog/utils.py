from django.utils.safestring import mark_safe
from django.forms.util import ErrorList

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u''
        return mark_safe(u'<div>%s</div>' % ''.join([u'<div class="alert alert-danger">%s</div>' % e for e in self]))  # NOQA
