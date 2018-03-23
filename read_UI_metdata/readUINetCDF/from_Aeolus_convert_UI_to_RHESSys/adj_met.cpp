#include "adj_met.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string.h>
double tmax;
double tmin;
double sph;    //fraction
double srad;
double wind;
double ppt;
double rmax;
double rmin;
bool read_disturb_data(std::string filename, Adj_records* data)
{
    std::ifstream disturb_file(filename.c_str());
    std::string line;
    int index = 0;
    while (std::getline(disturb_file, line)) {
        std::istringstream iss(line);
        if (line[0] >= '0' && line[0] <= '9') {
            if (iss >> data[index].year
                    >> data[index].month
                    >> data[index].tmax
                    >> data[index].tmin
                    >> data[index].sph
                    >> data[index].srad
                    >> data[index].wind
                    >> data[index].ppt
                    >> data[index].rmax
                    >> data[index].rmin) {
            }
            index++;
        }
    }
    disturb_file.close();
    return true;
}
//______________________________________________________________________________
int get_disturb_index(int year, int month)
{   //month: 1-12
    if (year < START_YEAR || year > END_YEAR) return -1;
    else {
        return (year - START_YEAR) * 12 + (month - 1);
    }
}
