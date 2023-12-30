import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID, DEVICE_CLASS_CURRENT, UNIT_AMPERE, STATE_CLASS_MEASUREMENT
from .. import CONF_USWB_ID, uswb_ns, UswbItemBaseSchema

UswbRequestedCurrentSensor = uswb_ns.class_("UswbRequestedCurrentSensor", sensor.Sensor, cg.Component)

CONFIG_SCHEMA = cv.All(
    sensor.sensor_schema(
        UswbRequestedCurrentSensor,
        unit_of_measurement=UNIT_AMPERE,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(UswbItemBaseSchema),
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)
    uswb_component = await cg.get_variable(config[CONF_USWB_ID])
    cg.add(uswb_component.set_requested_current_sensor(var))
