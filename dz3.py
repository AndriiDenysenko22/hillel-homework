#!python3
import copy


class Url(object):

    def __init__(self, scheme='', authority='', path='', query='', fragment=''):
        self.scheme = scheme
        self.authority = authority
        self.path = path
        self.query = query
        self.fragment = fragment

    def __str__(self):
        if isinstance(self.path, str):
            pass
        else:
            aa = '/'.join(map(str, self.path))
            self.path = aa
        if isinstance(self.query, str):
            pass
        else:
            qq = '&'.join(f'{key}={value}' for key, value in self.query.items())
            self.query = qq
        if self.scheme != '':
            if self.authority != '' and self.path != '' and self.query != '' and self.fragment != '':
                return str(self.scheme + '://' + self.authority + '/' + self.path + '?' + self.query + '#' +
                           self.fragment)
            elif self.authority != '' and self.path != '' and self.query != '' and self.fragment == '':
                return str(self.scheme + '://' + self.authority + '/' + self.path + '?' + self.query)
            elif self.authority != '' and self.path != '' and self.query == '' and self.fragment == '':
                return str(self.scheme + '://' + self.authority + '/' + self.path)
            elif self.path == '':
                if self.query != '':
                    if self.fragment != '':
                        return str(self.scheme + '://' + self.authority + '/' + '?' + self.query + '#' + self.fragment)
                    else:
                        return str(self.scheme + '://' + self.authority + '?' + self.query)
                elif self.query == '' and self.fragment != '':
                    return str(self.scheme + '://' + self.authority + '#' + self.fragment)
                else:
                    return str(self.scheme + '://' + self.authority)
        elif self.scheme == '':
            if self.path == '':
                if self.query != '':
                    if self.fragment != '':
                        return str(self.authority + '/' + '?' + self.query + '#' + self.fragment)
                    else:
                        return str(self.authority + '?' + self.query)
                elif self.query == '' and self.fragment != '':
                    return str(self.authority + '#' + self.fragment)
                else:
                    return str(self.authority)

            elif self.path != '' and self.query == '':
                return self.authority + '/' + self.path
            elif self.path != '' and self.query != '' and self.fragment == '':
                return (self.authority + '/' + self.path + '?' + self.query)
            elif self.path != '' and self.query != '' and self.fragment != '':
                return str(self.authority + '/' + self.path + '?' + self.query + '#' + self.fragment)

    def __eq__(self, other):
        self = str(self)
        other = str(other)
        if self == other:
            return True
        else:
            return False


class HttpsUrl(Url):

    def __init__(self, authority='', path='', query='', fragment='', scheme='https'):
        super().__init__(self, authority, path, query, fragment)
        self.scheme = scheme


class HttpUrl(Url):

    def __init__(self, authority='', path='', query='', fragment='', scheme='http'):
        super().__init__(self, authority, path, query, fragment)
        self.scheme = scheme


class GoogleUrl(Url):
    def __init__(self, path='', authority='google.com', query='', fragment='', scheme='https'):
        super().__init__(self, authority, path, query, fragment)
        self.scheme = scheme


class WikiUrl(Url):
    def __init__(self, path='', authority='wikipedia.org', query='', fragment='', scheme='https'):
        super().__init__(self, authority, path, query, fragment)
        self.scheme = scheme


assert GoogleUrl() == HttpsUrl(authority='google.com')
assert GoogleUrl() == Url(scheme='https', authority='google.com')
assert GoogleUrl() == 'https://google.com'
assert WikiUrl() == str(Url(scheme='https', authority='wikipedia.org'))
assert WikiUrl(path=['wiki', 'python']) == 'https://wikipedia.org/wiki/python'
assert GoogleUrl(query={'q': 'python', 'result': 'json'}) == 'https://google.com?q=python&result=json'





class UrlCreator(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, item):
        kwa = copy.deepcopy(self.kwargs)
        kwa['path'] = [*self.kwargs.get('path', []), item]
        return UrlCreator(**kwa)

    def _create(self):
        print(self.kwargs)
        return UrlCreator(**self.kwargs)

    def __call__(self, *args, **kwargs):
        self.kwargs['path'] = [*self.kwargs.get('path', []), *args]
        self.kwargs['query'] = {**self.kwargs.get('query', {})}
        self.kwargs['query'].update(kwargs)
        return self

    def __str__(self):
        return str(self._create().kwargs)

    def __eq__(self, other):
        elf = str(self)

        other = str(other)
        diction = {}
        protocol, smth_other = other.split('://')

        diction['scheme'] = protocol

        try:
            name, out = smth_other.split('/', 1)
        except ValueError:
            diction['authority'] = smth_other

        else:
            diction['authority'] = name

            if len(out) > 0:
                try:
                    prepath, query = out.split('?')
                except ValueError:
                    path_last = out.split('/')
                    diction['path'] = path_last

                else:

                    path = prepath.split('/')
                    diction['path'] = path

                    last = query.split('&')
                    lstd = {x.split('=')[0]: x.split('=')[1] for x in last}

                    diction['query'] = lstd
        other = str(diction)

        if elf == other:
            return True
        else:
            diction['query'] = {}
            other = str(diction)
            if elf == other:
                return True
            else:
                return False


url_creator = UrlCreator(scheme='https', authority='docs.python.org')
assert url_creator.docs.v1.api.list == 'https://docs.python.org/docs/v1/api/list'
assert url_creator('api','v1','list') == 'https://docs.python.org/api/v1/list'
assert url_creator('api','v1','list', q='my_list') == 'https://docs.python.org/api/v1/list?q=my_list'

assert url_creator('3').search(q='getattr', check_keywords='yes', area='default')._create()  \
       == 'https://docs.python.org/3/search?q=getattr&check_keywords=yes&area=default'
