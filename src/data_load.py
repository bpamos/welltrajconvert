import json

class DataLoader:
    """
    Get information about a directional survey from dict
    reformat into directional survey obj
    """

    def __init__(self, json_path):
        """

        """

        self.json_path = json_path

    def read_json(self):
        """Function to read in data from a txt file or list. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.
        If list, the list should be all floats

        Args:
            data_name (string) or (list): if string it is the name of a file to read from
            if list, it is the list name
        Returns:
            None
        """

        with open(self) as json_file:
            data = json.load(json_file)
        json_file.close()

        self.data

        return data