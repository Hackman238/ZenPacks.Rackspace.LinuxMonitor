from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class CoreCountMap(SnmpPlugin):

    maptype = 'coreCount'

    cMonOperEntry = {
        '.1': 'hrProcessorFrwID',
    }

    snmpGetTableMaps = (
        GetTableMap('MonOperEntry', '.1.3.6.1.2.1.25.3.3.1', cMonOperEntry),
    )

    def process(self, device, results, log):
        """
        Collect Core count from Linux or simular device
        """
        log.info('Processing %s for device %s', self.name(), device.id)
        log.debug('Core count result: %S', results)
        getdata, tabledata = results
        coreTable = tabledata.get('MonOperEntry')

        maps = []
    
        #coreCount = 20
        coreCount = len(coreTable.values())
        if coreCount is not None:
            log.info('Found a count of %s logical CPUs!', coreCount)
            maps.append(ObjectMap({'setCoreCount': coreCount}, compname=''))

        return maps
