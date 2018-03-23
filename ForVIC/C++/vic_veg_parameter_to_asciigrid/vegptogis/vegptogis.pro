QT += core
QT -= gui

CONFIG += c++11

TARGET = vegptogis
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app
INCLUDEPATH += ../../../../../CropSyst/MicroBasin/util \
               ../../../../../corn

SOURCES += \
    ../vic_veg_parameter_to_asciigrid.cpp \
    ../../../../../CropSyst/MicroBasin/util/pubtools.cpp \
    ../../../../../CropSyst/MicroBasin/util/esrigridclass.cpp
