# -*-coding:utf-8-*-
# python3.0
import logging
import ssl
import urllib.parse as urlparse
from http.client import HTTPConnection, HTTPSConnection


class HttpClient:
    def get(self, httpUrl, headers={}):
        return self.invoke("GET", httpUrl, None, headers)

    def post(self, httpUrl, body, headers={}):
        return self.invoke("POST", httpUrl, body, headers)

    def invoke(self, method, httpUrl, body=None, headers={}):
        connect = None
        try:
            uri = urlparse.urlparse(httpUrl)
            if "https".__eq__(uri.scheme):
                context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                context.verify_flags = ssl.CERT_NONE
                connect = HTTPSConnection(uri.hostname, uri.port, context=context)
            else:
                connect = HTTPConnection(uri.hostname, uri.port)
            url = uri.path + "?" + uri.query
            connect.request(method, url=url, body=body, headers=headers)
            response = connect.getresponse()
            rHeader = {}
            for k in response.headers:
                rHeader[k.lower()] = response.headers.get(k)
            result = response.read()
            response.close()
            return True, response.status, result, rHeader
        except Exception as e:
            logging.exception("http invoke:%s", e)
            return False, 0, "", {}
        finally:
            if connect is not None:
                connect.close()
