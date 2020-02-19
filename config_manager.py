from yaml import load, dump, FullLoader


def create_base_yaml():
    """creates the yaml file from the predefined dictionary below"""
    my_yaml = \
        {"groups": [
            {"number": 1,
             "degrees": 100,
             "mac": "dc-4f-22-19-a5-ff"},
            {"number": 2,
             "degrees": 100,
             "mac": "b4-e6-2d-37-22-b8"},
            {"number": 3,
             "degrees": 100,
             "mac": "dc-4f-22-18-de-d6"},
            {"number": 4,
             "degrees": 100,
             "mac": "b4-e6-2d-37-34-8e"},
            {"number": 5,
             "degrees": 100,
             "mac": "dc-4f-22-18-d7-ae"},
            {"number": 6,
             "degrees": 100,
             "mac": "b4-e6-2d-37-39-ca"},
            {"number": 7,
             "degrees": 100,
             "mac": "68-c6-3a-d5-36-71"},
            {"number": 8,
             "degrees": 100,
             "mac": "b4-e6-2d-37-16-77"},
            {"number": 9,
             "degrees": 100,
             "mac": "b4-e6-2d-37-3e-03"},
            {"number": 10,
             "degrees": 100,
             "mac": "b4-e6-2d-37-42-29"},
            {"number": 11,
             "degrees": 100,
             "mac": "b4-e6-2d-37-38-36"},
            {"number": 12,
             "degrees": 100,
             "mac": "dc-4f-22-19-a0-54"},
            {"number": 13,
             "degrees": 100,
             "mac": "dc-4f-22-19-a7-63"},
            {"number": 14,
             "degrees": 100,
             "mac": "b4-e6-2d-37-12-a7"},
            {"number": 15,
             "degrees": 100,
             "mac": "b4-e6-2d-37-3f-e9"},
            {"number": 16,
             "degrees": 100,
             "mac": "dc-4f-22-18-d0-b3"},
            {"number": 17,
             "degrees": 100,
             "mac": "dc-4f-22-18-f6-4d"},
            {"number": 18,
             "degrees": 100,
             "mac": "de-ad-be-ef-00-01"},
            {"number": 19,
             "degrees": 100,
             "mac": "de-ad-be-ef-00-02"},
            {"number": 20,
             "degrees": 100,
             "mac": "de-ad-be-ef-00-03"},
        ],
            "serial1": "COM3",
            "serial2": "COM4",
            "subnet_ip": "192.168.1.",
            "base_ip": 0,
            "dynamic_ip": 100,
            "groups_number": 20
        }
    stream = open('configuration.yaml', 'w')
    dump(my_yaml, stream)
    stream.close()


class ConfigManager:
    """Reads yaml file and serves as an API for its' content"""

    def __init__(self):
        self.loaded_dictionary = {}
        self.reload_yaml()

    def get_item(self, item_name):
        return self.loaded_dictionary[item_name]

    def get_group_degrees(self, group_number):
        for group in self.loaded_dictionary["groups"]:
            if group["number"] == group_number:
                return group["degrees"]
        return 100

    def get_group_mac_address(self, group_number):
        for group in self.loaded_dictionary["groups"]:
            if group["number"] == group_number:
                return group["mac"]
        return ''

    def reload_yaml(self):
        stream = open('configuration.yaml', 'r')
        self.loaded_dictionary = load(stream, Loader=FullLoader)
        stream.close()


if __name__ == "__main__":
    create_base_yaml()
    config = ConfigManager()
    print(config.get_item("groups_number"))