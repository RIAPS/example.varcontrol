# example.varcontrol
Simple RIAPS application to demonstrate RIAPS sending control commands to OpenDSS simulation agent. The agent needs to be running separately in a Windows machine. 

## Algorithm
The application here reads the voltage of a specific line of the network, queries the reactive part of a particular load and then updates it according to a duty cycle. Thus, it demonstrates all the three types of messaging that the OpenDSS agent supports: Publish, Subscribe and Query.

## Organization

The folder contains the riaps application files that talk with OpenDSS. The OpenDSS device component provides the necessary interfacing machinery while the Controller component implements the control logic. The model has been extended to thirty two switches. The updated model can be found in the models directory.

## Configuration

In the deployment file "varcontrol.depl", each Conrtroller component needs to be supplied with a tuple corresponding to the sensor (which it will subscribe to) and the actuator (which it will send commands to control) in the form of `[Object.Name.Attribute]`
