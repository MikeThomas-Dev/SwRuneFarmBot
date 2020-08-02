# Summoners War Rune Farm Bot
This project describes a way to automate the process of farming items, called runes, in the mobile game 
[Summoners War][1] on a Windows 10 host. The core components of the implementation are [Python][2], 
[Tensorflow Object Detection][3] and [Tesseract-OCR][4].

## Getting Started
The setup of Tensorflow Object Detection using Python was done following the instructions of this [tutorial][5]. 
For Tesseract-OCR using Python setup [this guide][6] was used. Please note that the versions of the components used 
within this project can differ from the ones mentioned in the tutorials. 
 
 Versions used for this project:
- Cuda 10.0
- cuDNN 7.6.7 for Cuda 10.0
- Python Anaconda 4.8.2
- Python 3.5
- Tensorflow-GPU 1.15
- NVIDIA GeForce GTX 1080 Driver Version 26.21.14.4587
- Tesseract 5.0.0-alpha.20200328

In order to run and further control the mobile game Summoners War on a Windows 10 host [BlueStacks][7] was used.

The files contained in this repository must be placed in a folder called SwRuneFarmerProject within the 
object_detection folder mentioned in the [Tensorflow guide][5]. Following the instructions this folder structure should 
exist: 

```
C:
└─── tensorflow1
│   └─── models
│   │   └─── research
│   │   │   └─── object_detection
│   │   │   │   └─── SwRuneFarmerProject
│   │   │   │   │   └─── Content of this repository
```
## Dependencies
In order to perform mouse move and click actions the functionality provided by [mouse][8] is used. The stated repository v0.7.1 is included in this repository.

[1]: https://summonerswar.com/
[2]: https://www.python.org/
[3]: https://github.com/tensorflow/models/tree/master/research/object_detection
[4]: https://github.com/tesseract-ocr/tesseract
[5]: https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10
[6]: https://nanonets.com/blog/ocr-with-tesseract/
[7]: https://www.bluestacks.com/de/index.html
[8]: https://github.com/boppreh/mouse
