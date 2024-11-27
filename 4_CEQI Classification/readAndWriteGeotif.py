"""
Created on 2024-11-27

@author: Baoshi He


This script is used to retrieve TIFF information and output TIFF data.
"""


from osgeo import gdal
import numpy as np
import os

def get_tif_information(file_path):
    dataset = gdal.Open(file_path) 

    if dataset is None:
        print(f'Unable to open {file_path.rsplit(".")[0]}.tif')

    im_width = dataset.RasterXSize             
    im_height = dataset.RasterYSize                  
    im_bands = dataset.RasterCount                  
    im_geotrans = dataset.GetGeoTransform()    
    im_proj = dataset.GetProjection()        
    nodatavalue = dataset.GetRasterBand(1).GetNoDataValue()


    im_data = dataset.ReadAsArray()

    print("-"*100)

    print(f'{file_path.rsplit(".")[0]}的栅格波段数总共有：', im_bands)
    print(f'{file_path.rsplit(".")[0]}的栅格仿射矩阵信息：', im_geotrans)
    print(f'{file_path.rsplit(".")[0]}的栅格投影：', im_proj)
    print(f'{file_path.rsplit(".")[0]}的栅格行列信息：', im_data.shape)
    print(f'{file_path.rsplit(".")[0]}的NoDataValue：', nodatavalue)
    print("-"*100)

    del dataset
        
    return im_width,im_height,im_bands,im_geotrans,im_proj,im_data , nodatavalue



def get_tif_information3(file_path):
    dataset = gdal.Open(file_path)  

    if dataset is None:
        print(f'Unable to open {file_path.rsplit(".")[0]}.tif')

    im_width = dataset.RasterXSize            
    im_height = dataset.RasterYSize                
    # im_bands = dataset.RasterCount               
    im_geotrans = dataset.GetGeoTransform()   
    im_proj = dataset.GetProjection()          



    print("-"*100)
    print(f'{file_path.rsplit(".")[0]}的栅格行列信息：', (im_height , im_width))
    print("-"*100)

    del dataset
        
    return im_width , im_height  , im_geotrans, im_proj




def array_to_tif2(name , mat , im_geotrans ,im_proj , nodata_value): 

    dtype_name = mat.dtype.name
    if 'uint8' == dtype_name:
        datatype = gdal.GDT_Byte
    elif 'int8' == dtype_name:
        datatype = gdal.GDT_Int16
    elif 'int16' == dtype_name:
        datatype = gdal.GDT_Int16
    elif 'uint16' == dtype_name:
        datatype = gdal.GDT_UInt16
    elif 'int32' == dtype_name:
        datatype = gdal.GDT_Int32
    elif 'uint32' == dtype_name:
        datatype = gdal.GDT_UInt32
    elif 'float64' == dtype_name:
        datatype = gdal.GDT_Float64
    else:
        datatype = gdal.GDT_Float32


    if len(mat.shape) == 3:
        im_bands, im_height, im_width = mat.shape
    else:
        im_bands, (im_height, im_width) = 1, mat.shape

    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(f"{name}.tif", im_width, im_height, im_bands, datatype , options=["COMPRESS=LZW"])
    dataset.SetGeoTransform(im_geotrans) 
    dataset.SetProjection(im_proj) 
    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(mat) 
        dataset.GetRasterBand(1).SetNoDataValue(nodata_value)
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i+1).WriteArray(mat[i])
            dataset.GetRasterBand(i+1).SetNoDataValue(nodata_value[i])
    del dataset



def array_to_tif(name , mat , im_geotrans ,im_proj):  

    dtype_name = mat.dtype.name
    if 'uint8' == dtype_name:
        datatype = gdal.GDT_Byte
    elif 'int16' == dtype_name:
        datatype = gdal.GDT_Int16
    elif 'uint16' == dtype_name:
        datatype = gdal.GDT_UInt16
    elif 'int32' == dtype_name:
        datatype = gdal.GDT_Int32
    elif 'uint32' == dtype_name:
        datatype = gdal.GDT_UInt32
    elif 'float64' == dtype_name:
        datatype = gdal.GDT_Float64
    else:
        datatype = gdal.GDT_Float32



    if len(mat.shape) == 3:
        im_bands, im_height, im_width = mat.shape
    else:
        im_bands, (im_height, im_width) = 1, mat.shape

    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(f"{name}.tif", im_width, im_height, im_bands, datatype)
    dataset.SetGeoTransform(im_geotrans) 
    dataset.SetProjection(im_proj) 
    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(mat) 
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i+1).WriteArray(mat[i])
    del dataset



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


