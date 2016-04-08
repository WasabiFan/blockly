goog.provide('Blockly.Blocks.ev3dev');

goog.require('Blockly.Blocks');

Blockly.Blocks['ev3dev_connectMotor'] = {
    init: function() {
        this.setPreviousStatement(true);
        this.setNextStatement(true);
        this.setColour(30);
        
        this.appendDummyInput()
            .appendField('connect to motor')
            .appendField('on port')
            .appendField(new Blockly.FieldTextInput('outA'), 'PORT');
        
        this.setTooltip('Connects to the motor on the specified port for future use.');
    }
}

Blockly.Blocks['ev3dev_startMotor'] = {
    init: function() {
        this.setPreviousStatement(true);
        this.setNextStatement(true);
        this.setColour(30);
        
        this.appendDummyInput()
            .appendField('start motor')
            .appendField('on port')
            .appendField(new Blockly.FieldTextInput('outA'), 'PORT');
        
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("at speed")
            .appendField(new Blockly.FieldTextInput('500', Blockly.FieldTextInput.numberValidator), 'SPEED');
        
        this.setTooltip('Starts the specified motor with the specified speed.');
    }
}