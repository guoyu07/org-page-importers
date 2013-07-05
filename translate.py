# -*- encoding: utf-8 -*-

import urllib, urllib2
from sgmllib import SGMLParser

class Parser(SGMLParser):
    def __init__(self, result):
        SGMLParser.__init__(self)
        self.result = result
        self.open = False

    def start_span(self, attrs):
        id = [v for k, v in attrs if k=='id']

        if 'result_box' in id:
            self.open = True

    def handle_data(self, text):
        if self.open:
            self.result += text
            self.open = False

def translate(lang_in, lang_out, text):
    if isinstance(text, unicode):
	text = text.encode("utf-8")
    values = {'hl':'zh-CN','ie':'UTF-8','text':text,'langpair':"%s|%s" % (lang_in, lang_out)}
    url    = 'http://translate.google.cn/translate_t'
    data   = urllib.urlencode(values)

    req = urllib2.Request(url, data)
    req.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)")

    response = urllib2.urlopen(req)
    
    parser = Parser("")
    data   = response.read()

    parser.feed(data)

    result = parser.result.lower().replace(' ', '-').replace('/', '-').replace('-----', '-').replace('----','-').replace('---', '-')

    response.close()

    return result

if __name__ == "__main__":
    print translate("zh_CN", "en_US", "我们的祖国")
