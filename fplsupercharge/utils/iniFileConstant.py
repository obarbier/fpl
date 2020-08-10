FILE_NAME = "FPLSUPERCHARGE.ini"
TEMP_FILE_DIR = "./tmp"
SAVE_TEMPLATE = "{}/{{}}".format(TEMP_FILE_DIR)

TEMP_CREATION_MESSAGE_FAILED = "Creation of the directory {} failed".format(
    TEMP_FILE_DIR)
TEMP_CREATION_MESSAGE_SUCCESS = "Sucessfully Created the directory {}".format(
    TEMP_FILE_DIR)

TEMP_DELETE_MESSAGE_FAILED = "deletion of the directory {} failed".format(
    TEMP_FILE_DIR)
TEMP_DELETE_MESSAGE_SUCCESS = "Sucessfully delete the directory {}".format(
    TEMP_FILE_DIR)

INI_CREATION_MESSAGE_SUCCESS = "Sucessfully Created the file {}".format(
    FILE_NAME)

SECTION = {1: "INITILIAZATION", 2: "COOKIES::{DOMAIN}", 3: "DB", 4: "JOB-INFO"}
