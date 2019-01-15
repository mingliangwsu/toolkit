import os
import dbf
rootdir = '/mnt/hydronas/Projects/BPA_CRB/GIS/VIC_basins'
os.chdir(rootdir)
outpath = '/home/liuming/temp/temp'
extensions = ('.dbf')

for subdir, dirs, files in os.walk(rootdir, topdown=True):
    dirs.clear()
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        filename = os.path.basename(file)
        base = filename.split('.')[0]
        fullpath_file = rootdir + '/' + filename
        #print(base + ':ext:' + ext + ':' + fullpath_file)
        print(base)
        if ext in extensions and len(ext) > 0:
            #print(base + ':' + fullpath_file)
            outfile = outpath + '/' + base + '.txt'
            testoutfile = outpath + '/test.txt'
            test = dbf.Table(fullpath_file)
            test.open()
            dbf.export(test, filename=testoutfile, format='csv', header=False)
            test.close()
            outf = open(outfile,"w")
            with open(testoutfile) as f:
                for line in f:
                    a = line.split(',')
                    if len(a[0]) > 4:
                        out = a[0].replace('"', '')
                        outf.write(out + '\n')
            outf.close()
                        #print(location + ':' + cellid)

