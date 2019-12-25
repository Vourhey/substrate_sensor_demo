# Substrate Sensor Agent

The agent works with [SEN0233](https://wiki.dfrobot.com/Air_Quality_Monitor__PM_2.5,_Formaldehyde,_Temperature_&_Humidity_Sensor__SKU__SEN0233) sensor and publishes every `interval` seconds the measurements to Robonomics Network

## roslaunch parameters

* `interval` - interval in seconds. Default is 30 seconds
* `port` - specifies the port where the sensor is. Default is `/dev/ttyS0`

## Build

```
nix build -f release.nix
```

## Launch

```
roslaunch substrate_sensor_demo agent.launch
```

## NixOS Service

From the channel:

```
substrate_sensor.enable = true;
substrate_sensor.interval = 30;         # optional
substrate_sensor.port = "/dev/ttyS0";   # optional
```

or manually:

```
systemd.services.substrate_sensor = {
   requires = [ "roscore.service" ];  
   after = ["roscore.service" ];
   wantedBy = [ "multi-user.target" ];
   environment.ROS_MASTER_URI =  "http://localhost:11311";
   script = ''
        source /root/substrate_sensor_demo/result/setup.bash \
        && roslaunch substrate_sensor_demo agent.launch 
   '';
   serviceConfig = {
     Restart = "on-failure";
     StartLimitInterval = 0;
     RestartSec = 60;
     User = "liability";
     Group = "users";
   };
};
```

