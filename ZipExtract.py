import zipfile
import os

zipfiles = [f for f in os.listdir('./') if zipfile.is_zipfile(f)];
for file in zipfiles:
    fileDirectory = './{0}'.format(file)
    newzip = zipfile.ZipFile(fileDirectory)
    originalName = newzip.namelist()[0]
    print('Extracting {0}'.format(file))
    newzip.extractall('./ExtractedZips')
    newzip.close()
    if (re.search(r"zip$",file) is not None):
        os.rename('./ExtractedZips/{0}'.format(originalName),'./ExtractedZips/{0}'.format(file[0:-4]))
    else:
        os.rename('./ExtractedZips/{0}'.format(originalName),'./ExtractedZips/{0}'.format(file))
    os.remove(fileDirectory);

