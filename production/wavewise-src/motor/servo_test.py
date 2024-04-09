from machine import PWM, Pin
from time import sleep
# Set the GPIO pin number (based on the connection in step 2)
SERVO_PIN = 20
# Set the PWM frequency (50Hz is common for servos)
PWM_FREQUENCY = 50
# Create a PWM object with the specified pin and frequency
pwm = PWM(Pin(SERVO_PIN))
pwm.freq(PWM_FREQUENCY)

while True: 
    for duty in range(65025): 
        pwm.duty_u16(duty)
        print(duty)
        sleep(0.0001)
    for duty in range(65025, 0, -1): 
        pwm.duty_u16(duty)
        print(duty)
        sleep(0.0001)
# # Function to set the servo angle
# def set_angle(angle):
#     # Convert the angle to a duty cycle value (0.5 ms to 2.5 ms pulse width)
#     duty_cycle = int((angle / 180) * (1000000 / PWM_FREQUENCY) + 2500)
#     # Set the duty cycle to control the servo
#     pwm.duty_ns(duty_cycle)
# # Main loop
# while True:
#     # Move the servo from 0 to 180 degrees
#     for angle in range(0, 180, 5):
#         print(angle)
#         set_angle(angle)
#         utime.sleep_ms(50)
#     # Move the servo back from 180 to 0 degrees
#     for angle in range(180, 0, -5):
#         print(angle)
#         set_angle(angle)
#         utime.sleep_ms(50)