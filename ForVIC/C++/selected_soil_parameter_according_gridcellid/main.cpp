#include <algorithm>    // std::find
#include <fstream>
#include <iostream>
#include <list>
#include <sstream>
#include <string>
#include "global_var.h"

typedef struct Irr {
    int vegcode;
    std::string type;
} Irr;

#ifdef TTT
int main(int argc, char *argv[])
{
    std::list<int> selected_cells;
    std::list<std::string> veg_list;
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0]
                  << " [soil_parameter] "
                  << " [selected_gridcell_list] "
                  << " [output_sub_soil_paramater] "
                  << std::endl;
        exit(0);
    }
    std::ifstream vic_soil(argv[1]);
    std::ifstream gridcell_id_list(argv[2]);
    std::ofstream outf(argv[3]);
    std::string line;
    int gridid,numveg,veg_code;

    //reading selected grid cell list
    while (std::getline(gridcell_id_list, line)) {
        std::istringstream iss(line);
        if (line[0] >= '0' && line[0] <= '9') {
            if (iss >> gridid) {
                selected_cells.push_back(gridid);
                std::clog << "selected:" << gridid << "\n";
            }
        }
    }
    gridcell_id_list.close();
    int selected;
    //reading orig soil parameters and print to new (subset) paramater file
    while (std::getline(vic_soil, line)) {
        std::istringstream iss(line);
        if (line[0] >= '0' && line[0] <= '9') {
            if (iss >> selected >> gridid) {
                std::list<int>::iterator findIter =
                std::find(selected_cells.begin(),
                          selected_cells.end(), gridid);
                if (findIter != selected_cells.end()) {
                    outf << line << std::endl;
                }
            }
        }
    }
    selected_cells.clear();
    vic_soil.close();
    outf.close();
    std::clog << "Finished!\n";
    return 0;
}
#endif

//extern int Liu::member1;

int main()
{
    Liu::member1 = 0;
    std::cout << "member1 = " << Liu::member1 << std::endl;
}
