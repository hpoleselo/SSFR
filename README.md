# Stationary Spinning Follower Robot
A robot that uses fiducial markers (ArUco) to obtain the relative position to the marker and adjusts its position using PID control to follow the moving marker. You can find also separately the modelling of a DC motor which we used on SSFR.

![setup](https://user-images.githubusercontent.com/24254286/68078356-28faa900-fdb3-11e9-94ae-d9308d47922d.jpg)

## Installation
Get the Raspberry Pi Ubuntu Mate Installation for your Rpi:
https://ubuntu-mate.org/download/


Install git:

``` $ sudo apt-get install git ```

Install pip:

``` $ wget https://bootstrap.pypa.io/get-pip.py ```

``` $ sudo python2.7 get-pip.py ```

Install OpenCV with Python in the Rpi:

``` $ sudo apt-get install python-opencv ```

Clone the repository to anywhere:

``` $ git clone https://github.com/hpoleselo/SSFR.git ```

## Usage

If you want to check model retrieving, check the folder ``` /PlantModel ``` with MATLAB.

## Authors

* **Henrique Poleselo** - [hpoleselo](https://github.com/hpoleselo)
* **Jesse de Oliveira Santana Alves**
* **Luis Gustavo Nunes Christensen**

## Professor

**Humberto Xavier de Araujo**
