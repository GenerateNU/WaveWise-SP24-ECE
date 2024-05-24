from machine import PWM, Pin
from time import sleep
# Set the GPIO pin number (based on the connection in step 2)
SERVO_PIN = 8
# Set the PWM frequency (50Hz is common for servos)
PWM_FREQUENCY = 50
# Create a PWM object with the specified pin and frequency
pwm = PWM(Pin(SERVO_PIN), invert=True)
pwm.freq(PWM_FREQUENCY)

# begin = 85
# end = 95

begin = 4
end = 9

for duty in range(begin, end): 
    pwm.duty_u16(duty*650)
    print(duty*650, duty/100.0)
    sleep(1)
for duty in range(end, begin, -1): 
    pwm.duty_u16(duty*650)
    print(duty*650, duty/100.0)
    sleep(1)
    # for duty in range(0,65025, 100): 
    #     pwm.duty_u16(duty)
    #     print(duty, duty/65025.0)
    #     sleep(0.5)
    # for duty in range(65025, 0, -100): 
    #     pwm.duty_u16(duty)
    #     print(duty, duty/65025.0)
    #     sleep(0.5)
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