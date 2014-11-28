# encoding: utf-8

from Products.Five.browser import BrowserView
from imio.wsrequest.core import Request
from imio.wsrequest.core import Response
from imio.wsrequest.core import RequestException
import json


class WSRequestView(BrowserView):

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps({
            'success': self.success,
            'error': self.error,
            'id': self.id,
        })

    @property
    def content_dict(self):
        return {
            'type': self.context.portal_type,
            'title': self.context.Title(),
            'values': {
                'description': self.context.Description(),
                'text': self.context.getText(),
            },
        }

    def __call__(self):
        request = Request('plone2', 'Plone', 'create', **self.content_dict)
        request.webservice = 'test_request'
        request.version = 0.1

        self.success = False
        self.id = None
        self.error = None
        try:
            self.success, self.id = request.do_request()
        except RequestException, e:
            self.error = e.message
        return self.render()


class WSResponseView(BrowserView):

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps({
            'success': self.success,
            'error': self.error,
            'url': self.url,
        })

    def __call__(self):
        request = Response(self.request.get('id'))
        request.webservice = 'test_response'
        request.version = 0.1

        self.success = False
        self.error = None
        self.url = None
        try:
            self.success, response = request.do_request()
            self.url = response.get('url', None)
        except RequestException, e:
            self.error = e.message
        return self.render()
