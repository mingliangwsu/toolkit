QT += core
QT -= gui

CONFIG += c++11

TARGET = read_sisi_climate
CONFIG += console
CONFIG -= app_bundle

QMAKE_CXXFLAGS += -fopenmp
QMAKE_LFLAGS += -fopenmp -Wl,-Map=testmap.txt

DEFINES = CHINA_CLIMATE_INTERPOLATION

TEMPLATE = app

INCLUDEPATH = /home/liuming/dev/CropSyst/MicroBasin/util \
              /home/liuming/dev/corn \
              /home/liuming/dev/toolkits/read_UI_metdata/readUINetCDF \
              /home/liuming/dev/toolkits/alglib-3.12.0.cpp/src

SOURCES += \
    climread_2.cpp \
    ../../../../../CropSyst/MicroBasin/util/pubtools.cpp \
    ../../../../../CropSyst/MicroBasin/util/esrigridclass.cpp \
    ../../../../read_UI_metdata/readUINetCDF/time_tools.cpp \
    ../../../../alglib-3.12.0.cpp/src/diffequations.cpp \
    ../../../../alglib-3.12.0.cpp/src/alglibmisc.cpp \
    ../../../../alglib-3.12.0.cpp/src/alglibinternal.cpp \
    ../../../../alglib-3.12.0.cpp/src/specialfunctions.cpp \
    ../../../../alglib-3.12.0.cpp/src/ap.cpp \
    ../../../../alglib-3.12.0.cpp/src/interpolation.cpp \
    ../../../../alglib-3.12.0.cpp/src/linalg.cpp \
    ../../../../alglib-3.12.0.cpp/src/integration.cpp \
    ../../../../alglib-3.12.0.cpp/src/dataanalysis.cpp \
    ../../../../alglib-3.12.0.cpp/src/fasttransforms.cpp \
    ../../../../alglib-3.12.0.cpp/src/statistics.cpp \
    ../../../../alglib-3.12.0.cpp/src/optimization.cpp \
    ../../../../alglib-3.12.0.cpp/src/solvers.cpp

LIBS += -lnetcdf -lm -fopenmp
