#include "current_sensor.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

namespace esphome {
namespace uswb {

static const char *const TAG = "uswb.sensor";

void UswbRequestedCurrentSensor::dump_config() {
  LOG_SENSOR(TAG, "USWB requested current sensor", this);
}

}  // namespace uswb
}  // namespace esphome
