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

for video in os.listdir(rec_path):

    #create MKVReader class
    reader = o3d.io.AzureKinectMKVReader()

    #print(reader)
    print("Processing: " + video)

    #Load in MKV file
    reader.open(rec_path + video)

    #Read metadata and write to json
    meta = reader.get_metadata()
    o3d.io.write_azure_kinect_mkv_metadata("/tmp/intrinsic.json", meta)

    i = 1
    j = 0

    #Read next frame and extract RGBD
    reader.seek_timestamp(1000000)

    #Extract MKV Frames and create plys
    #for x in range(10):
    while reader.is_eof != True:

        #Read next frame and extract RGBD
        frame = reader.next_frame()

        #Move on to next file if no frames can be read 
        if frame == None:
            j += 1

            print("EMPTY FRAME " + str(j))
            
            i += 1

            if j > 5:
                break

        
        else: 

            #Create O3D Images
            rgb = o3d.geometry.Image(np.asarray(frame.color))
            depth = o3d.geometry.Image(np.asarray(frame.depth))

            #Combine Channels in to O3D RDGBImage and set correct depth
            if depth_trunc == 0:
                depth_trunc = 1000

            rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(rgb, depth, depth_scale=1000, depth_trunc=depth_trunc, convert_rgb_to_intensity=False)

            #Read generated intrinsic
            cam = o3d.io.read_pinhole_camera_intrinsic("/tmp/intrinsic.json")

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
                point_output = int(point_output)

                if len(pcd.points) < point_output:
                    break
                else:
                    pcd = pcd.farthest_point_down_sample(point_output)

                # #Write point cloud to ply
                o3d.io.write_point_cloud(pc_path + video + "_" + str(i).zfill(4) +".ply", pcd, compressed=True)

                i += 1

            else:

                #Write point cloud to ply
                o3d.io.write_point_cloud(pc_path + video + "_" + str(i).zfill(4) +".ply", pcd, compressed=True)

                i += 1