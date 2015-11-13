import os
from libmproxy.models import decoded
from libmproxy import filt
from proxyswitch import enable, disable
from proxyswitch.driver import driver, register
import proxyswitch.rules as rules

def response(context, flow):
    if driver.name != 'nobody':
        ruleset = rules.load(driver.name,
                             context.source_dir)

        urls = rules.urls(ruleset)

        if flow.request.url in urls:
            rule = rules.find_by_url(flow.request.url,
                                     ruleset)

            body = rules.body(rule,
                              context.source_dir)

            rules.process_request_headers(rule, flow.request.headers)
            rules.process_response_headers(rule, flow.response.headers)

            with decoded(flow.response):
                flow.response.content = body


def start(context, argv):
    register(context)
    enable('127.0.0.1', '8080')

    context.source_dir = argv[1]

    # context.filter = filt.parse("~d github.com")
    context.log('Source dir: {}'.format(context.source_dir))

def done(context):
    disable()
