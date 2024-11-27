"""
Created on 2024-11-27

@author: Baoshi He


Align the row and column numbers of the influencing factor TIFF data.
"""


import arcpy
# from arcpy import env
from arcpy.sa import *
import os
import json



def he_outExtractByMask_withEnvironment(tif_path, geometry , output_tif_path):
    

    desc = arcpy.Describe(geometry)
    cell_size = (desc.meanCellWidth, desc.meanCellHeight)
    # print(cell_size)
    spatial_ref = desc.spatialReference


    arcpy.env.outputCoordinateSystem = spatial_ref
    arcpy.env.cellSize = cell_size[0]
    arcpy.env.snapRaster = geometry  

    arcpy.env.extent = desc.extent


    if os.path.exists(output_tif_path):
        os.remove(output_tif_path)
        print("{} file removed.".format(output_tif_path))

    try:

        outExtractByMask = arcpy.sa.ExtractByMask(tif_path, geometry)          
        outExtractByMask.save(output_tif_path)                      
        print(f"已掩膜至：{output_tif_path}")              


    except:
        text = f"{tif_path}执行ExtractByMask失败"
        print(text)



def add_mask_to_filename(filename , text = "_掩膜"):
    base_name, extension = os.path.splitext(filename)
    new_filename = f"{base_name}{text}{extension}"
    return new_filename




if __name__ == '__main__':
   
    # Mask

    geometry_path = r"E:\Desktop\Python改变地球\A中国滨海湿地生态质量评估\0三年的湿地范围\output\200020102020中国滨海湿地区域.tif"

    input_floder_path = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\影响因素_纯净"
    output_floder_path = r"E:\Desktop\滨海湿地生态质量评估指标与任务进程\影响因素_行列号对齐"

    for file_path,sub_dirs1,files in os.walk(input_floder_path):

        # print(file_path,sub_dirs1,files)
        # print("-"*60)
        for file in files:
            # print(file)
            if file.endswith("tif"):
                up_folder = file_path.rsplit("\\" , 1)[1]

                new_filename = add_mask_to_filename(filename = file , text = "_湿地范围掩膜")

                tif_full_path = file_path + '\\' + file

                output_tif_path = os.path.join(output_floder_path , up_folder , new_filename)

                print(f"正在掩膜至{output_tif_path}...........................................")
                he_outExtractByMask_withEnvironment(tif_path = tif_full_path, geometry = geometry_path , output_tif_path = output_tif_path)
                print(f"{output_tif_path} ----------------------> successfully!")






