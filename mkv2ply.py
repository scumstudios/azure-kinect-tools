#!/usr/bin/python3

import os
import open3d as o3d
import numpy as np

#get recordings path ## TODO: Fix TRAILING slash detection

rec_path = input("Recording Directory: ")

depth_trunc = float(input("Depth Truncation in Meters (0 to Disable): "))
voxel_size = float(input("Initial Voxel Downsample in Meters (0 to Disable): "))
point_output = float(input("Fixed Point Output (0 to Disable): "))

pc_path = input("Point Cloud Output Directory: ")


#Define conversion function:
def pc_gen(video):

    #create MKVReader class
    reader = o3d.io.AzureKinectMKVReader()

    #print(reader)
    print("Processing: " + video)

    #Load in MKV file
    reader.open(rec_path + video)

    #Read metadata and write to json
    meta = reader.get_metadata()
    o3d.io.write_azure_kinect_mkv_metadata("/tmp/" + video + ".json", meta)

    i = 0
    j = 0

    #Read next frame and extract RGBD
    reader.seek_timestamp(1000000)

    #Extract MKV Frames and create plys
    #for x in range(10):
    while reader.is_eof != True:

        #Read next frame and extract RGBD
        frame = reader.next_frame()

        #Move on to next file if three consecutive frames can't be read 
        if frame == None:
            j += 1

            print("EMPTY FRAME " + str(j))
            
            i += 1

            if j > 2:
                break

        
        else: 

            i += 1

            #Create O3D Images
            rgb = o3d.geometry.Image(np.asarray(frame.color))
            depth = o3d.geometry.Image(np.asarray(frame.depth))

            #Combine Channels in to O3D RDGBImage and set correct depth
            if depth_trunc == 0:
                depth_fix = 1000
            else:
                depth_fix = depth_trunc

            rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(rgb, depth, depth_scale=1000, depth_trunc=depth_fix, convert_rgb_to_intensity=False)

            #Read generated intrinsic
            cam = o3d.io.read_pinhole_camera_intrinsic("/tmp/" + video + ".json")

            #Create point cloud
            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, cam)
            
            #Voxel downsample point cloud before filtering for better perfomance
            if voxel_size != 0:
                pcd = pcd.voxel_down_sample(voxel_size)

            #Filter point cloud outliers
            pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=16, std_ratio=0.75, print_progress=False)

            #Check if fixed amount downsampling is enabled
            if point_output != 0:
            
                #Check to see if point cloud has less points than final output
                point_fix = int(point_output)

                if len(pcd.points) < point_fix:
                    break
                else:
                    pcd = pcd.farthest_point_down_sample(point_fix)

        #Write point cloud to ply
        o3d.io.write_point_cloud(pc_path + str(video).rstrip(".mkv") + "_" + str(i).zfill(4) +".ply", pcd, compressed=True)

### SERIAL PROCESSING ###

for video in os.listdir(rec_path):
    if str(video.endswith('.mkv')):
        pc_gen(video)




### PARALLEL PROCESSING RANDOM ###

# videos = os.listdir(rec_path)

# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# with ThreadPoolExecutor() as executor:
#     results = executor.map(pc_gen, [video for video in videos])

### PARALLEL PROCESSING ###

# videos = os.listdir(rec_path)

# from multiprocessing import Process

# p = Process(target=pc_gen, args=[video for video in videos])
# p.start()
# p.join()


#####


# import threading

# videos = os.listdir(rec_path)

# for v in videos:
#     t=threading.Thread(target=pc_gen, args=(v, ))
#     t.start()


#######


# thread_list = []

# for video in videos:
#     t = threading.Thread(target=pc_gen, args=video)
#     thread_list.append(t)

# for thread in thread_list:
#     thread.start()

# for thread in thread_list:
#     thread.join()