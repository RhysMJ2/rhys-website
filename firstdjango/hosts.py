from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'firstdjango.boards_urls', name='www'),
    host(r'admin', settings.ROOT_URLCONF, name='admin'),
    host(r'account', 'firstdjango.accounts_urls', name='account')
    # host(r'api', 'subdomains_tutorial.api_urls', name='api'),
)
