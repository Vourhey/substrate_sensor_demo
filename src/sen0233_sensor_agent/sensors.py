import serial
from threading import Thread
import rospy
from collections import deque

class SEN0233:
    def __init__(self):
        physicalPort = '/dev/ttyS0'

        self.serialPort = serial.Serial(physicalPort)
        self.buff = deque(maxlen=4)

        def read_most_recent_data(buff: deque):
            while True:
                if self.serialPort.in_waiting >= 40:
                    d = self.serialPort.read(40)

                    CR1 =(d[38]<<8) + d[39]
                    CR2 = 0
                    for i in range(38):
                        CR2 += d[i]

                    if CR1 == CR2:
                        PMSa = d[12]             # Read PM2.5 High 8-bit
                        PMSb = d[13]             # Read PM2.5 Low 8-bit
                        PMS = (PMSa<<8)+PMSb        # PM2.5 value
                        FMHDSa = d[28]           # Read Formaldehyde High 8-bit
                        FMHDSb = d[29]           # Read Formaldehyde Low 8-bit
                        FMHDS = (FMHDSa<<8)+FMHDSb  # Formaldehyde value
                        TPSa = d[30]             # Read Temperature High 8-bit
                        TPSb = d[31]             # Read Temperature Low 8-bit
                        TPS = (TPSa<<8)+TPSb        # Temperature value
                        HDSa = d[32]             # Read Humidity High 8-bit
                        HDSb = d[33]             # Read Humidity Low 8-bit
                        HDS = (HDSa<<8)+HDSb        # Humidity value
                    else:
                        PMS = 0
                        FMHDS = 0
                        TPS = 0
                        HDS = 0

                    buff.append(round(TPS/10, 2))
                    buff.append(round(HDS/10, 2))
                    buff.append(FMHDS)
                    buff.append(PMS)
                rospy.sleep(0.7)

        self.reading_thr = Thread(target=read_most_recent_data, args=(self.buff, ))
        self.reading_thr.start()

    def data(self) -> dict:
        rospy.loginfo("In waiting data: {}".format(self.serialPort.in_waiting))

        res = {
                "temp_c": self.buff.popleft(),
                "humidity": self.buff.popleft(),
                "formaldehyde": self.buff.popleft(),
                "pm2.5": self.buff.popleft()
                }
        rospy.loginfo(res)
        return res

