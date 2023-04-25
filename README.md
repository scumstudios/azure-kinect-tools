# Azure Kinect Volumetric Capture Wiki
A place for our research project to collect information regaring Azure Kinect volumetric capture.


## Azure Kinect SDK Linux Installation & Configuration

Ubuntu 20.04 & Derivatives:

SDK: https://learn.microsoft.com/en-us/azure/kinect-dk/sensor-sdk-download#linux-installation-instructions

Direct links to 18.04 .deb (can be installed on 20.04):
- K4A SDK: https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4a1.4/libk4a1.4_1.4.1_amd64.deb
- K4A Tools: https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/k/k4a-tools/k4a-tools_1.4.1_amd64.deb
- Body Tracking SDK: https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4abt1.1/libk4abt1.1_1.1.2_amd64.deb

Copy '99-k4a.rules' into '/etc/udev/rules.d/' to access the cameras as non-root user. [Reference Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md#linux-device-setup)



## Relevant software

Open Source Projects:

Python Wrappers

- [PyKinect Azure](https://github.com/ibaiGorordo/pyKinectAzure) can be installed through pip: ```pip install pykinect_azure```
- [pyk4a](https://github.com/etiennedub/pyk4a)
- [Azure Kinect Python](https://github.com/hexops/Azure-Kinect-Python/blob/master/example/simple_sample.py)

.NET Wrapper

- [k4a.net](https://github.com/bibigone/k4a.net/releases)


Commercial Solutions:

- [Brekel Pointcloud](https://brekel.com/brekel-pointcloud-v3/)
- [Depthkit](https://www.depthkit.tv/)
- EF EVE (discontinued)
