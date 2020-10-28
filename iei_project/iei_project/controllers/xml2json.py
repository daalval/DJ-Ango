import json
import xmltodict

def xml_parser(xml_file, json_file):
    """Parser from XML to JSON / IEI"""
    with open(xml_file) as xml_f: 
        data_dict = xmltodict.parse(xml_f.read()) 
        xml_f.close() 
      
    json_data = json.dumps(data_dict) 
    print(json_data)
      
    with open(json_file, "w") as json_file_opened: 
        json_file_opened.write(json_data) 
        json_file_opened.close()

def main():
    """
    Main IEI parser
    """
    xml_parser("../../static/dblp-pruebas.xml", "../../static/dblp.json")


if __name__ == "__main__":
    main()

