import sqlite3, os, csv, glob

#
# finds all necessary .tif images from current working directory
#
files = []
for file in glob.glob("*.tif"):
    files.append(file)

count_files = len(files)

#
# data to be imported
#

for file in files:                          # iterates through all images and creates separate datasets

    file_name = file.strip(".tif")
    database = ("{}.sqlite".format(file_name))
    conn = sqlite3.connect(database)
    curs = conn.cursor()

#
# setting up metadata
#
    curs.execute("SELECT InitSpatialMetadata()")
    curs.fetchall()

#
# loading raster data from objects
#
    os.system("rasterlite_load -d {}.sqlite -T {} -D . -t".format(file_name,file_name))
    os.system("rasterlite_load -d {}.sqlite -T {} -D . -v".format(file_name,file_name))

    curs.execute("SELECT tbl_name FROM sqlite_master WHERE type='table';")
    tables = curs.fetchall()

    os.system("mkdir {}_files".format(file_name))

#
# generating CSVs
#
    for i in tables:
        print('Creating CSV for: ',i[0])
        curs.execute("SELECT * FROM {};".format(i[0]))
        ex = curs.fetchall()
        for row in ex :
            list = []
            for j in row:
                value = str(j)
                list.append(value)
            file_data = open('.{}_files/{}.csv'.format(file_name,i[0]), 'a')
            ex = csv.writer(file_data)
            ex.writerow(list)
