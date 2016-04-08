goog.provide('Blockly.Python.ev3dev');

goog.require('Blockly.Python');

function importEv3dev() {
    Blockly.Python.definitions_['import_ev3dev'] = 'import ev3dev.ev3 as ev3';
}

Blockly.Python['ev3dev_startMotor'] = function(block) {    
    var port = block.getFieldValue('PORT');
    var speed = block.getFieldValue('SPEED');
    
    return port + "Motor.run_forever(speed_regulation='off', duty_cycle_sp=" + speed + ")\n";
}

Blockly.Python['ev3dev_connectMotor'] = function(block) {
    importEv3dev();
    
    var port = block.getFieldValue('PORT');
    
    return port + "Motor = ev3.Motor('" + port + "')\n"
        + port + "Motor.reset()\n";
}