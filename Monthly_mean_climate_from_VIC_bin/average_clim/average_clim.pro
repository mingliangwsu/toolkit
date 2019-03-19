QT += core
QT -= gui

CONFIG += c++11

TARGET = average_clim
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    time_tools.cpp
