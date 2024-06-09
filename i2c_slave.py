import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import keyboard.keyboard as keyboard

GPIO.setmode(GPIO.BOARD)

stepPins = [7,11,13,15]
sensorPin = 19

GPIO.setup(sensorPin,GPIO.IN)

for pin in stepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

stepper_state = 0
seq_pos = 0
backward_move = 0
program_state = 'waiting'

just_one = 0

seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1] ]

x = []
y = []


def check_keys(global_state):
    program_state = global_state
    if (keyboard.is_pressed('s')):
        program_state = 'started'
    elif (keyboard.is_pressed('p')):
        program_state = 'waiting'
    elif (keyboard.is_pressed('r')):
        program_state = ('restarting')
    elif (keyboard.is_pressed('g')):
        program_state = ('ploting')
    return program_state

try:
    while(True):
        program_state = check_keys(program_state)
        if (program_state == 'started'):
            if (GPIO.input(sensorPin) == 0 and just_one == 0):
                if (len(x) == 0):
                    x.append(0)
                    begin = time.time()
                else:
                    timer = time.time()
                    x.append(timer - begin)
                y.append(stepper_state)
                backward_move = 400
                just_one = 1
            if (GPIO.input(sensorPin) == 1):
                just_one = 0
            if(backward_move == 0):
                if (seq_pos == 8):
                    seq_pos = 0
                if (seq_pos == -1):
                    seq_pos = 7
                for pin in range(4):
                    GPIO.output(stepPins[pin], seq[seq_pos][pin])
                seq_pos += 1
                stepper_state -= 1
            else:
                if (seq_pos == 8):
                    seq_pos = 0
                if (seq_pos == -1):
                    seq_pos = 7
                for pin in range(4):
                    GPIO.output(stepPins[pin],seq[seq_pos][pin])           
                stepper_state += 1
                seq_pos -= 1
                backward_move -= 1
        if (program_state == 'ploting'):
            plt.plot(x,y)
            plt.show()
            program_state = 'waiting'
        if (program_state == 'restarting'):
            backward_move = 0
            x = []
            y = []
            if (stepper_state < 0):
                if (seq_pos == 8):
                    seq_pos = 0
                if (seq_pos == -1):
                    seq_pos = 7
                for pin in range(4):
                    GPIO.output(stepPins[pin],seq[seq_pos][pin])           
                stepper_state += 1
                seq_pos -= 1
            elif (stepper_state > 0):
                if (seq_pos == 8):
                    seq_pos = 0
                if (seq_pos == -1):
                    seq_pos = 7
                for pin in range(4):
                    GPIO.output(stepPins[pin], seq[seq_pos][pin])
                seq_pos += 1
                stepper_state -= 1
            else:
                program_state = 'waiting'
        time.sleep(0.001)
except KeyboardInterrupt:
    print("Programa interrumpido, el Step Motor puede no estar en la posicion esperada")

 
            