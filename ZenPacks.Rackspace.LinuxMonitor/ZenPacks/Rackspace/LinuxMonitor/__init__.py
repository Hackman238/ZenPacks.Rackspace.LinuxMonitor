import Globals
import logging
import os
log = logging.getLogger('zen.ZenPack.Rackspace.LinuxMonitor')

import ZenPacks.Rackspace.LinuxMonitor
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenUtils.Utils import zenPath
from Products.ZenModel.ZenMenu import ZenMenu
from Products.Zuul.interfaces import ICatalogTool

from Products.ZenModel.ZenossSecurity import *
from Products.ZenUtils.Utils import monkeypatch

# Declare skins location
skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

# Declare relationship



# Register python class




class ZenPack(ZenPackBase):
    """ Rackspace LinuxMonitor Loader
    """

    packZProperties = [('zCoreCount', 1.0, 'float'),('zThreadsPerCore', 2.0, 'float'),('zFreeMemoryThresholdPercentLimit', 0.15, 'float'),]

    def install(self, app):
        # Link daemon and hub service
        self.symlinkPlugin()

        # Install menus
        self.installMenuItems(app.zport.dmd, menuName=None)

        # Install report organizers
        self.createReportOrg(app.zport.dmd, parent=None, organizer=None)

        # Create event organizer, if not existant
        self.createEventOrg(app.zport.dmd, organizer=None)

        # Create device class, if not existant
        self.createDeviceOrg(app.zport.dmd, organizer=None)

        # Add modeler to organizer, if not existant
        self.addModeler(app.zport.dmd, organizer=None, modelerNames=[])

        # Rebuild relations
        self.rebuildRelations(app.zport.dmd, dontReBuild=1)

        # Start daemon
        self.startDaemon(app.zport.dmd, daemonName=None)

        # Recatalog
        self.recatalog(app.zport.dmd, dontReIndex=1)

        # Do it
        super(ZenPack, self).install(app)


    def remove(self, app, leaveObjects=True):
        # Do it
        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

        # Stop daemon
        self.stopDaemon(app.zport.dmd, daemonName=None)

        # Remove menus
        self.removeMenuItems(app.zport.dmd, menuName=None)

        if not leaveObjects:
            # Remove components based on classes extended by this package
            self.removeParts(app.zport.dmd, componentTypes=None, componentNames=[])

            # Remove report organizers
            self.delReportOrg(app.zport.dmd, parent=None, organizer=None)

            # Remove modeler from organizer
            self.removeModeler(app.zport.dmd, organizer=None, modelerNames=[])

            # Remove organizer
            self.delDeviceOrg(app.zport.dmd, organizer=None)

            # Remove event organizer
            self.delEventOrg(app.zport.dmd, organizer=None)

            # Rebuild relations
            self.rebuildRelations(app.zport.dmd, dontReBuild=1)

            # Recatalog
            self.recatalog(app.zport.dmd, dontReIndex=1)

        # Unlink daemon and service
        self.removePluginSymlink()


    def upgrade(self, app):
        # Stop daemon
        self.stopDaemon(app.zport.dmd, daemonName=None)

        # Remove menus
        self.removeMenuItems(app.zport.dmd, menuName=None)

        # Remove report organizers
        self.delReportOrg(app.zport.dmd, parent=None, organizer=None)

        # Unlink daemon and service
        self.removePluginSymlink()

        # Remove modeler from organizer
        self.removeModeler(app.zport.dmd, organizer=None, modelerNames=[])

        # Relink daemon and service
        self.symlinkPlugin()

        # Install menus
        self.installMenuItems(app.zport.dmd, menuName=None)

        # Install report organizers
        self.createReportOrg(app.zport.dmd, parent=None, organizer=None)

        # Create event organizer, if not existant
        self.createEventOrg(app.zport.dmd, organizer=None)

        # Create device class, if not existant
        self.createDeviceOrg(app.zport.dmd, organizer=None)

        # Add modeler to organizer
        self.addModeler(app.zport.dmd, organizer=None, modelerNames=[])

        # Rebuild relations
        self.rebuildRelations(app.zport.dmd, dontReBuild=1)

        # Start daemon
        self.startDaemon(app.zport.dmd, daemonName=None)

        # Recatalog
        self.recatalog(app.zport.dmd, dontReIndex=1)

        # Do it
        super(ZenPack, self).upgrade(app)

    ### Frame ###
    def stopDaemon(self, dmd, daemonName=None):
        if daemonName:
            try:
                # Log it
                log.info('DAEMON: Stopping %s daemon', str(daemonName))
                # Just in case it's not executable for some reason
                os.system('chmod a+x %s' % (zenPath('bin', str(daemonName))))
                # Stop daemon
                os.system('$ZENHOME/bin/%s stop', str(daemonName))
            except Exception:
                log.info('DAEMON: Some unknown exception occurred during daemon stop')
                pass
        else:
            # Log it
            log.info('DAEMON: No daemon to stop')


    def startDaemon(self, dmd, daemonName=None):
        if daemonName:
            try:
                # Log it
                log.info('DAEMON: Starting %s daemon', str(daemonName))
                # Just in case it's not executable for some reason
                os.system('chmod a+x %s' % (zenPath('bin', str(daemonName))))
                # Stop daemon
                os.system('$ZENHOME/bin/%s start', str(daemonName))
            except Exception:
                log.info('DAEMON: Some unknown exception occurred during daemon start')
                pass
        else:
            # Log it
            log.info('DAEMON: No daemon to start')


    def createDeviceOrg(self, dmd, organizer=None):
        if organizer:
            try:
                deviceOrg = dmd.Devices
                if not hasattr(deviceOrg, str(organizer)):
                    dmd.Devices.createOrganizer(str(organizer))
                    log.info('DEVICE CLASS: Adding device class %s', str(organizer))
                    from transaction import commit
                    dmd.commit()
                else:
                    log.warn('DEVICE CLASS: Device class %s already exists', str(organizer))
            except KeyError:
                log.warn('DEVICE CLASS: Device class %s already exists', str(organizer))
                pass
            except Exception:
                log.error('DEVICE CLASS: Some unknown problem occured adding device class %s', str(organizer))
                pass
        else:
            log.info('DEVICE CLASS: No device classes to add')


    def createEventOrg(self, dmd, organizer=None):
        if organizer:
            try:
                eventOrg = dmd.Events
                if not hasattr(eventOrg, str(organizer)):
                    dmd.Events.createOrganizer(str(organizer))
                    log.info('EVENT CLASS: Adding event class %s', str(organizer))
                    from transaction import commit
                    dmd.commit()
                else:
                    log.warn('EVENT CLASS: Event class %s already exists', str(organizer))
            except KeyError:
                log.warn('EVENT CLASS: Event class %s already exists', str(organizer))
                pass
            except Exception:
                log.error('EVENT CLASS: Some unknown problem occured adding event class %s', str(organizer))
                pass
        else:
            log.info('EVENT CLASS: No event classes to add')


    def createReportOrg(self, dmd, parent=None, organizer=None):
        if organizer and parent:
            try:
                reportOrg = dmd.Reports[str(parent)]
                rClass = reportOrg.getReportClass()
                if not hasattr(reportOrg, str(organizer)):
                    dc = rClass(str(organizer), None)
                    reportOrg._setObject(str(organizer), dc)
                    log.info('REPORT CLASS: Adding report class %s', str(organizer))
                    from transaction import commit
                    dmd.commit()
                else:
                    log.warn('REPORT CLASS: Report class %s already exists', str(organizer))
            except KeyError:
                log.warn('REPORT CLASS: Report class %s already exists', str(organizer))
                pass
            except Exception:
                log.error('REPORT CLASS: Some unknown problem occured  adding report class %s', str(organizer))
                pass
        else:
            log.info('REPORT CLASS: No report classes to add')


    def delDeviceOrg(self, dmd, organizer=None):
        if organizer:
            try:
                log.info('DEVICE CLASS: Removing device class %s', str(organizer))
                deviceOrg = dmd.Devices
                if hasattr(deviceOrg, str(organizer)):
                    deviceOrg._delObject(str(organizer))
                    from transaction import commit
                    dmd.commit()
                else:
                    log.warn('DEVICE CLASS: Device class %s doesnt exist, so it cannot be deleted', str(organizer))
            except KeyError:
                log.warn('DEVICE CLASS: Device class %s doesnt exist, so it cannot be deleted', str(organizer))
                pass
            except Exception:
                log.error('DEVICE CLASS: Some unknown problem occured deleting device class %s', str(organizer))
                pass
        else:
            log.info('DEVICE CLASS: No device classes to remove')


    def delEventOrg(self, dmd, organizer=None):
        if organizer:
            try:
                log.info('EVENT CLASS: Removing event class %s', str(organizer))
                eventOrg = dmd.Events
                if hasattr(eventOrg, str(organizer)):
                    eventOrg._delObject(str(organizer))
                    from transaction import commit
                    dmd.commit()
                else:
                    log.warn('EVENT CLASS: Event class %s doesnt exist, so it cannot be deleted', str(organizer))
            except KeyError:
                log.warn('EVENT CLASS: Event class %s doesnt exist, so it cannot be deleted', str(organizer))
                pass
            except Exception:
                log.error('EVENT CLASS: Some unknown problem occured deleting event class %s', str(organizer))
                pass
        else:
            log.info('EVENT CLASS: No event classes to remove')


    def delReportOrg(self, dmd, parent=None, organizer=None):
        if organizer and parent:
            try:
                log.info('REPORT CLASS: Removing report class %s', str(organizer))
                if hasattr(dmd.Reports, str(parent)):
                    parentOrg = dmd.Reports[str(parent)]
                    if hasattr(parentOrg, str(organizer)):
                        parentOrg._delObject(str(organizer))
                        from transaction import commit
                        dmd.commit()
                    else:
                        log.warn('REPORT CLASS: Report class %s doesnt exist, so it cannot be deleted', str(organizer))
            except KeyError:
                log.warn('REPORT CLASS: Report class %s doesnt exist, so it cannot be deleted', str(organizer))
                pass
            except Exception:
                log.error('REPORT CLASS: Some unknown problem occured deleting report class %s', str(organizer))
                pass
        else:
            log.info('REPORT CLASS: No report classes to remove')


    def removeParts(self, dmd, componentTypes='os', componentNames=[]):
        if len(componentNames) > 0:
            log.info('COMPONENTS: Removing pack supplied components [This could take a long time]')
            from transaction import commit
            for componentName in componentNames:
                log.info('COMPONENTS: Removing %s component relations', str(componentName))
                try:
                    if componentTypes == 'os':
                        for deviceOb in dmd.Devices.getSubDevices():
                            try:
                                for iOb in deviceOb.os._getOb(str(componentName))():
                                    iObParent = iOb.getPrimaryParent()
                                    iObParent.removeRelation(iOb)
                                dmd.commit()
                            except KeyError:
                                # Device doesn't have the relationship
                                pass
                            except Exception:
                                log.error('COMPONENTS: Some unknown problem occured removing objects from relations in device %s', str(deviceOb.id))
                                pass
                        OperatingSystem._relations = tuple([x for x in OperatingSystem._relations if x[0] not in [str(componentName)]])
                    if componentTypes == 'hw':
                        for deviceOb in dmd.Devices.getSubDevices():
                            try:
                                for iOb in deviceOb.hw._getOb(str(componentName))():
                                    iObParent = iOb.getPrimaryParent()
                                    iObParent.removeRelation(iOb)
                                dmd.commit()
                            except KeyError:
                                # Device doesn't have the relationship
                                pass
                            except Exception:
                                log.error('COMPONENTS: Some unknown problem occured removing objects from relations in device %s', str(deviceOb.id))
                                pass
                        DeviceHW._relations = tuple([x for x in DeviceHW._relations if x[0] not in [str(componentName)]])
                except Exception:
                    log.error('COMPONENTS: An unknown error occured removing the relationship %s', str(componentName))
                    pass
        else:
            log.info('COMPONENTS: No pack related components to remove.')


    def rebuildRelations(self, dmd, dontReBuild=1):
        log.info('RELATIONS: Building device relations [This could take a very long time]')
        # Build relations on all devices
        if dontReBuild != 1:
            try:
                for d in dmd.Devices.getSubDevicesGen():
                    d.buildRelations()
                    d.os.buildRelations()
                    d.hw.buildRelations()
            except Exception:
                log.error('RELATIONS: Some unknown problem occured during relationship construction')
                pass
        else:
           log.info('RELATIONS: Skipping relationship rebuild')


    def addModeler(self, dmd, organizer=None, modelerNames=[]):
        if organizer and len(modelerNames) > 0:
            try:
                plugins = []
                operationOrg = dmd.Devices.getOrganizer(str(organizer))
                for plugin in operationOrg.zCollectorPlugins:
                    plugins.append(plugin)
                for modelerName in modelerNames:
                    if modelerName not in plugins:
                        plugins.append(str(modelerName))
                        log.info('MODELERS: Adding modeler %s', str(modelerName))
                operationOrg.setZenProperty('zCollectorPlugins', plugins)
            except KeyError:
                log.warn('MODELERS: Problem adding modeler since specified organizer does  exist')
                pass
            except Exception:
                log.error('MODELERS: Some unknown problem occured adding modelers')
                pass


    def removeModeler(self, dmd, organizer=None, modelerNames=[]):
        if organizer and len(modelerNames) > 0:
            try:
                plugins = []
                operationOrg = dmd.Devices.getOrganizer(str(organizer))
                for plugin in operationOrg.zCollectorPlugins:
                    if str(plugin) in modelerNames:
                        log.info('MODELERS: Removing modeler %s', str(plugin))
                    else:
                        plugins.append(plugin)
                operationOrg.setZenProperty('zCollectorPlugins', plugins)
            except KeyError:
                log.warn('MODELERS: Problem removing modeler since specified organizer does exist')
                pass
            except Exception:
                log.error('MODELERS: Some unknown problem occured removing modelers')
                pass


    def recatalog(self, dmd, dontReIndex=0):
        try:
           if dmd.dontReindexMyStuffZenpack == 1: dontReIndex = 1
        except:
           log.info('CATALOG: Attribute dontReindexMyStuffZenpack created and set to 0. Toggle to 1 to skip future catalog operations.')
           dmd.dontReindexMyStuffZenpack = 0

        if dontReIndex != 1:
           # Update global catalog (important during upgrade)
           self.updateGlobalCatalog(dmd)

           # Update ZenPack persistance catalog
           self.updateZenPackPersistance(dmd)
        else:
           log.info('CATALOG: Per dontReindexMyStuffZenpack, skipping catalog updates')


    def updateGlobalCatalog(self, dmd):  
        log.info('CATALOG: Updating GC [This could take a really long time]')
        # Get global catalog log
        gc_log = logging.getLogger('Zope.ZCatalog')
        # Max logging
        gc_log.setLevel(logging.CRITICAL)
        # Reindex
        os.system('env python %s' % (zenPath('Products/ZenUtils/', 'zencatalog.py --reindex')))
        # Normal logging
        gc_log.setLevel(logging.INFO)


    def updateZenPackPersistance(self, dmd):
        # Update ZenPack persistance catalog
        from Products.ZCatalog.ProgressHandler import StdoutHandler
        log.info('CATALOG: Updating ZenPack Persistance Catalog [This could take a really long time]')
        dmd.zenPackPersistence.refreshCatalog(clear=1,pghandler=StdoutHandler())


    def symlinkPlugin(self):
        # Link daemon
        log.info('DAEMON: Nothing to link')


    def removePluginSymlink(self):
        # Unlink
        log.info('DAEMON: Nothing to unlink')


    def removeMenuItems(self, dmd, menuName):
        # Remove menu
        if menuName != '':
            log.info('MENUS: Removing menus')
            try:
                dmd.zenMenus._delObject(str(menuName))
            except AttributeError:
                pass
        else:
            log.info('MENUS: No menus to remove')


    def installMenuItems(self, dmd, menuName):
        # Install menus
        if menuName != '':
            log.info('MENUS: Installing menus')
            menu = ZenMenu(str(menuName))
            dmd.zenMenus._setObject(menu.id, menu)
            menu = dmd.zenMenus._getOb(menu.id)
        else:
            log.info('MENUS: No menus to install')


### Patching ###

# Imports
from Products.ZenModel.Device import Device




# Patches
@monkeypatch('Products.ZenModel.Device.Device')
def setCoreCount(self, zCoreCount):
    """
    Sets zCoreCount
    """
    if hasattr(self, 'zCoreCount'):
        self.zCoreCount = zCoreCount
    else:
        setattr(self, 'zCoreCount', zCoreCount)


@monkeypatch('Products.ZenModel.Device.Device')
def getCoreCount(self):
    """
    Returns zCoreCount if set
    """
    if hasattr(self, 'zCoreCount'):
        return self.zCoreCount
    else:
        return 0


@monkeypatch('Products.ZenModel.Device.Device')
def setThreadsPerCore(self, zThreadsPerCore):
    """
    Sets zThreadsPerCore
    """
    if hasattr(self, 'zThreadsPerCore'):
        self.zThreadsPerCore = zThreadsPerCore
    else:
        setattr(self, 'zThreadsPerCore', zThreadsPerCore)


@monkeypatch('Products.ZenModel.Device.Device')
def getThreadsPerCore(self):
    """
    Returns zThreadsPerCore if set
    """
    if hasattr(self, 'zThreadsPerCore'):
        return self.zThreadsPerCore
    else:
        return 0

@monkeypatch('Products.ZenModel.Device.Device')
def setFreeMemoryThresholdPercentLimit(self, zFreeMemoryThresholdPercentLimit):
    """
    Sets zFreeMemoryThresholdPercentLimit
    """
    if hasattr(self, 'zFreeMemoryThresholdPercentLimit'):
        self.zFreeMemoryThresholdPercentLimit = zFreeMemoryThresholdPercentLimit
    else:
        setattr(self, 'zFreeMemoryThresholdPercentLimit', zFreeMemoryThresholdPercentLimit)


@monkeypatch('Products.ZenModel.Device.Device')
def getFreeMemoryThresholdPercentLimit(self):
    """
    Returns zFreeMemoryThresholdPercentLimit if set
    """
    if hasattr(self, 'zFreeMemoryThresholdPercentLimit'):
        return self.zFreeMemoryThresholdPercentLimit
    else:
        return 0

@monkeypatch('Products.ZenModel.Device.Device')
def getFreeMemoryThresholdPercentLimitNice(self):
    """
    Returns zFreeMemoryThresholdPercentLimit if set, as a percent
    """
    if hasattr(self, 'zFreeMemoryThresholdPercentLimit'):
        return str(float(self.zFreeMemoryThresholdPercentLimit) * 100) + "%"
    else:
        return '0%'
