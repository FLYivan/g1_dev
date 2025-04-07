import time
import sys
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient


class UserInterface:
    def __init__(self):
        self.test_option_ = None



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} networkInterface")
        sys.exit(-1)

    print("WARNING: Please ensure there are no obstacles around the robot while running this example.")
    input("Press Enter to continue...")

    ChannelFactoryInitialize(0, sys.argv[1])

    test_option = TestOption(name=None, id=None) 
    user_interface = UserInterface()
    user_interface.test_option_ = test_option

    sport_client = LocoClient()  
    sport_client.SetTimeout(10.0)
    sport_client.Init()

    print("Input \"list\" to list all test option ...")
    while True:
        user_interface.terminal_handle()

        print(f"Updated Test Option: Name = {test_option.name}, ID = {test_option.id}")

        if test_option.id == 0:
            sport_client.Damp()
        elif test_option.id == 1:
            sport_client.Damp()
            time.sleep(0.5)
            sport_client.Squat2StandUp()
        elif test_option.id == 2:
            sport_client.StandUp2Squat()
        elif test_option.id == 3:
            sport_client.Move(0.3,0,0)
        elif test_option.id == 4:
            sport_client.Move(0,0.3,0)
        elif test_option.id == 5:
            sport_client.Move(0,0,0.3)
        elif test_option.id == 6:
            sport_client.LowStand()
        elif test_option.id == 7:
            sport_client.HighStand()
        elif test_option.id == 8:
            sport_client.ZeroTorque()
        elif test_option.id == 9:
            sport_client.WaveHand()
        elif test_option.id == 10:
            sport_client.WaveHand(True)
        elif test_option.id == 11:
            sport_client.ShakeHand()
            time.sleep(3)
            sport_client.ShakeHand()
        elif test_option.id == 12:
            sport_client.Damp()
            time.sleep(0.5)
            sport_client.Lie2StandUp() # When using the Lie2StandUp function, ensure that the robot faces up and the ground is hard, flat and rough.

        time.sleep(1)