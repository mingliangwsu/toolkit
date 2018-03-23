QT += core
QT -= gui

CONFIG += c++11

TARGET = generate_location
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app
INCLUDEPATH = ../../../../../CropSyst/MicroBasin/util \
              ../../../../../corn

SOURCES += main.cpp \
    ../../../../../CropSyst/MicroBasin/util/pubtools.cpp \
    ../../../../../CropSyst/MicroBasin/util/esrigridclass.cpp
