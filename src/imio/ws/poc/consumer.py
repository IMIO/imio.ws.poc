# encoding: utf-8

from collective.zamqp.interfaces import IMessageArrivedEvent
from five import grok
from imio.dataexchange.core import Response
from imio.wsresponse.core import Request
from imio.wsresponse.core import ResponsePublisher
from imio.wsresponse.core import IResponse
from plone import api
from zope.component.hooks import getSite

import cPickle


class ResponseConsumer(Request):
    grok.name('ws.request.test')
    queuename = 'Plone.create.{0}'


@grok.subscribe(IResponse, IMessageArrivedEvent)
def consume_requests(message, event):
    content = cPickle.loads(message.body)
    portal = getSite()
    publisher = ResponsePublisher()
    uid = content.parameters.get('external_uid')
    obj = uid and api.content.get(UID=uid) or None
    if obj is not None:
        obj.setTitle(content.parameters.get('title'))
        for key, value in content.parameters.get('values').items():
            me = getattr(obj, 'set%s' % key.capitalize(), None)
            if me:
                me(value)
    else:
        obj = api.content.create(
            container=portal,
            type=content.parameters.get('type'),
            title=content.parameters.get('title'),
            **content.parameters.get('values')
        )
    publisher.setup_queue(content.uid, content.uid)
    response = Response(
        content.uid,
        external_uid=obj.UID(),
        url=obj.absolute_url(),
    )
    publisher.add_message(response)
    publisher.start()

    message.ack()
