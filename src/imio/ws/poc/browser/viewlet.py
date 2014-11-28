# encoding: utf-8

from plone.app.layout.viewlets import common as base


class WSViewlet(base.ViewletBase):

    def can_view(self):
        return getattr(self.context, 'original_url', None) is None

    @property
    def sended(self):
        return getattr(self.context, 'external_uid', None) is not None

    @property
    def url(self):
        return self.context.absolute_url()
