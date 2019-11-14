# Stationary Spinning Follower Robot
A robot that uses fiducial markers (ArUco) to obtain the relative position to the marker and adjusts its position using PID control to follow the moving marker. You can find also separately the modelling of a DC motor which we used on SSFR.

![setup](https://user-images.githubusercontent.com/24254286/68078356-28faa900-fdb3-11e9-94ae-d9308d47922d.jpg)

## Installation
Get the Raspberry Pi Ubuntu Mate Installation for your Rpi:
https://ubuntu-mate.org/download/


Install git:

``` $ sudo apt-get install git ```

Install OpenCV with Python in the Rpi in order to make use of the ArUco library:

``` $ sudo apt-get install python-opencv ```

Clone the repository anywhere you want:

``` $ git clone https://github.com/hpoleselo/SSFR.git ```

## Usage

If you want to check how we retrieve the model for the control, check the folder ``` PlantModel ``` with MATLAB.

## Lessons Learned

Check the file [linque] to the next time we decide building a robot from scratch...

## Authors

* **Henrique Poleselo** - [hpoleselo](https://github.com/hpoleselo)
* **Jesse de Oliveira Santana Alves** - [Jessalves11](https://github.com/Jessalves11)
* **Luis Gustavo Nunes Christensen** - [Goustaf](https://github.com/goustaf)

## Professor

**Humberto Xavier de Araujo**
