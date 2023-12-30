#include "uswb.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"

namespace esphome {
namespace uswb {

static const char *const TAG = "uswb";

void UltimateSpeedWallbox::setup() {
  if (this->flow_control_pin_ != nullptr) {
    this->flow_control_pin_->setup();
  }
  if (this->max_current_number_ != nullptr) {
    float state = max_current_number_->traits.get_max_value();
    this->max_current_number_->publish_state(state > 0 ? state : 16);
  }
  if (this->requested_current_sensor_ != nullptr) {
    this->requested_current_sensor_->publish_state(0);
  }
}
void UltimateSpeedWallbox::loop() {
  const uint32_t now = millis();

  if (now - this->last_response_byte_ > 50) {
    this->rx_buffer_.clear();
    this->last_response_byte_ = now;
  }
  // stop blocking new send commands after send_wait_time_ ms regardless if a response has been received since then
  if (now - this->last_send_ > send_wait_time_) {
    waiting_for_response = 0;
  }

  while (this->available()) {
    uint8_t byte;
    this->read_byte(&byte);
    if (this->parse_response_byte_(byte)) {
      this->last_response_byte_ = now;
    } else {
      this->rx_buffer_.clear();
    }
  }
}

void UltimateSpeedWallbox::update() { this->send(); }

bool UltimateSpeedWallbox::parse_response_byte_(uint8_t byte) {
  size_t at = this->rx_buffer_.size();
  this->rx_buffer_.push_back(byte);
  ESP_LOGV(TAG, "USWB received Byte  %d (0X%x)", byte, byte);

  if (at == 0)
    return this->rx_buffer_.at(0) == START_SEQ.at(0);

  if (at == 1)
    return this->rx_buffer_.at(1) == START_SEQ.at(1);

  // Load until all bytes are loaded (message length is in byte 3 after start sequence)
  if (at > 1 && at < (this->rx_buffer_.at(2) + START_SEQ.size())) {
    return true;
  }

  // ESP_LOGD(TAG, "Got full message - check crc: %s", format_hex_pretty(rx_buffer_).c_str());

  uint16_t computed_crc = uswb_crc16(rx_buffer_, true);
  uint16_t remote_crc = uint16_t(rx_buffer_.at(at-1)) | (uint16_t(rx_buffer_.at(at)) << 8);

  if (computed_crc != remote_crc) {
    ESP_LOGW(TAG, "CRC16-Modbus Check failed! %02X!=%02X", computed_crc, remote_crc);
    return false;
  }

  uint8_t address = rx_buffer_.at(4);
  float state = static_cast<float>(rx_buffer_.at(7));

  if (this->address_ == address) {
    if (this->requested_current_sensor_ != nullptr) {
      if (!requested_current_sensor_->has_state() || (
        requested_current_sensor_->has_state() &&
        requested_current_sensor_->get_state() != state
      ))
      requested_current_sensor_->publish_state(state);
      // Reset allowed max current if we plug in new vehicle and want to charge - TODO: really a good idea?!
      // if (requested_current_sensor_->get_state() == 0 && state > 0) {
      //   float state = max_current_number_->traits.get_max_value();
      //   state = state > 0 ? state : 16;
      //   ESP_LOGW(TAG, "New charging process - reset max allowd to %.0f! ", state);
      //   this->max_current_number_->publish_state(state);
      // }
    }
  } else {
    ESP_LOGW(TAG, "Got response frame from unknown address 0x%02X! ", address);
  }

  waiting_for_response = 0;

  // return false to reset buffer
  return false;
}

void UltimateSpeedWallbox::dump_config() {
  ESP_LOGCONFIG(TAG, "USWB:");
  LOG_PIN("  Flow Control Pin: ", this->flow_control_pin_);
  ESP_LOGCONFIG(TAG, "  Send Wait Time: %d ms", this->send_wait_time_);
  ESP_LOGCONFIG(TAG, "  Address: %d", this->address_);
  ESP_LOGCONFIG(TAG, "  Revision: %d", this->revision_);
}

float UltimateSpeedWallbox::get_setup_priority() const {
  // After UART bus
  return setup_priority::BUS - 1.0f;
}

void UltimateSpeedWallbox::send() {
  // Start of Frame      Len                 SlaveId   Func?     Q/A                 CRC16 Modbus (LE uint16)
  // 5Ah       A5h       07h       00h       02h       02h       01h       00h       85h       E8h      
  std::vector<uint8_t> data;
  data.insert(data.begin(), START_SEQ.begin(), START_SEQ.end());
  data.push_back(0x7);
  data.push_back(0x0);
  data.push_back(address_);
  data.push_back(0x2);
  data.push_back(0x1);
  if (requested_current_sensor_ != nullptr && requested_current_sensor_->has_state()) {
    float allowed = requested_current_sensor_->get_state();
    if (max_current_number_ != nullptr && max_current_number_->has_state()) {
      float max_allowed = max_current_number_->state;
      allowed = max_allowed > allowed ? allowed : max_allowed;
    }
    // ESP_LOGD(TAG, "USWB send - allowed %.2f", allowed);
    data.push_back(allowed);
  } else { // initial value
    data.push_back(0x0);
  }

  auto crc = uswb_crc16(data, false);
  data.push_back(crc >> 0);
  data.push_back(crc >> 8);

  send_raw(data);
}

// Helper function for lambdas
// Send raw command. Everything must be contained in payload
void UltimateSpeedWallbox::send_raw(const std::vector<uint8_t> &payload) {
  if (payload.empty()) {
    return;
  }

  if (this->flow_control_pin_ != nullptr)
    this->flow_control_pin_->digital_write(true);

  this->write_array(payload);
  this->flush();

  if (this->flow_control_pin_ != nullptr)
    this->flow_control_pin_->digital_write(false);
  waiting_for_response = payload[0];
  ESP_LOGV(TAG, "Write payload: %s", format_hex_pretty(payload).c_str());
  last_send_ = millis();
}

uint16_t UltimateSpeedWallbox::uswb_crc16(const std::vector<uint8_t> &payload, bool payload_with_crc) {
  if (payload.size() < 5) {
    ESP_LOGW(TAG, "USWB-Crc16 - payload to small");
    return 0;
  }
  return crc16(payload.data() + 3, payload.size() - 3 - (payload_with_crc ? 2 : 0));
}

}  // namespace uswb
}  // namespace esphome
