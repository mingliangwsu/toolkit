#ifndef ADJ_MET_H
#define ADJ_MET_H
#include <string>
#define START_YEAR 1895
#define END_YEAR 2017
#define DISTURB_YEARS (END_YEAR - START_YEAR + 1)
typedef struct Adj_record {
    int year;
    int month;
    double tmax;
    double tmin;
    double sph;    //fraction
    double srad;
    double wind;
    double ppt;
    double rmax;
    double rmin;

} Adj_records;
bool read_disturb_data(std::string filename, Adj_records* data);
int get_disturb_index(int year, int month);
#endif // ADJ_MET_H
