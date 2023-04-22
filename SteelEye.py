import wget
from zipfile import ZipFile
import csv
from lxml import etree as ET
import logging
import os
import unittest

logging.basicConfig(filename='steeleye.log', level=logging.INFO)
"""
    Downloads a zip file from a URL and extracts its contents.

"""
url = 'http://firds.esma.europa.eu/firds/DLTINS_20210117_01of01.zip'
wget.download(url)
logging.info("Successfully download!!")

# open te zip file in read mode
with ZipFile('DLTINS_20210117_01of01.zip', 'r') as zip:
    zip.printdir()
    logging.info("Extracting all the files now...")
    zip.extractall()
    logging.info("Done!")
"""
    Parses an XML file and writes its data to a CSV file.

"""

try:
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp',
                             'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr'])
        tree = ET.parse('DLTINS_20210117_01of01.xml')
        root = tree.getroot()
        namespaces = {
                'a': 'urn:iso:std:iso:20022:tech:xsd:auth.036.001.02'}
        elements = root.findall('.//a:FinInstrmGnlAttrbts', namespaces)
        for element in elements:
            id = element.find('a:Id', namespaces)
            full_nm = element.find('a:FullNm', namespaces)
            Clssfctn_tp = element.find('a:ClssfctnTp', namespaces)
            cmmdty_deriv_ind = element.find('a:CmmdtyDerivInd', namespaces)
            ntnl_ccy = element.find('a:NtnlCcy', namespaces)
            if id is not None and id.text:
                id_element = id.text.strip()
            if full_nm is not None and full_nm.text:
                full_nm_element = full_nm.text.strip()
            if Clssfctn_tp is not None and Clssfctn_tp.text:
                Clssfctn_tp_element = Clssfctn_tp.text.strip()
            if cmmdty_deriv_ind is not None and cmmdty_deriv_ind.text:
                cmmdty_deriv_ind_element = cmmdty_deriv_ind.text.strip()
            if ntnl_ccy is not None and ntnl_ccy.text:
                ntnl_ccy_element = ntnl_ccy.text.strip()

        # Find Issr tag outside of FinInstrmGnlAttrbts elements and write its value to csv file
        for issr_elem in root.findall('.//a:Issr', namespaces):
            if issr_elem is not None and issr_elem.text:
                issr = issr_elem.text.strip()
            writer.writerow([id_element, full_nm_element, Clssfctn_tp_element,
                                 cmmdty_deriv_ind_element, ntnl_ccy_element, issr])
except Exception as e:
    logging.error("An error occurred while parsing XML file: " + str(e))

"""
Testing the working of code

Args:
predefined unit test case

Return:
None
"""

class TestXMLParsing(unittest.TestCase):

    def test_file_download(self):
        # Check if the file exists
        try:
            self.assertTrue(os.path.exists('DLTINS_20210117_01of01.zip'))
            logging.info("Checked the file is downloaded..")
        except AssertionError:
            logging.error("The zip file does not exist")
        except Exception as e:
            logging.error(
                "An error occurred while testing file download: " + str(e))

    def test_file_extraction(self):
        # Check if the extracted files exist
        try:
            self.assertTrue(os.path.exists('DLTINS_20210117_01of01.xml'))
            logging.info("Checked the file is extracted..")
        except AssertionError:
            logging.error("The xml file does not exist")
        except Exception as e:
            logging.error(
                "An error occurred while testing file extraction: " + str(e))

    def test_csv_file_creation(self):
        # Check if the CSV file has been created
        try:
            self.assertTrue(os.path.exists('output.csv'))
            logging.info("Checked the output file created..")
        except AssertionError:
            logging.error("The output.csv file does not exist")
        except Exception as e:
            logging.error(
                "An error occurred while testing CSV file creation: " + str(e))

    def test_null_value(self):
        # Check if the CSV file has data
        try:
            with open('output.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # Skip the header row
                next(reader)
                # Check if there is at least one row of data
                self.assertIsNotNone(next(reader, None))
                logging.info("Checked the data is stored in output.csv")
        except AssertionError:
            logging.error("The output.csv file does not have any data")
        except Exception as e:
            logging.error(
                "An error occurred while testing CSV file data: " + str(e))


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
