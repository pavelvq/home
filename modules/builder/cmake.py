import getpass
import os, sys


class Cmake():
    CURRENT = {
            "SOURCE_FOLDER": None,
            "BUILD_FOLDER": None,
            "OUTPUT_NAME": None,
            "OUTPUT_SUFFIX": None,
            "TMP_FOLDER_NAME": None,
            "CLEAR_TMP": None
        }

    def cmake(self, source_folder=".", build_folder=".", output_name="output", output_suffix="exe", tmp_folder_name=".tmp", clear_tmp=True):
        self.CURRENT = {
            "SOURCE_FOLDER": source_folder,
            "BUILD_FOLDER": build_folder,
            "OUTPUT_NAME": output_name,
            "OUTPUT_SUFFIX": output_suffix,
            "TMP_FOLDER_NAME": tmp_folder_name,
            "CLEAR_TMP": clear_tmp
        }
        
    def _clearcurrent(self):
        self.CURRENT = {
                "SOURCE_FOLDER": None,
                "BUILD_FOLDER": None,
                "OUTPUT_NAME": None,
                "OUTPUT_SUFFIX": None,
                "TMP_FOLDER_NAME": None,
                "CLEAR_TMP": None
            }