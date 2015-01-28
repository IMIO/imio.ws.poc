# encoding: utf-8

from imio.wsrequest.core import WSRequestBaseView
from imio.wsrequest.core import WSResponseBaseView


class WSRequestView(WSRequestBaseView):

    # XXX To be moved in a configuration view
    plone_id = 'plone2'
    application_id = 'Plone'
    request_type = 'create'

    render_extra_values = {
        'id': None,
    }

    @property
    def request_kwargs(self):
        return {
            'type': self.context.portal_type,
            'title': self.context.Title(),
            'external_uid': self.context.external_uid,
            'original_url': self.context.absolute_url(),
            'values': {
                'description': self.context.Description(),
                'text': self.context.getText(),
            },
        }


class WSResponseView(WSResponseBaseView):

    render_extra_values = {
        'url': None,
    }
