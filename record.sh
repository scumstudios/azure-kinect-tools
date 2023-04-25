#!/bin/bash

framerate=30 #Available options: 30,15,5
timestamp=$(date +%s)

    # Generate Index List    
    index_list=$(k4arecorder --list)
    printf "Available Azure Kinect Cameras:\n\n$index_list\n"

    # Parse indices to an array
    readarray -t cameras <<< "$index_list"
    declare -a cam_rec=()

    # Set Master Camera
    printf "\nSet master device index: "
    read index_master

    printf "Please specify output directory: "
    read -e output_dir

    printf "Color Mode Selection: (2160p, 1536p, 1440p, 1080p, 720p, OFF): "
    read color_res

    printf "\nDepth Modes:\n1. NFOV_UNBINNED\n2. WFOV_2X2BINNED\n3. NFOV_2X2BINNED\n4. WFOV_UNBINNED\n5. PASSIVE_IR\n6. OFF\n\nSelect Depth Mode: "
    read depth_sel

    case $depth_sel in
        1)
        depth_res="NFOV_UNBINNED"
        ;;

        2)
        depth_res="WFOV_2X2BINNED"
        ;;

        3)
        depth_res="NFOV_2X2BINNED"
        ;;

        4)
        depth_res="WFOV_UNBINNED"
        ;;

        5)
        depth_res="PASSIVE_IR"
        ;;

        6)
        depth_res="OFF"
        ;;
    esac

    printf "Exposure (-11 to 1): "
    read exposure

    for i in "${cameras[@]}";
        do
            # Extract index number from list
            j=${i:6:1}

            # Re-sort array by filling with subs first
            if [ $j != $index_master ]; then
                cam_rec+=($j)
            fi
        done
     
    # Add master index as last
    cam_rec+=($index_master)

    for i in "${cam_rec[@]}";
        do       
            if [ $i != $index_master ]; then
                printf "Subordinate with index $i start with depth $depth_res\n"
                tilix -e k4arecorder --device $i --exposure-control "$exposure" --external-sync sub --imu ON -c $color_res -d "$depth_res" -r $framerate "$output_dir""$timestamp"_sub_$i.mkv
                sleep 2
            fi
        done
     
    printf "Master with index $i start with depth $depth_res\n"
    tilix -e k4arecorder --device $i --exposure-control "$exposure" --external-sync master --imu ON -c $color_res -d "$depth_res" -r $framerate "$output_dir""$timestamp"_master_$i.mkv
