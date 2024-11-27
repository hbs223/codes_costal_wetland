
from tqdm import tqdm
import numpy as np




def convert_arr_from_float2int(sub_im_arrays , enlargement_factor = 10000 , convert_type = np.int16):

    min_int = np.iinfo(convert_type).min
    max_int = np.iinfo(convert_type).max

    error_num = 0

    with tqdm(total=len(sub_im_arrays) , desc="Processing", unit="iteration") as pbar:
        for memory_block in sub_im_arrays:

            for cpu_index , cpu_block in enumerate(memory_block):


                if np.isnan(cpu_block).all():     

                    cpu_block[np.isnan(cpu_block)] = max_int

                    memory_block[cpu_index] = cpu_block.astype(convert_type)

                else:                     
                    cpu_block = cpu_block * enlargement_factor


                    min_vlaue = np.nanmin(cpu_block)
                    max_value = np.nanmax(cpu_block)


                    if min_vlaue >= min_int and max_value <= max_int:
                        # print("can be transformed............")

                        cpu_block[np.isnan(cpu_block)] = max_int
                        memory_block[cpu_index] = cpu_block.astype(convert_type)

                    else:
                        error_num += 1
                        print("error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            pbar.update(1)
            

    print("存在转换错误数组个数:",error_num)
    print("--------------------------数组转为int完毕！--------------------------------")
    
