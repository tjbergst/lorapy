# base datfile class

import pathlib



class BaseDatFile:

    def __init__(self, file_path: pathlib.Path):

        self.file_path = file_path



    def __repr__(self):
        return self.name
        # TODO: note, can add more params like bw, sf, etc but would require a .load()



    @property
    def name(self) -> str:
        return self.file_path.name

