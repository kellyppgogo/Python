import sys

sys.path.append("../..")
print(sys.path)

file_name = "bondInfomation.xls"
properties_dict = {}


def __init__():
    from intelligence.util.Util import Properties
    global properties_dict
    properties_dict = Properties("../config/bond_info_config").getProperties()


__init__()
print(properties_dict.get("output_path"))