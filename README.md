# Scum Studios Azure Kinect Volumetric Tools

A set of tools to record and process point clouds from multiple Azure Kinect cameras.

## Prerequisites (Installation instructions below)

- Ubuntu 20.04, 22.04 or derivatives. Our test environment is Linux Mint 20.3.
- Azure Kinect SDK
- Python 3.8 or higher
- Python Open3D library


### Azure Kinect SDK Linux Installation & Configuration

Ubuntu 20.04 & Derivatives:

SDK: https://learn.microsoft.com/en-us/azure/kinect-dk/sensor-sdk-download#linux-installation-instructions

Direct links to 18.04 .deb (can be installed on 20.04):
- K4A SDK: https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4a1.4/libk4a1.4_1.4.1_amd64.deb
- K4A Tools: https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/k/k4a-tools/k4a-tools_1.4.1_amd64.deb
- Body Tracking SDK: https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4abt1.1/libk4abt1.1_1.1.2_amd64.deb

Copy '99-k4a.rules' into '/etc/udev/rules.d/' to access the cameras as non-root user. [Reference Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md#linux-device-setup)

For Ubuntu 22.04, libsoundio1 is no longer in the repos and is required for the K4A SDK, you can install the [.deb from 20.04](http://archive.ubuntu.com/ubuntu/pool/universe/libs/libsoundio/libsoundio1_1.1.0-1_amd64.deb) first at your own risk.


### Python Open3D

Open3D can be installed through the Python package manager (pip).

Install pip: ```sudo apt install python3-pip```

Install Open3D: ```pip install open3d```
