#include <algorithm>    // std::find
#include <fstream>
#include <iostream>
#include <list>
#include <sstream>
#include <string>

typedef struct Irr {
    int vegcode;
    std::string type;
} Irr;

int main(int argc, char *argv[])
{
    std::list<int> selected_crops = {3001, 3002, 3003, 4001, 4002};
    std::list<std::string> veg_list;
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0]
                  << " [vic_veg_parameter] "
                  << " [new_veg_parameter] "
                  << " [gridcell_list]"
                  << std::endl;
        exit(0);
    }
    std::ifstream vic_veg(argv[1]);
    std::ofstream outf(argv[2]);
    std::ofstream outf_gridcell(argv[3]);
    //reading orig veg parameters and print to new veg paramater file
    std::string line;
    int gridid,numveg,veg_code;
    while (std::getline(vic_veg, line)) {
        std::istringstream iss(line);
        veg_list.clear();
        if (line[0] >= '0' && line[0] <= '9') {
            if (iss >> gridid >> numveg) {
                for (int veg = 0; veg < numveg; veg++) {
                    std::string vegline;
                    std::getline(vic_veg, vegline);
                    std::istringstream vegiss(vegline);
                    vegiss >> veg_code;
                    std::list<int>::iterator findIter =
                        std::find(selected_crops.begin(),
                                  selected_crops.end(), veg_code);
                    if (findIter != selected_crops.end()) {
                        veg_list.push_back(vegline);
                    }
                } //for each veg
            }
            if (veg_list.size() > 0) {
                outf << gridid << " " << veg_list.size() << "\n";
                std::list<std::string>::iterator it;
                for(it = veg_list.begin(); it != veg_list.end(); ++it){
                    outf << *it << "\n";
                }
                outf_gridcell << gridid << "\n";
            }
        }
    }
    vic_veg.close();
    outf.close();
    outf_gridcell.close();
    std::clog << "Finished!\n";
    return 0;
}
