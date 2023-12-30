#pragma once

#include "esphome/components/number/number.h"
#include "esphome/core/component.h"
#include "../uswb.h"

namespace esphome {
namespace uswb {

class UswbAllowedCurrentNumber : public number::Number, public Component, public Parented<UltimateSpeedWallbox> {
 public:
  UswbAllowedCurrentNumber() = default;
  void dump_config() override;

 protected:
  void control(float max_current) override;
};

}  // namespace uswb
}  // namespace esphome
