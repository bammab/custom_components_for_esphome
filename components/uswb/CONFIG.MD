external_components:
  # - source:
  #     type: git
  #     url: https://github.com/bammab/custom_components_for_esphome
  #     ref: main
  #     username: OPTIONAL_USER
  #     password: OPTIONAL_PWD
  #   components: [ uswb ]

  - source:
      type: local
      path: local_components

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
