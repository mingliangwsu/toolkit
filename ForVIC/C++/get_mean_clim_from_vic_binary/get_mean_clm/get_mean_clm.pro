QT += core
QT -= gui

CONFIG += c++11

TARGET = get_mean_clm
CONFIG += console
CONFIG -= app_bundle

DEFINES = TEST_DATA

TEMPLATE = app
INCLUDEPATH = /home/liuming/dev/CropSyst/MicroBasin/util \
              /home/liuming/dev/corn \
              /home/liuming/dev/toolkits/read_UI_metdata/readUINetCDF

SOURCES += \
    ../../../../../CropSyst/MicroBasin/util/esrigridclass.cpp \
    ../../../../../CropSyst/MicroBasin/util/pubtools.cpp \
    ../../../../read_UI_metdata/readUINetCDF/time_tools.cpp \
    generate_mean_vic_bin_climate_data.cpp

LIBS += -lnetcdf -lm -fopenmp
