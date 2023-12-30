#include "max_current_number.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

namespace esphome {
namespace uswb {

static const char *const TAG = "uswb.number";

void UswbAllowedCurrentNumber::control(float allowed_current) {
  // this->parent_->set_max_current((uint8_t) allowed_current)
  this->publish_state(allowed_current);
}
void UswbAllowedCurrentNumber::dump_config() { LOG_NUMBER(TAG, "USWB allowed current number", this); }

}  // namespace uswb
}  // namespace esphome
