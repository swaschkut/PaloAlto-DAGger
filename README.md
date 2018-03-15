# PaloAlto-DAGger

PANW Dagger is a tool that allows for synchronization of the Dynamic Address Groups (DAG) with 3rd party meta-data services (such as OpenStack Nova, OpenStack Neutron, Nuage SDN Controller, etc.).

The current implementation supports:
- OpenStack

## Prerequisites

see requirements.txt

## Installation

    $ sudo -H pip install virtualenv
    $ virtualenv venv
    $ source ./venv/bin/activate 
    $ git clone https://github.com/ivanbojer/PaloAlto-DAGger.git
    $ cd PaloAlto-DAGger
    $ pip install -r requirements.txt
    
## Configuration

Modify 'clouds.yaml' to suite your needs.

## Running

    $ python PANWDagger.py

## Disclaimer

PaloAlto-DAGger is for illustrative purposes only. This software is supplied "AS IS" without any warranties and support.
