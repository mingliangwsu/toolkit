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
    std::list<int> cell_contain_4001_4002_4003;
    std::list<int> irrig_cell_list;
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0]
                  << " [vic_veg_parameter] "
                  << " [orig_vic_irrig_parameter] "
                  << " [new_vic_irrig_parameter]"
                  << std::endl;
        exit(0);
    }
    std::ifstream vic_veg(argv[1]);
    std::ifstream vic_irrig(argv[2]);
    std::ofstream outf(argv[3]);
    //reading orig veg parameters and print to new veg paramater file
    std::string line;
    int gridid,numveg,veg_code;
    while (std::getline(vic_veg, line)) {
        std::istringstream iss(line);
        if (line[0] >= '0' && line[0] <= '9') {
            if (iss >> gridid >> numveg) {
                for (int veg = 0; veg < numveg; veg++) {
                    std::string vegline;
                    std::getline(vic_veg, vegline);
                    std::istringstream vegiss(vegline);
                    vegiss >> veg_code;
                    if (veg_code >= 4001 && veg_code <= 4003) {
                        cell_contain_4001_4002_4003.push_back(gridid);
                    }
                } //for each veg
            }
        }
    }
    vic_veg.close();
    //reading irrigation paramater
    while (std::getline(vic_irrig, line)) {
        std::istringstream iss(line);
        if (line[0] >= '0' && line[0] <= '9') {
            if (iss >> gridid >> numveg) {
                int num_potato = 0;
                std::string irrtype = "";
                std::list<Irr> irrlist;
                std::list<int> irr_veg_list;
                for (int veg = 0; veg < numveg; veg++) {
                    std::string vegline;
                    std::string irrig_type = "";
                    std::getline(vic_irrig, vegline);
                    std::istringstream vegiss(vegline);
                    vegiss >> veg_code >> irrig_type;
                    if (veg_code == 1827 || veg_code == 4001
                        || veg_code == 4002) {
                        num_potato++;
                        irrtype = irrig_type;
                    }
                    Irr t;
                    t.vegcode = veg_code;
                    t.type = irrig_type;
                    irrlist.push_back(t);
                    irr_veg_list.push_back((veg_code));
                } //for each veg
                std::list<int>::iterator findIter =
                    std::find(cell_contain_4001_4002_4003.begin(),
                              cell_contain_4001_4002_4003.end(), gridid);
                if (findIter != cell_contain_4001_4002_4003.end()) {
                    for (int veg = 4001; veg <= 4003; veg ++) {
                        std::list<int>::iterator it =
                            std::find(irr_veg_list.begin(),
                                      irr_veg_list.end(), veg);
                        if (it == irr_veg_list.end()) {
                            Irr t;
                            t.vegcode = veg;
                            t.type = irrtype.length() > 0 ? irrtype : "CENTER_PIVOT";
                            irrlist.push_back(t);
                        }
                    }
                }
                outf << gridid << " " << irrlist.size() << "\n";
                std::list<Irr>::iterator it;
                for(it = irrlist.begin(); it != irrlist.end(); ++it){
                    outf << "   " << it->vegcode << " " << it->type << "\n";
                }
            }
        }
    }
    vic_irrig.close();
    outf.close();
    std::clog << "Finished!\n";
    return 0;
}
