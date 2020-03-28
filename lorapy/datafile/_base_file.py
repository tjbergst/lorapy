# base datfile class

import pathlib



class BaseDatFile:

    def __init__(self, file_path: pathlib.Path):

        self.file_path = file_path



    def __repr__(self):
        return self.name



    @property
    def name(self) -> str:
        return self.file_path.name

