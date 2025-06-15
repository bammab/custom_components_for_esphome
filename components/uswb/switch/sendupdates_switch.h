#pragma once

#include "esphome/components/switch/switch.h"
#include "esphome/core/component.h"

namespace esphome {
namespace uswb {

class UswbRequestedSendUpdatesSwitch : public Component, public switch_::Switch {
 public:
  void dump_config() override;

 protected:
  void write_state(bool state) override;
};

}  // namespace uswb
}  // namespace esphome
