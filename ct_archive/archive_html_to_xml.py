## archive xml to HTML ##

# function that takes in an HTML page and returns a dictionary with
# before xml, after xml, id name, and file_date

from bs4 import BeautifulSoup
import glob
import re
import os

''' takes an html file, outputs a dictionary '''
def archive_to_xml(html_file):

    xml_name = str(html_file).replace('.html','').replace('./ct_changes/', '')
    id_name = re.search('NCT[0-9]{8}', xml_name).group(0)
    file_date = re.search('[0-9]{4}_[0-9]{2}_[0-9]{2}', xml_name).group(0).replace('_', '')

    # get the content of the html input file
    soup = BeautifulSoup(open(html_file))

    # the id that contains all xml
    sdiff_full = soup.find(id="sdiff-full")

    # and these are the <tr> tags in that object with the xml we want
    sdiff_xml = sdiff_full.find_all("tr", {"class" : 
                                    ["sdiff-unc", "sdiff-add","sdiff-chg"]})

    before_changed_date = sdiff_full.find("a").text.replace('(Updated ', '').replace(')', '').replace('_','')

    ### td class sdiff-a: all of the "before" xml ###
    all_before = []
    for result in sdiff_xml:
        all_before.append(result.find("td", {"class" : "sdiff-a"}))

     # td class sdiff-b: all of the "after" xml
    all_after = []
    for result in sdiff_xml:
        all_after.append(result.find("td", {"class" : "sdiff-b"}))

    before_after_xml  = {}
    before_after_xml['before_xml'] = all_before[0].text
    before_after_xml['after_xml'] = all_after[0].text
    before_after_xml['id_name'] = id_name
    before_after_xml['file_date'] = file_date
    before_after_xml['before_changed_date'] = before_changed_date

    return before_after_xml

def write_after_xml_file(output_directory, xml_dict):
    file_name = xml_dict['id_name'] + '_' + xml_dict['file_date'] 

    print "ID name is: " + xml_dict['id_name']
    print "date is: " + xml_dict['file_date']
    with open(output_directory + file_name + '.xml', 'w') as filepath:
        filepath.write('{0}'.format(xml_dict['after_xml']))

def write_before_xml_file(output_directory, xml_dict):
    file_name = xml_dict['id_name'] + '_' + xml_dict['before_changed_date'] 

    with open(output_directory + file_name + '.xml', 'w') as filepath:
        filepath.write('{0}'.format(xml_dict['before_xml']))

    file_name2 = xml_dict['id_name'] + '_' + xml_dict['file_date']

    with open(output_directory + file_name2 + '.xml', 'w') as filepath:
        filepath.write('{0}'.format(xml_dict['after_xml']))

''' returns a list of directories in the archive -> changes directory '''
def get_directory_list(html_location):
    directory_names = os.walk(html_location).next()[1]
    return directory_names

''' saves XML files for each archive HTML change file '''
def get_archive_xml():
    archive_directories = get_directory_list('./ct_changes/')
    directory_of_html = './ct_changes/'
    directory_for_xml = './ct_changes_xml/'

    for directory in archive_directories:
        print "directory: " + directory
        if not os.path.exists(directory_for_xml + '/' + directory):
            os.makedirs(directory_for_xml + directory)

        # get a list of all HTML files in each HTML study directory
        html_files = glob.glob(directory_of_html + directory + '/*.html')

        before_dict = archive_to_xml(html_files[0])
        write_before_xml_file(directory_for_xml + before_dict['id_name'] + '/', before_dict)

        print len(html_files)
        # run get archive xml on each html file
        for html_file in html_files[1:]:
            after_dict = archive_to_xml(html_file)
            output_directory = directory_for_xml
            # takes a 
            write_after_xml_file(output_directory + 
                        after_dict['id_name'] + '/', after_dict)

# archive_to_xml('./ct_changes/NCT00000122/2005_06_30.html')
get_archive_xml()



