import esphome.codegen as cg
from esphome.components import number
import esphome.config_validation as cv
from esphome.const import (
    CONF_MAX_CURRENT,
    UNIT_AMPERE,
    DEVICE_CLASS_CURRENT,
    CONF_ID,
)
from .. import CONF_USWB_ID, uswb_ns, UswbItemBaseSchema

UswbAllowedCurrentNumber = uswb_ns.class_("UswbAllowedCurrentNumber", cg.Component, number.Number)

CONFIG_SCHEMA = cv.All(
    number.number_schema(
        UswbAllowedCurrentNumber,
        unit_of_measurement=UNIT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    )
    .extend(UswbItemBaseSchema)
    .extend(
        {
            cv.Optional(CONF_MAX_CURRENT, default=0x0): cv.positive_int,
        }
    ),
)

async def to_code(config):
    # Using new_number (new_Pvariable + register_number)
    # var = await number.new_number(
    #     config,
    #     min_value=0,
    #     max_value=config[CONF_MAX_CURRENT],
    #     step=1,
    # )
    # await cg.register_component(var, config)
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await number.register_number(
        var,
        config,
        min_value=0,
        max_value=config[CONF_MAX_CURRENT],
        step=1,
    )

    uswb_component = await cg.get_variable(config[CONF_USWB_ID])        
    await cg.register_parented(var, config[CONF_USWB_ID])
    cg.add(uswb_component.set_max_current_number(var))
