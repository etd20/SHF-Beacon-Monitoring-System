# SHF Beacon Monitoring: Eric Dollinger

This repo contains all the files for monitoring an amateur radio SHF 10 GHz beacon using a Raspberry Pi Pico W. It will decode the incoming signal over the Pi's GPIO ADC and decode the morse code into a string which is then compared to the known beacon message we are looking for. The signal is sampled every 5 ms using an interrupt to get an accurate reading. Every 15 minutes, the Raspberry Pi will check if it has heard the beacon, if it has, it will wait for 24 hours and then send a status update. If it does not hear the beacon, it will send out an email to the maintainers of the beacon and notify them that the beacon is offline.

## Abstract

The SHF Beacon Monitoring System monitors an amateur radio beacon that is operating at 10 GHz. In order to monitor the beacon, a repurposed Police Microwave Radar Antenna is attached to a Raspberry Pi Pico W that analyzes the incoming morse code, or CW, signal and determines if a 10 GHz beacon is broadcasting. The Raspberry Pi Pico W will notify custodians of the beacon via email if it is fully operational once a day or offline if it is not heard every 15 minutes. The main objectives of the monitoring system are to receive a 10 GHz CW signal, convert it from analog to digital using the Raspberry Pi Pico W’s onboard analog-to-digital converter, analyze the incoming signal on the Raspberry Pi Pico W, determine if the received signal is the desired 10 GHz beacon, and notify a set list of custodians via email about the operational status of the beacon.

## Things to know

Coded using micropython.
If you are unable to connect to an open network, update the firmware on the Raspberry Pi Pico W and try again. Firmware after December 2022 fixes a bug with the network package. See attached setup and care document for how to reconstruct from scratch.

&copy; Eric Dollinger
