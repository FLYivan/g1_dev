import json
from unitree_api.msg import Request
from .sport_api import *
from typing import List  # 添加缺失的导入


"""
" class PathPoint
"""
class PathPoint:
    def __init__(self, timeFromStart: float, x: float, y: float, yaw: float, vx: float, vy: float, vyaw: float):
        self.timeFromStart = timeFromStart
        self.x = x
        self.y = y
        self.yaw = yaw
        self.vx = vx
        self.vy = vy
        self.vyaw = vyaw

"""
" class SportClient
"""

class SportClient:
    def Damp(self, req):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_DAMP


    def BalanceStand(self,req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_BALANCESTAND


    def StopMove(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_STOPMOVE


    def StandUp(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_STANDUP


    def StandDown(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_STANDDOWN


    def RecoveryStand(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_RECOVERYSTAND


    def Euler(self, req: Request, roll: float, pitch: float, yaw: float):
        js = {
            "x": roll,
            "y": pitch,
            "z": yaw
        }
        req.parameter = json.dumps(js)
        req.header.identity.api_id = ROBOT_SPORT_API_ID_EULER


    def Move(self, req: Request, vx: float, vy: float, vyaw: float):
        js = {
            "x": vx,
            "y": vy,
            "z": vyaw
        }
        req.parameter = json.dumps(js)
        req.header.identity.api_id = ROBOT_SPORT_API_ID_MOVE


    def Sit(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_SIT


    def RiseSit(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_RISESIT


    def SwitchGait(self, req: Request, d: int):
        js = {
            "data": d
        }
        req.header.identity.api_id = ROBOT_SPORT_API_ID_SWITCHGAIT
        req.parameter = json.dumps(js)


    def Trigger(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_TRIGGER

    def BodyHeight(self, req: Request, height: float):
        js = {
            "data": height
        }
        req.parameter = json.dumps(js)
        req.header.identity.api_id = ROBOT_SPORT_API_ID_BODYHEIGHT

    def FootRaiseHeight(self, req: Request, height: float):
        js = {
            "data": height
        }
        req.parameter = json.dumps(js)
        req.header.identity.api_id = ROBOT_SPORT_API_ID_FOOTRAISEHEIGHT

    def SpeedLevel(self, req: Request, level: int):
        js = {
            "data": level
        }
        req.parameter = json.dumps(js)
        req.header.identity.api_id = ROBOT_SPORT_API_ID_SPEEDLEVEL

    def Hello(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_HELLO

    def Stretch(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_STRETCH


    def TrajectoryFollow(self, req: Request, path: List[PathPoint]):
        js_path = []
        req.header.identity.api_id = ROBOT_SPORT_API_ID_TRAJECTORYFOLLOW
        for i in range(30):
            js_point = {
                "t_from_start": path[i].timeFromStart,
                "x": path[i].x,
                "y": path[i].y,
                "yaw": path[i].yaw,
                "vx": path[i].vx,
                "vy": path[i].vy,
                "vyaw": path[i].vyaw
            }
            js_path.append(js_point)
        req.parameter = json.dumps(js_path)


    def SwitchJoystick(self, req: Request, flag: bool):
        js = {
            "data": flag
        }
        req.parameter = json.dumps(js)
        req.header.identity.api_id = ROBOT_SPORT_API_ID_SWITCHJOYSTICK

    def ContinuousGait(self, req: Request, flag: bool):
        js = {
            "data": flag
        }
        req.parameter = json.dumps(js)
        req.header.identity.api_id = ROBOT_SPORT_API_ID_CONTINUOUSGAIT

    def Wallow(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_WALLOW

    def Content(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_CONTENT

    def Pose(self, req: Request, flag: bool):
        js = {
            "data": flag
        }
        req.parameter = json.dumps(js)
        req.header.identity.api_id = ROBOT_SPORT_API_ID_POSE

    def Scrape(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_SCRAPE

    def FrontFlip(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_FRONTFLIP

    def FrontJump(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_FRONTJUMP

    def FrontPounce(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_FRONTPOUNCE

    def Dance1(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_DANCE1

    def Dance2(self, req: Request):
        req.header.identity.api_id = ROBOT_SPORT_API_ID_DANCE2




