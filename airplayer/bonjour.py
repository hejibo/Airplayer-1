import select
import pybonjour
import logging

logger = logging.getLogger('airplayer')

def register_service(name, regtype, port):
    def register_callback(sdRef, flags, errorCode, name, regtype, domain):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            logger.info('Registered bonjour service %s', name)

    record = pybonjour.TXTRecord({
        'deviceid' : 'FF:FF:FF:FF:FF:FF',
        'features' : '0x7',
        'model' : 'AppleTV2,1',
    })
    
    service = pybonjour.DNSServiceRegister(name = name,
                                         regtype = regtype,
                                         port = port,
                                         txtRecord = record,
                                         callBack = register_callback)

    try:
        try:
            while True:
                ready = select.select([service], [], [])
                if service in ready[0]:
                    pybonjour.DNSServiceProcessResult(service)
        except KeyboardInterrupt:
            pass
    finally:
        service.close()