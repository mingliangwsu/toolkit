#include <algorithm>    // std::find
#include <fstream>
#include <iostream>
#include <list>
#include <sstream>
#include <string>
#include "esrigridclass.h"
#define MAX_VIC_CELL 413060
#define MAX_VEG_TYPE 6000

typedef struct Irr {
    int vegcode;
    std::string type;
} Irr;

int main(int argc, char *argv[])
{
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0]
                  << " [vic_veg_parameter] "
                  << " [vic_cell_id_esri_grid_ascii]"
                  << " [prefix_output] "
                  << std::endl;
        exit(0);
    }
    std::ifstream vic_veg(argv[1]);
    EsriGridClass<int> viccell;
    viccell.readAsciiGridFile(argv[2]);
    std::string outf_gridcell_pre(argv[3]);
    std::clog << "Allocating mem...\n";
    double **vegfraction = alloc_2d_array<double>(MAX_VIC_CELL,MAX_VEG_TYPE,"vegfraction");
    double *sum_type = alloc_1d_array<double>(MAX_VEG_TYPE,"sum_type");
    for (int i = 0; i < MAX_VIC_CELL; i++) {
        for (int j = 0; j < MAX_VEG_TYPE; j++) {
            vegfraction[i][j] = 0.0;
        }
    }
    for (int j = 0; j < MAX_VEG_TYPE; j++) {
        sum_type[j] = 0.0;
    }
    std::clog << "Reading veg parameter...\n";
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
                    double fraction;
                    vegiss >> veg_code >> fraction;
                    vegfraction[gridid][veg_code] = fraction;
                    sum_type[veg_code] += fraction;
                } //for each veg
            }
        }
    }
    vic_veg.close();
    std::clog << "Writting outputs ...\n";
    //Write output grid ascii
    for (int j = 0; j < MAX_VEG_TYPE; j++) {
        if (sum_type[j] > 1.0e-6) {
            EsriGridClass<double> outf_gridcell;
            outf_gridcell.setNcols(viccell.getNcols());
            outf_gridcell.setNrows(viccell.getNrows());
            outf_gridcell.setNodataValue(-9999.0);
            outf_gridcell.setXll(viccell.getXll());
            outf_gridcell.setYll(viccell.getYll());
            outf_gridcell.setCellsize(viccell.getCellsize());
            outf_gridcell.AllocateMem();
            outf_gridcell.InitAllNovalue();
            for (int r = 0; r < outf_gridcell.getNrows(); r++) {
                for (int c = 0; c < outf_gridcell.getNcols(); c++) {
                    int grid_id = viccell.getValue(r,c);
                    if (grid_id >= 0) {
                        outf_gridcell.setValue(r,c,vegfraction[grid_id][j]);
                    }
                }
            }
            std::string outfilename = outf_gridcell_pre + std::to_string(j) + ".asc";
            outf_gridcell.writeAsciiGridFile(outfilename);
        }
    }
    //clean up
    std::clog << "Cleanning up...\n";
    delete_2d_array(vegfraction,MAX_VIC_CELL);
    delete_1d_array(sum_type);
    std::clog << "Finished!\n";
    return 0;
}
