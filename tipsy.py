import asyncio
import os

from typing import List
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.sensor import Sensor
from viam.components.base import Base
from viam.services.vision import VisionClient

robot_secret = os.getenv('ROBOT_SECRET') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''
# change this if you named your base differently in your robot configuration
base_name = os.getenv('ROBOT_BASE') or 'tipsy-base'
# change this if you named your camera differently in your robot configuration
camera_name = os.getenv('ROBOT_CAMERA') or 'cam'
pause_interval = os.getenv('PAUSE_INTERVAL') or 3
sensor_count = os.getenv('SENSOR_COUNT') or 2
drink_grab_wait_time = 30

if isinstance(pause_interval, str):
    pause_interval = int(pause_interval)

if isinstance(sensor_count, str):
    sensor_count = int(sensor_count)

base_state = "stopped"


async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload=robot_secret)
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address(robot_address, opts)


async def obstacle_detect(sensor: Sensor):
    reading = (await sensor.get_readings())["distance"]
    return reading


async def gather_obstacle_readings(sensors: List[Sensor]):
    return await asyncio.gather(*[obstacle_detect(sensor) for sensor in sensors])


async def obstacle_detect_loop(sensors: List[Sensor], base: Base):
    while (True):
        readings = await gather_obstacle_readings(sensors)
        global base_state
        if all(reading < 0.4 for reading in readings):
            # stop the base if moving straight
            if base_state == "straight":
                await base.stop()
                base_state == "stopped"
                print("obstacle in front")
        await asyncio.sleep(.01)


async def mingle(base: Base):
    global base_state
    print("I will turn and look for a person")
    base_state = "spinning"
    await base.spin(45, 45)
    base_state = "stopped"


async def person_detect(detector: VisionClient, sensors: List[Sensor], base: Base):
    while (True):
        # look for person
        found = False
        global base_state
        print("will detect")
        detections = await detector.get_detections_from_camera(camera_name)
        for d in detections:
            if d.confidence > .7:
                print(d.class_name)
                if (d.class_name == "Person"):
                    found = True
                    break
        if (found):
            print("I see a person")
            # first manually call obstacle_detect - don't even start moving if someone is in the way
            distances = await gather_obstacle_readings(sensors)
            if all(distance > 0.4 for distance in distances):
                print("will move straight")
                base_state = "straight"
                await base.move_straight(distance=800, velocity=250)
                base_state = "stopped"
            elif any(classification.class_name == "Person"
                     async for classification in detector.get_classifications_from_camera(camera_name, 1)
                     if classification.confidence > .7):
                print("waiting for person to grab drink")
                await asyncio.sleep(drink_grab_wait_time)
                await mingle()
        else:
            await mingle()

        await asyncio.sleep(pause_interval)


async def main():
    robot = await connect()
    base = Base.from_robot(robot, base_name)
    sensors = [Sensor.from_robot(robot, "ultrasonic" + x)
               for x in range(sensor_count)]
    detector = VisionClient.from_robot(robot, "myPeopleDetector")

    # create a background task that looks for obstacles and stops the base if its moving
    obstacle_task = asyncio.create_task(obstacle_detect_loop(sensors, base))
    # create a background task that looks for a person and moves towards them, or turns and keeps looking
    person_task = asyncio.create_task(person_detect(detector, sensors, base))
    results = await asyncio.gather(obstacle_task, person_task, return_exceptions=True)
    print(results)

    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
