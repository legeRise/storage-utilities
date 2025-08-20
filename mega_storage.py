import os
from dotenv import load_dotenv
from mega import Mega

load_dotenv(override=True)


class MegaStorage:
    def __init__(self, email=None, password=None):
        self.email = email or os.getenv("MEGA_STORAGE_EMAIL") 
        self.password = password or os.getenv("MEGA_STORAGE_PASSWORD") 
        self.mega = Mega()
        self.m = self.mega.login(self.email, self.password)

    # ✅ Upload a file
    def upload_file(self, file_path, dest_folder=None):
        if dest_folder:
            folder_node = self.m.find(dest_folder)[0]
            file = self.m.upload(file_path, folder_node)
        else:
            file = self.m.upload(file_path)
        return self.m.get_upload_link(file)

    # ✅ Download a file by name (to local folder)
    def download_file(self, file_name, dest_path="."):
        file = self.m.find(file_name)[0]
        return self.m.download(file, dest_path)

    # ✅ Get a share/export link for a file or folder
    def get_link(self, name):
        node = self.m.find(name)[0]
        return self.m.export(node)

    # ✅ Delete a file or folder
    def delete(self, name):
        node = self.m.find(name)[0]
        return self.m.delete(node)

    # ✅ List all files (returns dict of id → metadata)
    def list_files(self):
        return self.m.get_files()

    # ✅ Create a new folder (supports nested paths like 'a/b/c')
    def create_folder(self, folder_path):
        return self.m.create_folder(folder_path)

    # ✅ Rename a file or folder
    def rename(self, old_name, new_name):
        node = self.m.find(old_name)[0]
        return self.m.rename(node, new_name)

    # ✅ Import from public URL into account
    def import_from_url(self, url, dest_folder=None):
        if dest_folder:
            folder_node = self.m.find(dest_folder)[0]
            return self.m.import_public_url(url, dest_node=folder_node)
        return self.m.import_public_url(url)

    # ✅ Get storage space info
    def get_storage(self, unit="MB"):
        if unit == "KB":
            return self.m.get_storage_space(kilo=True)
        elif unit == "MB":
            return self.m.get_storage_space(mega=True)
        elif unit == "GB":
            return self.m.get_storage_space(giga=True)
        return self.m.get_storage_space()


if __name__ == "__main__":
    mega_storage = MegaStorage()


    
