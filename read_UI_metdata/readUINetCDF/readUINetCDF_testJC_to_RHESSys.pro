QT += core
QT -= gui

CONFIG += c++11

TARGET = readUINetCDF
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

DEFINES += HISTORICAL_MET xPRINT_DAILY_MET \
           xCHECK_WITH_GIS \
           REMOVE_HUMAN_EFFECT

INCLUDEPATH += ../../Calculate_ReferenceET/cal_reference_ET \
               /home/liuming/dev/CropSyst/MicroBasin/util \
              /home/liuming/dev/corn \
              /home/liuming/dev/toolkits/read_UI_metdata/readUINetCDF/from_Aeolus_convert_UI_to_RHESSys

SOURCES += \
    time_tools.cpp \
    ../../Calculate_ReferenceET/cal_reference_ET/et_functions.cpp \
    ../../../CropSyst/MicroBasin/util/esrigridclass.cpp \
    ../../../CropSyst/MicroBasin/util/pubtools.cpp \
    convert_UI_JC_to_RHESSys_netcdf.cpp \
    from_Aeolus_convert_UI_to_RHESSys/adj_met.cpp



HEADERS += \
    UInetcdf_constants.h \
    time_tools.h \
    ../../Calculate_ReferenceET/cal_reference_ET/et_functions.h

LIBS += -lnetcdf -lm -fopenmp
