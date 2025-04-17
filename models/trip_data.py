from typing import List
from dataclasses import dataclass, field
import time

@dataclass
class TripData:
    timestamps: List[float] = field(default_factory=list)
    speeds: List[float] = field(default_factory=list)
    rpms: List[float] = field(default_factory=list)

    def record_sample(self, speed, rpm):
        self.timestamps.append(time.time())
        self.speeds.append(speed)
        self.rpms.append(rpm)
