/*
 * Configure.c
 * 
 * Gocator Sample
 * Copyright (C) 2011-2024 by LMI Technologies Inc.
 * 
 * Licensed under The MIT License.
 * Redistributions of files must retain the above copyright notice.
 *
 * Purpose: Connect to Gocator system and modify parameters
 *
 */
#include <GoSdk/GoSdk.h>
#include <stdio.h>

#define SENSOR_IP           "192.168.1.10"                      // serial number of the sensor used for sensor connection GoSystem_FindSensor() call.

int main(int argc, char **argv)
{
    kStatus status;
    kAssembly api = kNULL;
    GoSystem system = kNULL;
    GoSensor sensor = kNULL;
    GoSetup setup = kNULL;
    k64f currentExposure;
    k64f newExposure;   
    kIpAddress ipAddress;

    // construct Gocator API Library
    if ((status = GoSdk_Construct(&api)) != kOK)
    {
        printf("Error: GoSdk_Construct:%d\n", status);
        return kERROR;
    }

    // construct GoSystem object
    if ((status = GoSystem_Construct(&system, kNULL)) != kOK)
    {
        printf("Error: GoSystem_Construct:%d\n", status);
        return kERROR;
    }

    // Parse IP address into address data structure
    kIpAddress_Parse(&ipAddress, SENSOR_IP);

    // obtain GoSensor object by IP address
    if ((status = GoSystem_FindSensorByIpAddress(system, &ipAddress, &sensor)) != kOK)
    {
        printf("Error: GoSystem_FindSensor:%d\n", status);
        return kERROR;
    }

    // create connection to GoSensor object
    if ((status = GoSensor_Connect(sensor)) != kOK)
    {
        printf("Error: GoSensor_Connect:%d\n", status);
        return kERROR;
    }

    // retrieve setup handle
    if ((setup = GoSensor_Setup(sensor)) == kNULL)
    {
        printf("Error: GoSensor_Setup: Invalid Handle\n");
        return kERROR;
    }   

    if ((status = GoSensor_CopyFile(sensor, "_live.job", "oldExposure.job")) != kOK)
    {
        printf("Error: GoSensor_CopyFile:%d\n", status);
        return kERROR;
    }

    // read current parameters
    currentExposure = GoSetup_Exposure(setup, GO_ROLE_MAIN);
    printf("Current Parameters:\n");
    printf("-------------------\n");
    printf("Exposure:%f us\n\n", currentExposure);
    
    // modify parameter in main sensor
    if ((status = GoSetup_SetExposure(setup, GO_ROLE_MAIN, currentExposure + 200)) != kOK)
    {
        printf("Error: GoSetup_SetExposure:%d\n", status);
        return kERROR;
    }

    // GoSensorFlush() - immediately synchronizes configuration changes to the sensor
    // *The changes will be shown on the web browser GUI after the browser has been refreshed.
    // NOTE: Sensor is not automatically synchronized with every call to function that modifies a setting.
    // This allows for rapid configuring sensors without delay caused by synchronization after every call.
    // Generally functions that retreieve setting values causes automatic synchronization while functions that set values don't.
    // Synchronization is also always guranteed prior to sensor entering running state. The GoSensor_Flush() function
    // should only be used when configuration changes are needed to be seen immediately.
    GoSensor_Flush(sensor);

    newExposure = GoSetup_Exposure(setup, GO_ROLE_MAIN);


    printf("New Parameters:\n");
    printf("---------------\n");
    printf("Exposure:%f us\n\n", newExposure);

    // Save the configuration and template into a new file set. This is the same behavior
    // as if the user clicks the save button in the toolbar.

    if ((status = GoSensor_CopyFile(sensor, "_live.job", "newExposure.job")) != kOK)
    {
        printf("Error: GoSensor_CopyFile:%d\n", status);
        return kERROR;
    }

    // Set the saved configuration as default job. This makes it the active configuration when the sensor powers up.
    if ((status = GoSensor_SetDefaultJob(sensor, "newExposure.job")) != kOK)
    {
        printf("Error: GoSensor_SetDefaultJob:%d\n", status);
        return kERROR;
    }
    
    // Switches back to the original exposure
    if ((status = GoSensor_CopyFile(sensor, "oldExposure.job", "_live.job")) != kOK)
    {
        printf("Error: GoSensor_CopyFile:%d\n", status);
        return kERROR;
    }
    
    // destroy handles
    GoDestroy(system);
    GoDestroy(api);

    printf("Press any key to continue...\n");
    getchar();

    return kOK;
}
