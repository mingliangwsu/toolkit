QT += core
QT -= gui

CONFIG += c++11

TARGET = bin_to_ascii_converter
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += \
    bin_to_ascii.cpp
