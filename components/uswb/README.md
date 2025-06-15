# UltimateSpeed Wallbox

Esphome component to control the allowed current to be used to charge a vehicle.
The component provides a sensor of the requested current of the wallbox
and a number to set the the allowed current.

Only the revision `A1` is supported. `A2` use another protocol, which is documented by the customer (should be easy to implement it if someone has one of this devices for testing).

## Example components

- ESP32 Dev Kit C V2
- Waveshare 4777 RS485 Board (3.3V)
- USWB11A1

Hardware setup:

The transceiver connects to the UART of the MCU. For ESP32, pin ``16`` to ``RO`` and pin ``17`` to ``DI`` are the default ones but any other pins can be used as well. ``3.3V`` to ``VCC`` and naturally ``GND`` to ``GND``. And ``RSE`` to ``18``.

The rs485 setting of the inverter must be one of the slave_id positions (e.g. 2). This id must be
set as uswb address.

RS485 of the mcu to NET2 of the inverter.


## Example config

```yaml
external_components:
  - source: github://bammab/custom_components_for_esphome

  # - source:
  #     type: git
  #     url: https://INTERNAL_GIT/USER/custom_components_for_esphome
  #     ref: dev_uswb11a1
  #     # username: OPTIONAL_USER
  #     # password: OPTIONAL_PWD
  #   components: [ uswb ]

  # - source:
  #     type: local
  #     path: local_components

...

uart:
  id: uswb_uart
  rx_pin: GPIO16
  tx_pin: GPIO17
  baud_rate: 4800
  stop_bits: 1

uswb:
  id: uswb_controller
  uart_id: uswb_uart
  send_wait_time: 200ms
  # address: 2
  # update_interval: 10s
  # revision: A1
  flow_control_pin: 18

sensor:
  - platform: uswb
    id: requested_current
    uswb_id: uswb_controller
    name: "USWB11A1 Requested Current"

switch:
  - platform: uswb
    id: send_updates
    uswb_id: uswb_controller
    name: "USWB11A1 Send Updates"

number:
  - platform: uswb
    id: allowed_current
    uswb_id: uswb_controller
    name: "USWB11A1 Allowed Current"
    max_current: 16
```

## Configuration variables:

Component (**uart**):

- **id** (*Optional*, [ID](https://esphome.io/guides/configuration-types.html#config-id)): Manually specify the ID used for code generation. Necessary for the sensors!
- **uart_id** (*Optional*, [ID](https://esphome.io/guides/configuration-types.html#config-id)): Manually specify the ID of the UART Component if you want to use multiple UART buses.
- **flow_control_pin** (*Optional*, [PIN](https://esphome.io/guides/configuration-types.html#config-pin)): The pin used to switch flow control. This is useful for RS485 transceivers that do not have automatic flow control switching, like the common MAX485.
- **send_wait_time** (*Optional*, [TIME](https://esphome.io/guides/configuration-types.html#config-time)): NOT USED AT THE MOMENT
- **address** (**Required**, [ID](https://esphome.io/guides/configuration-types.html#config-id)): The address of the slave device
- **update_interval** (*Optional*, [TIME](https://esphome.io/guides/configuration-types.html#config-time)): The interval that the sensors should be checked. Defaults to 10 seconds.
- **revision** (*Optional*, ENUM): The hardware revision of the wallbox. Currently only the 'A1' revision is supported - for future usage only.\
Defaults to 'A1'

Sensor:

- **uswb_id** (**Required**, [ID](https://esphome.io/guides/configuration-types.html#config-id)): The ID of the uswb component.

Number:

- **uswb_id** (**Required**, [ID](https://esphome.io/guides/configuration-types.html#config-id)): The ID of the uswb component.
- **max_current** (*Optional*, INT): The maximum allowed current. This is used to set the range of the number component and will be used as default value on startup.


## Protocol

Fields of messages (values of the example from an initial message of the master wallbox):

- **Start Sequence**: 5Ah A5h
- **Length of message**: 07h \
  (It's always 7)
- **Unknown**: 00h \
  (Always 0 - propable a second possible byte of the slaveid?)
- **SlaveId** (2-9): 02h
- **Unknown**:  02h \
  (Always 2 - function code?)
- **Question/Answer**: 01h
  - *Master*:  01h
  - *Slave*: 02h
- **Allowed/Requested Current**: 00h
  - *Master*: initial message with 0 / later the maximum allowed current (by default mostly the requested value)
  - *Slave*: the requested current (0 if not active - otherwise the maximum the wallbox and vehicle want to use for charging)
- **CRC16**: 85h E8h \
  (CRC16-Modbus as LE uint16 from the fourth byte until the end. The start sequence and the length byte are not included!)

Example message:
```
               |> CRC bytes           |
0x5A 0xA5 0x07 0x00 0x02 0x02 0x01 0x00 0x85 0xE8
|         |    |    |    |    |    |    |       |
|         |    |    |    |    |    |    |> CRC16
|         |    |    |    |    |    |> Current
|         |    |    |    |    |> Question of master
|         |    |    |    |> Unknown - Function code?
|         |    |    |> Slave id
|         |    |> Unknown
|         |> Length of following byte range
|> Start sequence
```

Communication between master and slave_id 2:
```
Master initial scan       >> 0x5A 0xA5 0x07 0x00 0x02 0x02 0x01 0x00 0x85 0xE8
Wallbox without vehicle   << 0x5A 0xA5 0x07 0x00 0x02 0x02 0x02 0x00 0x85 0x18
Master next loop          >> 0x5A 0xA5 0x07 0x00 0x02 0x02 0x01 0x00 0x85 0xE8
Wallbox request 16A       << 0x5A 0xA5 0x07 0x00 0x02 0x02 0x02 0x10 0x84 0xD4  <-- Wallbox waiting (do NOT charge)
Master allow 9A           >> 0x5A 0xA5 0x07 0x00 0x02 0x02 0x01 0x09 0x45 0xEE  <-- Charging begins with 9A
Wallbox request 16A       << 0x5A 0xA5 0x07 0x00 0x02 0x02 0x02 0x10 0x84 0xD4
Master allow 9A           >> 0x5A 0xA5 0x07 0x00 0x02 0x02 0x01 0x09 0x45 0xEE
Wallbox is ready          << 0x5A 0xA5 0x07 0x00 0x02 0x02 0x02 0x00 0x85 0x18
Master allow requested 0A >> 0x5A 0xA5 0x07 0x00 0x02 0x02 0x01 0x00 0x85 0xE8
Wallbox same response     << 0x5A 0xA5 0x07 0x00 0x02 0x02 0x02 0x00 0x85 0x18
...
```
