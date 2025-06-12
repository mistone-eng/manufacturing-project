ifndef verbose
	SILENT = @
endif

.PHONY: all
all: kApi GoSdk AlignmentMoving AlignmentStationary BackupRestore Configure ConsoleExample Discover DualSensor MultiSensorLayout ReceiveAsync ReceiveHealth ReceiveMeasurement ReceivePartSegments ReceiveProfile ReceiveRange ReceiveSurface ReceiveSurfaceFlatness ReceiveSurfaceTrack ReceiveSync SetupMeasurement

.PHONY: kApi
kApi: 
	$(SILENT) $(MAKE) -C ../../Platform/kApi -f kApi-Linux_X64.mk

.PHONY: GoSdk
GoSdk: kApi 
	$(SILENT) $(MAKE) -C ../../Gocator/GoSdk -f GoSdk-Linux_X64.mk

.PHONY: AlignmentMoving
AlignmentMoving: GoSdk 
	$(SILENT) $(MAKE) -C AlignmentMoving -f AlignmentMoving-Linux_X64.mk

.PHONY: AlignmentStationary
AlignmentStationary: GoSdk 
	$(SILENT) $(MAKE) -C AlignmentStationary -f AlignmentStationary-Linux_X64.mk

.PHONY: BackupRestore
BackupRestore: GoSdk
	$(SILENT) $(MAKE) -C BackupRestore -f BackupRestore-Linux_X64.mk

.PHONY: Configure
Configure: GoSdk
	$(SILENT) $(MAKE) -C Configure -f Configure-Linux_X64.mk

.PHONY: ConsoleExample
ConsoleExample: GoSdk
	$(SILENT) $(MAKE) -C ConsoleExample -f ConsoleExample-Linux_X64.mk

.PHONY: Discover
Discover: GoSdk
	$(SILENT) $(MAKE) -C Discover -f Discover-Linux_X64.mk

.PHONY: DualSensor
DualSensor: GoSdk
	$(SILENT) $(MAKE) -C DualSensor -f DualSensor-Linux_X64.mk

.PHONY: MultiSensorLayout
MultiSensorLayout: GoSdk
	$(SILENT) $(MAKE) -C MultiSensorLayout -f MultiSensorLayout-Linux_X64.mk

.PHONY: ReceiveAsync
ReceiveAsync: GoSdk
	$(SILENT) $(MAKE) -C ReceiveAsync -f ReceiveAsync-Linux_X64.mk

.PHONY: ReceiveHealth
ReceiveHealth: GoSdk
	$(SILENT) $(MAKE) -C ReceiveHealth -f ReceiveHealth-Linux_X64.mk

.PHONY: ReceiveMeasurement
ReceiveMeasurement: GoSdk
	$(SILENT) $(MAKE) -C ReceiveMeasurement -f ReceiveMeasurement-Linux_X64.mk

.PHONY: ReceivePartSegments
ReceivePartSegments: GoSdk
	$(SILENT) $(MAKE) -C ReceivePartSegments -f ReceivePartSegments-Linux_X64.mk

.PHONY: ReceiveProfile
ReceiveProfile: GoSdk
	$(SILENT) $(MAKE) -C ReceiveProfile -f ReceiveProfile-Linux_X64.mk

.PHONY: ReceiveRange
ReceiveRange: GoSdk
	$(SILENT) $(MAKE) -C ReceiveRange -f ReceiveRange-Linux_X64.mk

.PHONY: ReceiveSurface
ReceiveSurface: GoSdk
	$(SILENT) $(MAKE) -C ReceiveSurface -f ReceiveSurface-Linux_X64.mk

.PHONY: ReceiveSurfaceFlatness
ReceiveSurfaceFlatness: GoSdk
	$(SILENT) $(MAKE) -C ReceiveSurfaceFlatness -f ReceiveSurfaceFlatness-Linux_X64.mk

.PHONY: ReceiveSurfaceTrack
ReceiveSurfaceTrack: GoSdk
	$(SILENT) $(MAKE) -C ReceiveSurfaceTrack -f ReceiveSurfaceTrack-Linux_X64.mk

.PHONY: ReceiveSync
ReceiveSync: GoSdk
	$(SILENT) $(MAKE) -C ReceiveSync -f ReceiveSync-Linux_X64.mk

.PHONY: SetupMeasurement
SetupMeasurement: GoSdk
	$(SILENT) $(MAKE) -C SetupMeasurement -f SetupMeasurement-Linux_X64.mk

.PHONY: clean
clean: kApi-clean GoSdk-clean AlignmentMoving-clean AlignmentStationary-clean BackupRestore-clean Configure-clean ConsoleExample-clean Discover-clean DualSensor-clean MultiSensorLayout-clean ReceiveAsync-clean ReceiveHealth-clean ReceiveMeasurement-clean ReceivePartSegments-clean ReceiveProfile-clean ReceiveRange-clean ReceiveSurface-clean ReceiveSurfaceFlatness-clean ReceiveSurfaceTrack-clean ReceiveSync-clean SetupMeasurement-clean 

.PHONY: kApi-clean
kApi-clean:
	$(SILENT) $(MAKE) -C ../../Platform/kApi -f kApi-Linux_X64.mk clean

.PHONY: GoSdk-clean
GoSdk-clean:
	$(SILENT) $(MAKE) -C ../../Gocator/GoSdk -f GoSdk-Linux_X64.mk clean

.PHONY: AlignmentMoving-clean
AlignmentMoving-clean:
	$(SILENT) $(MAKE) -C AlignmentMoving -f AlignmentMoving-Linux_X64.mk clean

.PHONY: AlignmentStationary-clean
AlignmentStationary-clean:
	$(SILENT) $(MAKE) -C AlignmentStationary -f AlignmentStationary-Linux_X64.mk clean

.PHONY: BackupRestore-clean
BackupRestore-clean:
	$(SILENT) $(MAKE) -C BackupRestore -f BackupRestore-Linux_X64.mk clean

.PHONY: Configure-clean
Configure-clean:
	$(SILENT) $(MAKE) -C Configure -f Configure-Linux_X64.mk clean

.PHONY: ConsoleExample-clean
ConsoleExample-clean:
	$(SILENT) $(MAKE) -C ConsoleExample -f ConsoleExample-Linux_X64.mk clean

.PHONY: Discover-clean
Discover-clean:
	$(SILENT) $(MAKE) -C Discover -f Discover-Linux_X64.mk clean

.PHONY: DualSensor-clean
DualSensor-clean:
	$(SILENT) $(MAKE) -C DualSensor -f DualSensor-Linux_X64.mk clean

.PHONY: MultiSensorLayout-clean
MultiSensorLayout-clean:
	$(SILENT) $(MAKE) -C MultiSensorLayout -f MultiSensorLayout-Linux_X64.mk clean

.PHONY: ReceiveAsync-clean
ReceiveAsync-clean:
	$(SILENT) $(MAKE) -C ReceiveAsync -f ReceiveAsync-Linux_X64.mk clean

.PHONY: ReceiveHealth-clean
ReceiveHealth-clean:
	$(SILENT) $(MAKE) -C ReceiveHealth -f ReceiveHealth-Linux_X64.mk clean

.PHONY: ReceiveMeasurement-clean
ReceiveMeasurement-clean:
	$(SILENT) $(MAKE) -C ReceiveMeasurement -f ReceiveMeasurement-Linux_X64.mk clean

.PHONY: ReceivePartSegments-clean
ReceivePartSegments-clean:
	$(SILENT) $(MAKE) -C ReceivePartSegments -f ReceivePartSegments-Linux_X64.mk clean

.PHONY: ReceiveProfile-clean
ReceiveProfile-clean:
	$(SILENT) $(MAKE) -C ReceiveProfile -f ReceiveProfile-Linux_X64.mk clean

.PHONY: ReceiveRange-clean
ReceiveRange-clean:
	$(SILENT) $(MAKE) -C ReceiveRange -f ReceiveRange-Linux_X64.mk clean

.PHONY: ReceiveSurface-clean
ReceiveSurface-clean:
	$(SILENT) $(MAKE) -C ReceiveSurface -f ReceiveSurface-Linux_X64.mk clean

.PHONY: ReceiveSurfaceFlatness-clean
ReceiveSurfaceFlatness-clean:
	$(SILENT) $(MAKE) -C ReceiveSurfaceFlatness -f ReceiveSurfaceFlatness-Linux_X64.mk clean

.PHONY: ReceiveSurfaceTrack-clean
ReceiveSurfaceTrack-clean:
	$(SILENT) $(MAKE) -C ReceiveSurfaceTrack -f ReceiveSurfaceTrack-Linux_X64.mk clean

.PHONY: ReceiveSync-clean
ReceiveSync-clean:
	$(SILENT) $(MAKE) -C ReceiveSync -f ReceiveSync-Linux_X64.mk clean

.PHONY: SetupMeasurement-clean
SetupMeasurement-clean:
	$(SILENT) $(MAKE) -C SetupMeasurement -f SetupMeasurement-Linux_X64.mk clean


