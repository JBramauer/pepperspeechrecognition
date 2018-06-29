# Pepper Speech Recognition

This is a python module that brings Google Speech Recognition to the Pepper robot by Aldebaran.
It was specifically implemented so it can be run ON the robot as a NaoQi module but it can also be run on your computer.

## Features
* Automatic detection if and when a person speaks
* Automatic detection when a person stops speaking
* Calibration function to learn background noise level
* Manual trigger mode (record now for 10 seconds and then recognize)
* This module provides an ALMemory event other modules can subscribe to
* Unlike other modules this one does NOT depend on PyAudio/Portaudio
* Only dependencies: Numpy, NaoQi Python SDK

## Setup to run on robot
Everything you need should already be installed, simply clone the repository / copy the files to your robot, ssh into it and run

 ```
python module_speechrecognition.py
```

## Setup to run on computer

Like every NaoQi Python project you need the NaoQi Python SDK. You can get it from [doc.aldebaran.com](http://doc.aldebaran.com/2-5/dev/python/install_guide.html).
To test it simply run

```
python
import naoqi
```

Next up you need the numpy python module, which is the only python library used

```
pip install numpy
```

Test it:

```
python
import numpy
```

Now run the speechrecognition module


 ```
python module_speechrecognition.py --pip (your robot IP)
```

## Configuration
To configure the module you can use an ALProxy instance you can get from the Broker (speechrecognition module needs to be running)

Here's a simple example on how to do that:

```
SpeechRecognition = ALProxy("SpeechRecognition")
SpeechRecognition.start()
SpeechRecognition.setLanguage("de-de")
SpeechRecognition.calibrate()
SpeechRecognition.enableAutoDetection()
```
Calling start() makes the module subscribe to the ALAudio event of the robot. Calibrate() makes it calculate the mean RMS value of the signal for 4 seconds and use this as a reference for background noise level.

Also, you can just use the module like this to trigger a one-time recognition:
```
SpeechRecognition = ALProxy("SpeechRecognition")
SpeechRecognition.start()
SpeechRecognition.setLanguage("de-de")

# starts immediately, records for at least HOLD_TIME seconds and then tries to recognize
SpeechRecognition.startRecoring() 
```

You can use [module_receiver.py](module_receiver.py) as a template for implementing your own module.

## Subscribing to the ALMemory event
The speechrecognition module raises an ALMemory event every time a string was successfully recognized. You can subscribe to it in your module using the ALMemory proxy.

```
memory = naoqi.ALProxy("ALMemory")
memory.subscribeToEvent("SpeechRecognition", self.getName(), "processRemote")
```

"SpeechRecognition" is the name of the event, "proccessRemote" the name of your callback function.

```
def processRemote(self, signalName, message):
    # Do something with the received speech recognition result
    print(message)
```

### ROS Module
A simple ROS (Robot Operating System) module [is provided](ros_receiver.py), that uses [rospy](http://wiki.ros.org/rospy) to publish a ROS message whenever speech is recognized, carrying the recognized string as data.

## Dependencies
The speechrecognition module was built to be able to run ON Pepper (and you can't easily install 3rd party libraries there, also we need to be efficient), so it's only dependencies are
* Python 2.7
* numpy
* naoqi Python SDK

All of them are pre-installed on Pepper

## Built With

* Python 2.7
* [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE

## Changelog

**Version 1.0** - Initial release, May 30 2018

## Authors

* **Johannes Bramauer** @ Vienna University of Technology - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Anthony Zang (Uberi) and his [SpeechRecognition](https://github.com/Uberi/speech_recognition)
