import os
import fnmatch



def get_filepaths(folder_path , suffix = ".tif"):

    files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(suffix)]

    return files


def get_file_path(floder_path , suffix = ".tif"): 
    file_list = []
    for file_path,sub_dirs1,files in os.walk(floder_path):
        # print(file_path,sub_dirs1,files)
        # print("-"*60)
        for file in files:
            # print(file)
            if file.endswith(suffix):
                tif_full_path = file_path + '\\' + file
                # tif_full_path = os.path.join(file_path , file)    
                # print(tif_full_path)
                file_list.append(tif_full_path)
    return file_list




def get_file_path_withPattern(floder_path , suffix = ".tif" , pattern = 'GLC_FCS30D_20002022_*_Annual.tif'): 
    file_list = []
    for file_path,sub_dirs1,files in os.walk(floder_path):
        # print(file_path,sub_dirs1,files)
        # print("-"*60)
        for file in files:
            # print(file)
            if file.endswith(suffix):

                if fnmatch.fnmatch(file , pattern):
                    tif_full_path = file_path + '\\' + file
                    # tif_full_path = os.path.join(file_path , file)    
                    # print(tif_full_path)
                    file_list.append(tif_full_path)
    return file_list


def add_mask_to_filename(filename , text = "_掩膜"):
    base_name, extension = os.path.splitext(filename)
    new_filename = f"{base_name}{text}{extension}"
    return new_filename







