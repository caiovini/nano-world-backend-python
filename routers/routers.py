import traceback

from fastapi import APIRouter , HTTPException , Path
from dependency.service import BaseService
from dependency import service



class NanoNode(APIRouter):

    def __init__(self ,  nano_service : service.NanoService , geo_service : service.GeoLocationService) -> None:
        APIRouter.__init__(self )
        self.set_up_endpoints()
        self.nano_service = nano_service
        self.geo_service  = geo_service

    def set_up_endpoints(self) -> None:

        @self.get("/getBalance/{address}") 
        def get_balance(address : str = Path(... , title = "Nano wallet" , description = " Address of the user's wallet")) -> dict:

            self.nano_service.logger.info(f"Request to {get_balance.__name__}")
            try:
                return self.nano_service.account_balance(address)

            except Exception as e:
                save_log_error(self.nano_service , e , traceback.format_exc)
                raise HTTPException( status_code = 400 , detail = repr(e))



        @self.get("/getPeers") 
        def get_peers() -> dict:

            self.nano_service.logger.info(f"Request to {get_peers.__name__}")
            try:
                return self.nano_service.peers()

            except Exception as e:
                save_log_error(self.nano_service , e , traceback.format_exc)
                raise HTTPException( status_code = 400 , detail = repr(e))



        @self.get("/getGeoLocations") 
        def get_geo_location() -> dict:

            self.geo_service.logger.info(f"Request to {get_geo_location.__name__}")
            try:
                ips = self.nano_service.peers()                
                return { "cityResponse" : self.geo_service.get_geo_location(ips) }

            except Exception as e:
                save_log_error(self.geo_service , e , traceback.format_exc)
                raise HTTPException( status_code = 400 , detail = repr(e))


             
        def save_log_error(serv: BaseService , e : Exception , trace : traceback.format_exc) -> None:
            serv.logger.error(e)
            serv.logger.error(trace())