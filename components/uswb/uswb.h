#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/number/number.h"
#include "esphome/components/switch/switch.h"

#include <vector>

namespace esphome {
namespace uswb {

const std::vector<uint8_t> START_SEQ = {0x5A, 0xA5};

class UltimateSpeedWallbox : public uart::UARTDevice, public PollingComponent {
 public:
  UltimateSpeedWallbox() = default;
  
  SUB_SENSOR(requested_current)
  SUB_NUMBER(max_current)
  SUB_SWITCH(send_updates)

  void setup() override;

  void loop() override;

  void update() override;

  void dump_config() override;

  float get_setup_priority() const override;

  void send();
  void send_raw(const std::vector<uint8_t> &payload);
  void set_flow_control_pin(GPIOPin *flow_control_pin) { this->flow_control_pin_ = flow_control_pin; }
  void set_address(uint8_t address) { address_ = address; }
  void set_revision(uint8_t revision) { revision_ = revision; }
  uint8_t waiting_for_response{0};
  void set_send_wait_time(uint16_t time_in_ms) { send_wait_time_ = time_in_ms; }
  uint16_t uswb_crc16(const std::vector<uint8_t> &payload, bool payload_with_crc);

 protected:
  GPIOPin *flow_control_pin_{nullptr};

  bool parse_response_byte_(uint8_t byte);
  uint16_t send_wait_time_{250};
  uint8_t address_;
  uint8_t revision_;
  std::vector<uint8_t> rx_buffer_;
  uint32_t last_response_byte_{0};
  uint32_t last_send_{0};
};

}  // namespace uswb
}  // namespace esphome
