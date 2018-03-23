QT += core
QT -= gui

CONFIG += c++11

TARGET = selected_soil_parameter_according_gridcellid
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    global_var.cpp

HEADERS += \
    global_var.h
