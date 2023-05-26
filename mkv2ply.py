#!/usr/bin/python

# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-p", "--path", type=str)

# args = parser.parse_args()

import os
import readline
import open3d as o3d
import cv2 as cv
import numpy as np

device_o3d = o3d.core.Device("cuda:0")

point_output = 25000

readline.parse_and_bind("tab: complete")

#get recordings path ## TODO: Fix TRAILING slash detection
#videopath = input("Path to Kinect recordings: ")
videopath = ("/mnt/data/00-RECORD/")

for video in os.listdir(videopath):

    #create MKVReader class
    reader = o3d.io.AzureKinectMKVReader()

    #print(reader)
    print("Processing: " + video)

    #Load in MKV file
    reader.open(videopath + video)

    #Read metadata and write to json
    meta = reader.get_metadata()
    o3d.io.write_azure_kinect_mkv_metadata("/tmp/intrinsic.json", meta)

    i = 1
    j = 0

    #Read next frame and extract RGBD
    reader.seek_timestamp(500000)

    #Extract MKV Frames and create plys
    #for x in range(10):
    while reader.is_eof != True:

        #Read next frame and extract RGBD
        frame = reader.next_frame()
               
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
            rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(rgb, depth, depth_scale=1000, depth_trunc=.75, convert_rgb_to_intensity=False)

            #Read generated intrinsic
            cam = o3d.io.read_pinhole_camera_intrinsic("/tmp/intrinsic.json")

            # #Create point cloud
            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, cam)
            
            #Filter point cloud
            
            pcd = pcd.voxel_down_sample(0.002)
            pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=16, std_ratio=0.75, print_progress=False)

            # Check to see if point cloud has less points than final    
            if len(pcd.points) < point_output:
                break
            else:
                    
                pcd = pcd.farthest_point_down_sample(point_output)

                # #Write point cloud to ply
                o3d.io.write_point_cloud("/mnt/data/10-POINTCLOUDS/000-ply/" + video + "_" + str(i).zfill(4) +".ply", pcd, compressed=True)

                i += 1
