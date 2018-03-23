QT += core
QT -= gui

#CONFIG += c++11

TARGET = adjust_VIC_veg_parameter_file
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    old_veg_type_list.cpp

HEADERS += \
    old_veg_type_list.h \
    cdl_area.h
