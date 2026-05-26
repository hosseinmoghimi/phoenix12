import shutil
import os
from phoenix.settings import BASE_DIR
class Compress():
    def __init__(self,*args, **kwargs):
        output_folder=None
        self.get_output_archive=None
        output_file_name="archive"
        compress_file_type='zip'
        if 'output_file_name' in kwargs and kwargs['output_file_name'] is not None:
            output_file_name=kwargs['output_file_name']
        if 'compress_file_type' in kwargs and kwargs['compress_file_type'] is not None:
            compress_file_type=kwargs['compress_file_type']
        if 'output_folder' in kwargs and kwargs['output_folder'] is not None:
            output_folder=kwargs['output_folder']
        if 'folder' in kwargs and kwargs['folder'] is not None:
            folder=kwargs['folder']
        output_folder=os.path.join(output_folder,output_file_name)
        a=shutil.make_archive(output_folder, compress_file_type, folder)
    
        self.get_output_archive=str(a)