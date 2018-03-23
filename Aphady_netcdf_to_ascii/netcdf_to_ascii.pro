QT += core
QT -= gui

CONFIG += c++11

TARGET = readUINetCDF
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

DEFINES += APHARO CHINA_CLIMATE_INTERPOLATION

INCLUDEPATH += ../../Calculate_ReferenceET/cal_reference_ET \
               /home/liuming/dev/toolkits/read_UI_metdata/readUINetCDF \
               /home/liuming/dev/CropSyst/MicroBasin/util \
               /home/liuming/dev/corn

SOURCES += main.cpp \
    ../../CropSyst/MicroBasin/util/esrigridclass.cpp \
    ../../CropSyst/MicroBasin/util/pubtools.cpp \
    ../read_UI_metdata/readUINetCDF/time_tools.cpp



HEADERS += \
    UInetcdf_constants.h \
    time_tools.h

LIBS += -lnetcdf -lm -fopenmp
