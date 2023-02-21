import unittest
import os

class TestlistFilesInDirectory(unittest.TestCase):
    
    def test_list_files_in_directory(self):
        file_path = os.listdir(os.getcwd()+"/" + "filesToProcess")
        self.assertListEqual(file_path, os.listdir(os.getcwd() + "/" + "filesToProcess"))  
        
    def test_directory_exist(self):
        file_path = os.listdir(os.getcwd() + "/" + "filesToProcess")
        self.assertTrue(file_path)

if __name__ == "__main__":
    unittest.main()