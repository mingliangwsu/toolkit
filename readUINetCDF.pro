QT += core
QT -= gui

CONFIG += c++11

TARGET = readUINetCDF
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

DEFINES += xHISTORICAL_MET xPRINT_DAILY_MET

INCLUDEPATH += ../../Calculate_ReferenceET/cal_reference_ET

SOURCES += main.cpp \
    time_tools.cpp \
    ../../Calculate_ReferenceET/cal_reference_ET/et_functions.cpp



HEADERS += \
    UInetcdf_constants.h \
    time_tools.h \
    ../../Calculate_ReferenceET/cal_reference_ET/et_functions.h

LIBS += -lnetcdf -lm -fopenmp
