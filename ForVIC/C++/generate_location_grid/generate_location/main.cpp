#include "esrigridclass.h"
#include <iostream>

int main(int argc, char *argv[])
{
    if (argc < 4) {
        std::cerr << "Usage:"
                  << argv[0]
                  << " [boundary_grid_ascii] [out_x] [out_y] [size]\n";
        exit(0);
    }
    EsriGridClass<int> bound;
    bound.readAsciiGridFile(argv[1]);
    EsriGridClass<float> xy[2];
    double cellsize;
    if (argc < 5)
        cellsize = bound.getCellsize();
    else
        cellsize = atof(argv[4]);

    double xll = bound.getXll();
    double yll = bound.getYll();
    double yul = yll + bound.getNrows() * cellsize;

    for (int i = 0; i < 2; i++) {
        xy[i].setCellsize(cellsize);
        xy[i].setXll(xll);
        xy[i].setYll(yll);
        xy[i].setNcols(bound.getNcols());
        xy[i].setNrows(bound.getNrows());
        xy[i].AllocateMem();
        xy[i].setNodataValue(-9999.0);
    }

    for (int r = 0; r < bound.getNrows(); r++) {
        for (int c = 0; c < bound.getNcols(); c++) {
            if (bound.IsValidCell(r,c)) {
                xy[0].setValue(r,c,(double)(xll + (double)c * cellsize + cellsize / 2.0));
                xy[1].setValue(r,c,(double)(yul - (double)r * cellsize - cellsize / 2.0));
            } else {
                xy[0].setValue(r,c,-9999.0);
                xy[1].setValue(r,c,-9999.0);
            }
        }
    }

    xy[0].writeAsciiGridFile(argv[2]);
    xy[1].writeAsciiGridFile(argv[3]);
    std::clog << "Finished!\n";
    return 0;
}
