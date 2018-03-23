#include "esrigridclass.h"
#include <iostream>

int main(int argc, char *argv[])
{
    /*if (argc < 4) {
        std::cerr << "Usage:"
                  << argv[0]
                  << " [boundary_grid_ascii] [out_x] [out_y] [size]\n";
        exit(0);
    }*/
    EsriGridClass<int> cellid;
    EsriGridClass<int> stateidfill;
    EsriGridClass<int> fruitmask;
    EsriGridClass<double> apple;
    EsriGridClass<double> pears;
    EsriGridClass<double> walnut;
    EsriGridClass<double> lat;
    EsriGridClass<double> lon;

    cellid.readAsciiGridFile("cellid.asc");
    stateidfill.readAsciiGridFile("stateidfill.asc");
    fruitmask.readAsciiGridFile("ildall.asc");
    apple.readAsciiGridFile("ld68.asc");
    pears.readAsciiGridFile("ld77.asc");
    walnut.readAsciiGridFile("ld76.asc");
    lat.readAsciiGridFile("lat.asc");
    lon.readAsciiGridFile("lon.asc");

    FILE *outfile = fopen("/home/liuming/temp/conus_tree_fruit.txt","w");

    fprintf(outfile,"lat,lon,cellid,stateid,apple,pears,walnut\n");

    for (int r = 0; r < fruitmask.getNrows(); r++) {
        for (int c = 0; c < fruitmask.getNcols(); c++) {
            if (fruitmask.IsValidCell(r,c)) {
                fprintf(outfile,"%.5f,%.5f,%d,%d,%f,%f,%f\n",
                        lat.getValue(r,c),
                        lon.getValue(r,c),
                        cellid.getValue(r,c),
                        stateidfill.getValue(r,c),
                        apple.getValue(r,c),
                        pears.getValue(r,c),
                        walnut.getValue(r,c));
            }
        }
    }

    fclose(outfile);
    std::clog << "Finished!\n";
    return 0;
}
