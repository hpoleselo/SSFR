# Lessons Learned

First of all, check the deadband from the motor. We tested our motor with ~2V and it was spinning. Note that when you add the motor
to your robot the deadband will increase due to the robot's weight, so expect the motor to work around 2.5V, for instance. The ideal
would be have our robot operating with very low voltage so it can do fine adjustments, i.e our controller would work better.

## Physical Part
- Check deadband
- Check the sensor you want to use to control the feedback of your robot
- Find the minimum voltage that the robot responds, this will be important for your controller
- When you build your robot the wheels should be SYMMETRICAL, otherwise the robot will not go forward or rotate on its on axis properly
- After mounting the wheels on the robot don't forget to test with simple functions like going forward and check if they're really symmetrical

## Control
- Check if the actuator speed is at least 3x faster than the response of your sensor
- In order to the controller work properly the sensor should deliver AT LEAST 25Hz samples to have a closed loop control w/ that sensor
- After checking the minimum voltage you know your dynamic range to control
- The higher the dynamic range the better because you could do fine adjustments