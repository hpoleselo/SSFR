# Lessons Learned

First of all, check the deadband from the motor. We tested our motor with ~2V and it was spinning. Note that when you add the motor
to your robot the deadband will increase due to the robot's weight, so expect the motor to work around 2.5V, for instance. The ideal
would be have our robot operating with very low voltage so it can do fine adjustments, i.e our controller would work better.

- Check deadband
- Check the sensor you want to use to control the feedback of your robot
- Check if the actuator speed is at least 3x faster than the response of your sensor
- Find the minimum voltage that the robot responds, this will be important for your controller
- After checking the minimum voltage you know your dynamic range to control