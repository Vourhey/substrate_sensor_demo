{ stdenv
, mkRosPackage
, robonomics_comm
, python3Packages
}:

mkRosPackage rec {
  name = "${pname}-${version}";
  pname = "substrate_sensor_demo";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = [
    robonomics_comm
    python3Packages.pyserial
  ];

  meta = with stdenv.lib; {
    description = "Agent that offers data from sensors";
    homepage = http://github.com/vourhey/substrate_sensor_demo;
    license = licenses.bsd3;
    maintainers = with maintainers; [ vourhey ];
  };
}
