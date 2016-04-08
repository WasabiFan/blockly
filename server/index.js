var workspace = null;

function initBlockly() {
    var toolbox = $('#toolbox');
    workspace = Blockly.inject('blocklyDiv', {
        toolbox: toolbox[0],
    });
}

function runCode() {
    var generatedCode = Blockly.Python.workspaceToCode(workspace);
    $.post("/save-and-execute", { fileName: "my_file.py", code: generatedCode }).done(function (data) {
        alert(data);
    });
}