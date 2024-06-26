import multiprocessing
import time
import numpy as np

from pymmWave.utils import load_cfg_file
from pymmWave.IWR6843AOP import IWR6843AOP
from asyncio import get_event_loop
from Moduls.Group import get_closest_cluster, rotate_xy, distance
from Moduls.Encoder import RotaryEncoder
from Moduls.Move_3 import*


sensor1 = IWR6843AOP("1", verbose=False)
file = load_cfg_file("config.cfg")

config_connected = sensor1.connect_config('/dev/ttyUSB0', 115200)
if not config_connected:
    print("Config connection failed.")
    exit()

data_connected = sensor1.connect_data('/dev/ttyUSB1', 921600)
if not data_connected:
    print("Data connection failed.")
    exit()

if not sensor1.send_config(file, max_retries=5):
    print("Sending configuration failed")
    exit()

def read_encoder(shared_data):
	encoder = RotaryEncoder(5, 6)
	while True:
		shared_data.value = encoder.get_position()
		time.sleep(0.001)
		
def get_cluster(conn2,conn3):
	while True:
		point_matrix = conn2.recv()
		angle = shared_data.value
		cluster = get_closest_cluster(point_matrix, offset= np.array([-0.36,0,-0.46, 0])) # This is the offset [x, y, z, Doppler]
		target = rotate_xy(cluster, angle)
		conn3.send(target)
	
def move_to_target(conn4):
	turret = Turret()
	turret.setup_motors()
	while True:
		target = conn4.recv()
		turret.get_xyz(target)
		turret.find_angle()
		turret.move_horizontal_motor()
		turret.move_vertical_motor()


shared_data = multiprocessing.Value('f', 0.0)
conn1, conn2 = multiprocessing.Pipe()
conn3, conn4 = multiprocessing.Pipe()

p1 = multiprocessing.Process(target=read_encoder, args=(shared_data, ))
p1.start()
p2 = multiprocessing.Process(target=get_cluster, args=(conn2,conn3 ))
p2.start()
p3 = multiprocessing.Process(target=move_to_target, args=(conn4, ))
p3.start()

async def main(sens):
	while True:
		data = await sens.get_data()
		point_matrix = data.get()
		conn1.send(point_matrix)
		
		 
event_loop = get_event_loop()
event_loop.create_task(sensor1.start_sensor())
event_loop.create_task(main(sensor1))
event_loop.run_forever()