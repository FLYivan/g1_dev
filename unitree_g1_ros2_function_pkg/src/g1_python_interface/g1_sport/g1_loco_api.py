"""
" service name
"""
LOCO_SERVICE_NAME = "loco"


"""
" service api version
"""
LOCO_API_VERSION = "1.0.0.0"


"""
" api id
"""

ROBOT_API_ID_LOCO_GET_FSM_ID = 7001
ROBOT_API_ID_LOCO_GET_FSM_MODE = 7002
ROBOT_API_ID_LOCO_GET_BALANCE_MODE = 7003
ROBOT_API_ID_LOCO_GET_SWING_HEIGHT = 7004
ROBOT_API_ID_LOCO_GET_STAND_HEIGHT = 7005
ROBOT_API_ID_LOCO_GET_PHASE = 7006

ROBOT_API_ID_LOCO_SET_FSM_ID = 7101
ROBOT_API_ID_LOCO_SET_BALANCE_MODE = 7102
ROBOT_API_ID_LOCO_SET_SWING_HEIGHT = 7103
ROBOT_API_ID_LOCO_SET_STAND_HEIGHT = 7104
ROBOT_API_ID_LOCO_SET_VELOCITY = 7105





# Type alias for LocoCmd
LocoCmd = Dict[str, Union[int, float, List[float]]]

@dataclass
class JsonizeDataVecFloat:
    data: List[float] = None
    
    def from_json(self, json_map: Dict[str, Any]) -> None:
        self.data = json_map.get("data")
        
    def to_json(self) -> Dict[str, Any]:
        return {"data": self.data}

@dataclass        
class JsonizeVelocityCommand:
    velocity: List[float] = None
    duration: float = None
    
    def from_json(self, json_map: Dict[str, Any]) -> None:
        self.velocity = json_map.get("velocity")
        self.duration = json_map.get("duration")
        
    def to_json(self) -> Dict[str, Any]:
        return {
            "velocity": self.velocity,
            "duration": self.duration
        }
