# example.varcontrol
Simple RIAPS application to demonstrate RIAPS sending control commands to OpenDSS simulation agent. The agent needs to be running separately in a Windows machine. This application is designed to work with the model in the sample directory of the "interface.opendss" repository. For an end to end demo, please clone that repository onto the windows host machine on which the RIAPS VM is installed.

## Algorithm
The application here reads the voltage of a specific line of the network, queries the reactive part of a particular load and then updates it according to a duty cycle. Thus, it demonstrates all the three types of messaging that the OpenDSS agent supports: Publish, Subscribe and Query.

## Organization

The folder contains the riaps application files that talk with OpenDSS. The OpenDSS device component provides the necessary interfacing machinery while the Controller component implements the control logic. The model has been extended to thirty two switches. The updated model can be found in the models directory.

## Configuration

In the deployment file "varcontrol.depl", each Conrtroller component needs to be supplied with a tuple corresponding to the sensor (which it will subscribe to) and the actuator (which it will send commands to control) in the form of `[Object.Name.Attribute]`


Running the app with Mininet
----------------------------

The apps can run on the development VM (that has RIAPS installed) under mininet. 

Note: rpyc_registry, and riaps services (e.g. riaps_deplo) must NOT be running on the VM.
These can be halted as follows:
	systemctl disable riaps-deplo.service
	systemctl stop riaps-deplo.service || true
	systemctl disable riaps-rpyc-registry.service
	systemctl stop riaps-rpyc-registry.service || true

To start a mininet-based run (in this directory).
   source setup-mn
   riaps-mn N
where N is the number of virtual mininet hosts to be launched.
 At the mininet prompt:
    mininet> source mn/SCRIPT
 where SCRIPT is the name of the .mn script. (e.g. varcontrol2.mn).
 Note: mininet does not handle exceptions well, so if the last command fails it may leave the 
 (virtual) network intefaces behind - and a restart of the VM may be necessary.
 Note: the starup on the virtual nodes can take a few seconds.
 
 The simulation logs changes into InfluxDB (as specified in models/*/loadshed.gll), 
 the results can be accessed using the Grafana on localhost:3000.
 
 Running the app with Mininet in a RIAPS development environment
 ----------------------------------------------------------------
 
The app can be run on a VM that is being used to develop RIAPS as follows.
Assume $RIAPS points to the root folder of the RIAPS source tree, and $APP points to this folder.
	cd $RIAPS 
	source setup
	cd $APP
	souce setup-mn.dev
	riaps-mn N
where N is the number of virtual mininet hosts to be launched.
