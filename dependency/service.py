
import re
import logging
import traceback

from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from nano.rpc import Client
from os.path import join


class BaseService():

    def __init__(self) -> None:
        """
        All child classes will call contructor and initialize 
        log withe their own name
        Log will be displayed on console and written at logs/output.log
        """

        self.logger = logging.getLogger(
            f'{__name__}.{self.__class__.__name__}',
        )

class NanoService(Client , BaseService):

    # Implementation of lib client to be able to connect to nano node

    def __init__(self , url : str) -> None:
        Client.__init__(self , url)
        BaseService.__init__(self)


class GeoLocationService(BaseService):

    def __init__(self , db : str) -> None:
        self.db = join("resources" , db) # Connect to database resources
        BaseService.__init__(self)

    def get_geo_location(self, ips : dict , lst = None) -> list:

        """
        Return a list of city and their specific location according to IP address
        the ip has to be filtered because the nano node returns a list of dict along with the ports being used

        """
        lst = [] if not lst else lst
        with Reader(self.db) as reader:
            
            for filtered_ips in map( lambda i : re.findall( r'[0-9]+(?:\.[0-9]+){3}', i) , ips.keys()) :
                for ip in filtered_ips:
                    
                    try:
                        lst.append(reader.city(ip))
                    except AddressNotFoundError as r:
                        self.logger.error(r)
                        self.logger.error(str(traceback.format_exc()))

        return lst 
