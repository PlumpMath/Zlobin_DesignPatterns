__author__ = 'Tharun'

import abc
import urllib2
from BeautifulSoup import BeautifulStoneSoup

class Connector:
    """Abstract class to connect to a remote resource"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def parse(self):
        """Parses web content.
        This method should be redefined in the runtime"""
        pass

    def read(self, host, path):
        """A generic method for all subclasses, reads web content"""
        url = self.protocol + "://" + host + ":" + str(self.port) + path
        print "connecting to", url
        return urllib2.urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def protocol_factory_method(self):
        """
        A factory method that must be redefined in the subclass
        """
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        """
        A factory method to be redefined in the subclass
        """
        return FTPPort()


class HTTPConnector(Connector):
    """
    A concrete creator that creates a HTTP connector and sets in runtime all its attributes
    """
    def protocol_factory_method(self):
        if self.is_secure:
            return 'https'
        return 'http'

    def port_factory_method(self):
        """
        Here HTTPPort and HTTPSecurePort are concrete objects,
        created by factory method.
        """
        if self.is_secure:
            return HTTPSecurePort()
        return HTTPPort()

    def parse(self, content):
        """
        :param content: content to be parsed
        :return:
        """
        filenames = []
        soup = BeautifulStoneSoup(content)
        links = soup.table.findAll('a')
        for link in links:
            filenames.append(link['href'])
        return '\n'.join(filenames)

class FTPConnector(Connector):
    """ A concrete creator that creates a FTP connector
    """
    def protocol_factory_method(self):
        return 'ftp'

    def port_factory_method(self):
        return FTPPort()

    def parse(self, content):
        lines = content.split('\n')
        filenames = []
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)

class Port:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __str__(self):
        pass

class HTTPPort:
    def __str__(self):
        return '80'

class HTTPSecurePort:
    def __str__(self):
        return '443'

class FTPPort:
    def __str__(self):
        return '21'

if __name__ == "__main__":
    domain = "ftp.freebsd.org"
    path = "/pub/FreeBSD"

    protocol = input("Connecting to {}. Which protocol to use? (0 - http, 1 - ftp: ". format(domain))

    if protocol == 0:
        is_secure = bool(input("Use secure connection? (1 - yes, 0 - no): "))
        connector = HTTPConnector(is_secure)
    else:
        is_secure = False
        connector = FTPConnector(is_secure)

    try:
        content = connector.read(domain, path)
    except urllib2.URLError, e:
        print 'cannot access resource with this method'
    else:
        print connector.parse(content)



