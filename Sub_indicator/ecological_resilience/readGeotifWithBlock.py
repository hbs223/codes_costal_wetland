from osgeo import gdal
from tqdm import tqdm




def process_block_size(shape , block_list):

    block_row = block_list[0]
    block_col = block_list[1]
    
    block_size_row = int(shape[0] / block_row) + 1
    block_size_col = int(shape[1] / block_col) + 1
    block_size = (block_size_row , block_size_col)

    return block_size



def get_tif_subsetData(file_path , x_offset, y_offset, x_size_subset, y_size_subset):
    dataset = gdal.Open(file_path) 
    if dataset is None:
        print(f'Unable to open {file_path.rsplit(".")[0]}.tif')


    band = dataset.GetRasterBand(1)

    subset_im_data = band.ReadAsArray(x_offset, y_offset, x_size_subset, y_size_subset)

    nodatavalue = dataset.GetRasterBand(1).GetNoDataValue()

    
    print("-"*100)
    print(f'{file_path.rsplit(".")[0]}的栅格子集行列信息：', subset_im_data.shape)
    print(f'{file_path.rsplit(".")[0]}的NoDataValue：', nodatavalue)
    print("-"*100)

    del dataset
    
    return subset_im_data , nodatavalue


















