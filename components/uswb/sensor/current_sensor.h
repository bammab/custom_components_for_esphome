#pragma once

#include "esphome/components/sensor/sensor.h"
#include "esphome/core/component.h"

namespace esphome {
namespace uswb {

class UswbRequestedCurrentSensor : public Component, public sensor::Sensor {
 public:
  void dump_config() override;

 protected:
};

}  // namespace uswb
}  // namespace esphome
