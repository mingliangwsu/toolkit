#ifndef OLD_VEG_TYPE_LIST_H
#define OLD_VEG_TYPE_LIST_H
#include <map>
extern std::map<int,int> veg_type_list;
typedef struct Veg_paramater {
    int veg_code;
    double fraction;
    double dep1;
    double f1;
    double dep2;
    double f2;
    double dep3;
    double f3;
} Veg_paramater;

#endif // OLD_VEG_TYPE_LIST_H
