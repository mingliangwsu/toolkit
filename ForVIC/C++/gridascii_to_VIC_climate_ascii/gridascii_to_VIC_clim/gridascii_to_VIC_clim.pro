QT += core
QT -= gui

CONFIG += c++11

TARGET = gridascii_to_VIC_clim
CONFIG += console
CONFIG -= app_bundle

#for gcc
QMAKE_CXXFLAGS += -fopenmp
QMAKE_LFLAGS += -fopenmp


TEMPLATE = app
INCLUDEPATH = /home/liuming/dev/CropSyst/MicroBasin/util \
              /home/liuming/dev/corn \
              /home/liuming/dev/toolkits/read_UI_metdata/readUINetCDF
SOURCES += main.cpp \
    ../../../../../CropSyst/MicroBasin/util/esrigridclass.cpp \
    ../../../../../CropSyst/MicroBasin/util/pubtools.cpp \
    ../../../../read_UI_metdata/readUINetCDF/time_tools.cpp

LIBS += -lnetcdf -lm -fopenmp
