import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.cpp_helpers import gpio_pin_expression
from esphome.components import uart
from esphome.const import (
    CONF_FLOW_CONTROL_PIN,
    CONF_ID,
    CONF_ADDRESS,
    # CONF_DISABLE_CRC,
)
from esphome import pins

DEPENDENCIES = ["uart"]

uswb_ns = cg.esphome_ns.namespace("uswb")
USWB = uswb_ns.class_("UltimateSpeedWallbox", cg.PollingComponent, uart.UARTDevice)
MULTI_CONF = True

# CONF_INPUT_ID = "number_sensor_id"
CONF_SEND_WAIT_TIME = "send_wait_time"
CONF_ALLOWED_CURRENT = "allowed_current"
CONF_REVISION = "revision"
CONF_USWB_ID = "uswb_id"

REVISION = {
    "A1": 1,
    # "A2": "A2" # not supported - but message is explained in manual of USWB11A2 - feel free to implement that...
}

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(USWB),
            # cv.GenerateID(CONF_INPUT_ID): cv.use_id(HomeassistantSensor),
            cv.Optional(CONF_FLOW_CONTROL_PIN): pins.gpio_output_pin_schema,
            cv.Optional(
                CONF_SEND_WAIT_TIME, default="250ms"
            ): cv.positive_time_period_milliseconds,
            cv.Optional(CONF_REVISION, default="A1"): cv.enum(REVISION, upper=True),
            cv.Optional(CONF_ADDRESS, default=0x2): cv.hex_uint8_t,
        }
    )
    .extend(cv.polling_component_schema("10s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)

UswbItemBaseSchema = cv.Schema(
    {
        cv.GenerateID(CONF_USWB_ID): cv.use_id(USWB),
    }
)

async def to_code(config):
    cg.add_global(uswb_ns.using)
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_FLOW_CONTROL_PIN in config:
        pin = await gpio_pin_expression(config[CONF_FLOW_CONTROL_PIN])
        cg.add(var.set_flow_control_pin(pin))

    cg.add(var.set_send_wait_time(config[CONF_SEND_WAIT_TIME]))
    cg.add(var.set_address(config[CONF_ADDRESS]))
    cg.add(var.set_revision(config[CONF_REVISION]))
