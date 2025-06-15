#include "sendupdates_switch.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

namespace esphome {
namespace uswb {

static const char *const TAG = "uswb.switch";

void UswbRequestedSendUpdatesSwitch::dump_config() {
  LOG_SWITCH(TAG, "USWB switch control activation of update method", this);
}

void UswbRequestedSendUpdatesSwitch::write_state(bool state) {
  // ESP_LOGV(TAG, "USWB change update actication %s", ONOFF(state));
  publish_state(state);
}

}  // namespace uswb
}  // namespace esphome
