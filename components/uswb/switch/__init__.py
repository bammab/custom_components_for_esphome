import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, ENTITY_CATEGORY_CONFIG
from .. import CONF_USWB_ID, uswb_ns, UswbItemBaseSchema

UswbRequestedSendUpdatesSwitch = uswb_ns.class_("UswbRequestedSendUpdatesSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = cv.All(
    switch.switch_schema(
        UswbRequestedSendUpdatesSwitch,
        # entity_category=ENTITY_CATEGORY_CONFIG, # entity_category: config
        default_restore_mode = "ALWAYS_ON",
        )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(UswbItemBaseSchema),
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await switch.register_switch(var, config)
    uswb_component = await cg.get_variable(config[CONF_USWB_ID])
    cg.add(uswb_component.set_send_updates_switch(var))
