"""
Created on 2024-11-27

@author: Baoshi He


This script is used to calculate the Complete ecological resilience index
"""


from readAndWriteGeotif import *
import numpy as np
# import dask.array as da
import numpy.ma as ma



if __name__ == "__main__":

    # year = 2000
    year = 2020

    shdi = r"E:\Desktop\中国滨海湿地数据集\output\中国滨海湿地_diversity_{}.tif".format(year)
    tif_data = r"E:\Desktop\中国滨海湿地数据集\output\中国滨海湿地_生态弹性限度0_{}.tif".format(year)

    im_width_shdi,im_height_shdi,im_bands_shdi,im_geotrans_shdi,im_proj_shdi,im_data_shdi, nodatavalue_shdi = get_tif_information(shdi)

    im_width_tif_data,im_height_tif_data,im_bands_tif_data,im_geotrans_tif_data,im_proj_tif_data,im_data_tif_data, nodatavalue_tif_data = get_tif_information(tif_data)


    if im_data_shdi.shape == im_data_tif_data.shape:

        print("行列号一致，开始计算...........................................")

        output_type = np.uint32
        setNodataValue = np.iinfo(output_type).max

        mask_shdi = (im_data_shdi == nodatavalue_shdi)
        maksed_im_data_shdi = ma.masked_array(data = im_data_shdi , mask = mask_shdi)

        del im_data_shdi , mask_shdi

        mask_tif_data = (im_data_tif_data == nodatavalue_tif_data)
        maksed_im_data_tif = ma.masked_array(data = im_data_tif_data , mask = mask_tif_data)

        del im_data_tif_data , mask_tif_data
        maksed_im_data_tif = (maksed_im_data_tif / 1000).astype(np.uint32)  

        im_new = (maksed_im_data_shdi * maksed_im_data_tif).filled(setNodataValue)
        # print(im_new.dtype)


        # output tif
        name = r"E:\Desktop\中国滨海湿地数据集\output\中国滨海湿地_生态弹性限度1_{}.tif".format(year)
        mat = im_new

        im_geotrans =  im_geotrans_shdi
        im_proj = im_proj_shdi

        array_to_tif2(name  , mat , im_geotrans ,im_proj , nodata_value = setNodataValue)

    else:
        print("行列号不一致，请检查并重新输入xxxxxxxxxxxxx")