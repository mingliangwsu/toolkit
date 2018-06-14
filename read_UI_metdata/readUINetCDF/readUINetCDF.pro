QT += core
QT -= gui

CONFIG += c++11

TARGET = readUINetCDF
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

DEFINES += HISTORICAL_MET PRINT_DAILY_MET

INCLUDEPATH += ../../Calculate_ReferenceET/cal_reference_ET \
               /home/liuming/dev/CropSyst/MicroBasin/util \
              /home/liuming/dev/corn

SOURCES += \
    time_tools.cpp \
    ../../Calculate_ReferenceET/cal_reference_ET/et_functions.cpp \
    ../../../CropSyst/MicroBasin/util/esrigridclass.cpp \
    ../../../CropSyst/MicroBasin/util/pubtools.cpp \
    check_UI_historical_climate_data_new.cpp



HEADERS += \
    UInetcdf_constants.h \
    time_tools.h \
    ../../Calculate_ReferenceET/cal_reference_ET/et_functions.h

LIBS += -lnetcdf -lm -fopenmp
