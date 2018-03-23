QT += core
QT -= gui

CONFIG += c++11

TARGET = cal_reference_ET
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    et_functions.cpp

HEADERS += \
    et_functions.h
