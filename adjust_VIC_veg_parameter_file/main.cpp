#include "cdl_area.h"
#include "old_veg_type_list.h"

#include <fstream>
#include <iostream>
#include <list>
#include <map>
#include <sstream>
#include <string>

#define PRINT_SUM_FRACTION
#ifdef PRINT_SUM_FRACTION
#define NUM_VEG 166
#endif

#define MINIMUM_FRACTION 0.005
bool is_veg_exist_in_cdl(const CDL_areas *cdl, const int gid,
                         const std::string c_name);

int main(int argc, char *argv[])
{
#ifdef PRINT_SUM_FRACTION
    double total_fraction_print[NUM_VEG];
    for (int i = 0; i < NUM_VEG; i++) {
        total_fraction_print[i] = 0;
    }
#endif
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0]
                  << " [orig_vic_veg_parameter] "
                  << " [new_vic_veg_parameter] "
                  << " [cdl_file_name]"
                  << std::endl;
        exit(0);
    }
    int all_veg_count = veg_type_list.size();
    std::string orig_vic_veg_filename(argv[1]);
    std::string new_vic_veg_filename(argv[2]);
    std::ifstream orig_vic_veg(orig_vic_veg_filename);
    std::ofstream outf(new_vic_veg_filename);
    CDL_areas *cdl_area_list = 0;
    std::map<int,int> cdl_type_id;
    int num_grid_cdl = 0;
    //read cdl area information for each grid
    if (argc == 4) {
        std::ifstream fcdl(argv[3]);
        std::string line;
        while (std::getline(fcdl, line)) {
            if (line[0] >= '0' && line[0] <= '9') num_grid_cdl++;
        }
        fcdl.seekg(0, fcdl.beg);
        cdl_area_list = new CDL_areas[num_grid_cdl];
        int grid_index = 0;
        while (std::getline(fcdl, line) && grid_index < num_grid_cdl) {
            std::istringstream iss(line);
            CDL_areas &cdl = cdl_area_list[grid_index];
            if (line[0] >= '0' && line[0] <= '9') {
                iss >> cdl.gridid
                    >> cdl.corn
                    >> cdl.sweet_corn
                    >> cdl.barley
                    >> cdl.spring_wheat
                    >> cdl.winter_wheat
                    >> cdl.canola
                    >> cdl.alfafa
                    >> cdl.sugar_beet
                    >> cdl.dry_bean
                    >> cdl.potato;
                cdl_type_id[cdl.gridid] = grid_index;
                grid_index++;
            }
        }
        fcdl.close();
    }
    //reading orig veg parameters and print to new veg paramater file
    int gridid,numveg;
    std::string line;
    while (std::getline(orig_vic_veg, line)) {
        std::istringstream iss(line);
        if (line[0] >= '0' && line[0] <= '9') {
                if (iss >> gridid >> numveg) {
                    std::list<Veg_paramater> vicveg;
                    double total_fraction_large = 0;
                    double total_fraction_small = 0;
                    double total_fraction = 0;
                    for (int veg = 0; veg < numveg; veg++) {
                        Veg_paramater veg_record;
                        std::getline(orig_vic_veg, line);
                        std::istringstream vegiss(line);
                        vegiss >> veg_record.veg_code
                               >> veg_record.fraction
                               >> veg_record.dep1
                               >> veg_record.f1
                               >> veg_record.dep2
                               >> veg_record.f2
                               >> veg_record.dep3
                               >> veg_record.f3;
                        vicveg.push_back(veg_record);
                        if (veg_record.fraction < MINIMUM_FRACTION)
                            total_fraction_small += veg_record.fraction;
                        else
                            total_fraction_large += veg_record.fraction;
                        total_fraction = total_fraction_small
                                         + total_fraction_large;
                    } //for each veg
                    std::list<Veg_paramater>::iterator it;
                    if (total_fraction_small > 1e-20) {
                        for (it = vicveg.begin(); it != vicveg.end(); ) {
                            if (it->fraction >= MINIMUM_FRACTION) {
                                it->fraction += total_fraction_small
                                    * (it->fraction / total_fraction_large);
                                ++it;
                            } else {
                                it = vicveg.erase(it);
                            }
                        }
                    }
                    //Handle the annual crops with information from CDL layer
                    std::map<int,int>::iterator cdl_it;
                    cdl_it = cdl_type_id.find(gridid);
                    int cdl_grid_index = -1;
                    if (cdl_it != cdl_type_id.end()) {
                        cdl_grid_index = cdl_it->second;
                    }
                    //count potato and corn that don't have set rotation

                    double *veg_fraction     = new double[all_veg_count];
                    double *new_veg_fraction = new double[all_veg_count];
                    for (int veg = 0; veg < all_veg_count; veg++) {
                        veg_fraction[veg]       = 0;
                        new_veg_fraction[veg]   = 0;
                    }
                    for (it = vicveg.begin(); it != vicveg.end(); ++it) {
                        std::map<int,int>::iterator veg_it =
                            veg_type_list.find(it->veg_code);
                        if (veg_it == veg_type_list.end()) {
                            std::cerr << "ERROR: veg:" << it->veg_code
                                      << " is not in the veg list!\n";
                            exit(0);
                        }
                        int veg_index = veg_it->second;
                        veg_fraction[veg_index]     = it->fraction;
                        new_veg_fraction[veg_index] = veg_fraction[veg_index];

                        /*std::clog << "After first clean:\n"
                                  << "\tgridid:" << gridid
                                  << "\tveg:"  << it->veg_code
                                  << "\tveg_index:" << veg_index
                                  << "\tfract:"<< veg_fraction[veg_index]
                                  << "\tnewfract:"<< new_veg_fraction[veg_index]
                                  << std::endl;*/
                    }
                    double potato       = veg_fraction[veg_type_list[1827]];
                    double corn         = veg_fraction[veg_type_list[204]]
                                            + veg_fraction[veg_type_list[205]]
                                            + veg_fraction[veg_type_list[1509]]
                                            + veg_fraction[veg_type_list[1814]];
                    double alfalfa      = veg_fraction[veg_type_list[701]]
                                            + veg_fraction[veg_type_list[703]]
                                            + veg_fraction[veg_type_list[1501]]
                                            + veg_fraction[veg_type_list[5701]];
                    double winter_wheat = veg_fraction[veg_type_list[211]]
                                            + veg_fraction[veg_type_list[218]];
                    double suger_beet   = veg_fraction[veg_type_list[1502]]
                                            + veg_fraction[veg_type_list[1520]]
                                            + veg_fraction[veg_type_list[1832]];
                    double spring_wheat = veg_fraction[veg_type_list[210]];

                    double used_corn        = 0;
                    double used_suger_beet  = 0;
                    double used_ww          = 0;
                    //now, clear all above annual crops at first
                    new_veg_fraction[veg_type_list[1827]]   = 0;
                    new_veg_fraction[veg_type_list[204]]    = 0;
                    new_veg_fraction[veg_type_list[205]]    = 0;
                    new_veg_fraction[veg_type_list[1509]]   = 0;
                    new_veg_fraction[veg_type_list[1814]]   = 0;
                    new_veg_fraction[veg_type_list[701]]    = 0;
                    new_veg_fraction[veg_type_list[703]]    = 0;
                    new_veg_fraction[veg_type_list[1501]]   = 0;
                    new_veg_fraction[veg_type_list[5701]]   = 0;
                    new_veg_fraction[veg_type_list[211]]    = 0;
                    new_veg_fraction[veg_type_list[218]]    = 0;
                    new_veg_fraction[veg_type_list[1502]]   = 0;
                    new_veg_fraction[veg_type_list[1520]]   = 0;
                    new_veg_fraction[veg_type_list[1832]]   = 0;
                    new_veg_fraction[veg_type_list[210]]    = 0;
                    new_veg_fraction[veg_type_list[5701]]   = 0;


                    //Handle the potato
                    if (potato > 0) {
                        if (suger_beet > 0 || is_veg_exist_in_cdl(cdl_area_list,
                                                 cdl_grid_index,"sugar_beet")) {
                            new_veg_fraction[veg_type_list[4002]] += potato;     //P-SB-C
                            used_suger_beet += potato;
                            used_corn       += potato;
                        } else {
                            new_veg_fraction[veg_type_list[4001]] += potato;     //P-WW-C
                            used_corn += potato;
                            used_ww   += potato;
                        }
                    }
                    //Handle the left corn
                    double left_corn = corn - used_corn;
                    double left_alfalfa = alfalfa;
                    if (left_corn > 0) {
                        if (alfalfa > 0) {
                            double corn_alf = std::min(left_corn,
                                                       alfalfa / 3.0);
                            new_veg_fraction[veg_type_list[4003]] += corn_alf;
                            left_corn    -= corn_alf;
                            left_alfalfa -= corn_alf * 3.0;
                        }
                        if (left_corn > 0) {                                     //if still has corn; set it rotate with Alfalfa
                            new_veg_fraction[veg_type_list[4003]] += left_corn;
                            left_alfalfa -= left_corn * 3.0;
                            if (left_alfalfa < 0) left_alfalfa = 0;
                        }
                    }
                    new_veg_fraction[veg_type_list[5701]] += left_alfalfa;       //left all left alfalfa to rotation type 5701
                    //Handle Suger Beet. Put all suger beet to 1832
                    new_veg_fraction[veg_type_list[1832]] =
                        std::max(suger_beet - used_suger_beet, 0.0);
                    //Handle WW & SP
                    double left_WW = std::max(winter_wheat - used_ww, 0.0);
                    double total_wheat = left_WW + spring_wheat;

                    if (total_wheat > 0) {
                        if (spring_wheat > 0 && new_veg_fraction[veg_type_list[3001]] > 0) {
                            new_veg_fraction[veg_type_list[3001]] += total_wheat;
                        } else if (spring_wheat > 0 && new_veg_fraction[veg_type_list[3002]] > 0) {
                            new_veg_fraction[veg_type_list[3002]] += total_wheat;
                        } else {
                            new_veg_fraction[veg_type_list[3003]] += total_wheat;
                        }
                    }
                    //clean up all empty records and set new value if not empty
                    for (it = vicveg.begin(); it != vicveg.end(); ) {
                        int veg_index = veg_type_list[it->veg_code];
                        /*std::clog << "In second clean...\n"
                                  << "\tveg:"   << it->veg_code
                                  << "\tveg_index:" << veg_index
                                  << "\tfract:" << new_veg_fraction[veg_index]
                                  << std::endl;*/
                        if (new_veg_fraction[veg_index] < MINIMUM_FRACTION) {
                            //std::clog << "erased:" << it->veg_code << std::endl;
                            it = vicveg.erase(it);
                        } else {
                            it->fraction = new_veg_fraction[veg_index];
                            ++it;
                        }
                    }
                    //append new record if not exit
                    std::list<int> new_rot = {1832, 3001, 3002, 3003, 4001,
                                              4002, 4003, 5701};
                    std::list<int>::iterator rot_it;
                    for (rot_it = new_rot.begin(); rot_it != new_rot.end();
                         ++rot_it) {
                        int veg_index = veg_type_list[*rot_it];
                        if (new_veg_fraction[veg_index] > 0) {
                            bool find = false;
                            for (it = vicveg.begin(); it != vicveg.end(); ++it) {
                                if (it->veg_code == *rot_it) {
                                    find = true;
                                    break;
                                }
                            }
                            if (!find) {
                                Veg_paramater newveg;
                                newveg.veg_code = *rot_it;
                                newveg.fraction = new_veg_fraction[veg_index];
                                newveg.dep1 = 0.1;
                                newveg.f1   = 0.1;
                                newveg.dep2 = 0.75;
                                newveg.f2   = 0.6;
                                newveg.dep3 = 0.5;
                                newveg.f3   = 0.3;
                                vicveg.push_back(newveg);
                            }
                        }
                    }
                    outf << gridid << " " << vicveg.size() << std::endl;
                    for (it = vicveg.begin(); it != vicveg.end(); ++it) {
                        outf <<  "   " << it->veg_code      << " "
                                       << it->fraction      << " "
                                       << it->dep1          << " "
                                       << it->f1            << " "
                                       << it->dep2          << " "
                                       << it->f2            << " "
                                       << it->dep3          << " "
                                       << it->f3
                                       << std::endl;
#ifdef PRINT_SUM_FRACTION
                        total_fraction_print[veg_type_list[it->veg_code]] +=
                            it->fraction;
#endif
                    }
                    delete[] veg_fraction;
                    delete[] new_veg_fraction;
                } else {
                    std::cerr << "Veg parameter file not right!\n";
                    exit(0);
                }
        } //if
    } //while
    orig_vic_veg.close();
    outf.close();
    if (argc == 4) delete[] cdl_area_list;
    std::clog << "Finished!\n";
#ifdef PRINT_SUM_FRACTION
    std::ofstream outfraction("total_fraction.txt");
    for (int i = 0; i < NUM_VEG; i++) {
        std::map<int,int>::iterator it;
        for (it = veg_type_list.begin(); it != veg_type_list.end(); ++it ) {
            if (it->second == i) {
                outfraction << it->first << "\t" << total_fraction_print[i]
                    << std::endl;
            }
        }
    }
    outfraction.close();
#endif
    return 0;
}
//______________________________________________________________________________
bool is_veg_exist_in_cdl(const CDL_areas *cdl, const int gid,
                             const std::string c_name)
{   //gid: gridid index in cdl data list
    if (gid == -1) {
        return false;
    } else {
        if      (c_name == "corn")          return cdl[gid].corn > 0;
        else if (c_name == "sweet_corn")    return cdl[gid].sweet_corn > 0;
        else if (c_name == "barley")        return cdl[gid].barley > 0;
        else if (c_name == "spring_wheat")  return cdl[gid].spring_wheat > 0;
        else if (c_name == "winter_wheat")  return cdl[gid].winter_wheat > 0;
        else if (c_name == "canola")        return cdl[gid].canola > 0;
        else if (c_name == "alfafa")        return cdl[gid].alfafa > 0;
        else if (c_name == "sugar_beet")    return cdl[gid].sugar_beet > 0;
        else if (c_name == "dry_bean")      return cdl[gid].dry_bean > 0;
        else if (c_name == "potato")        return cdl[gid].potato > 0;
        else return false;
    }
}
