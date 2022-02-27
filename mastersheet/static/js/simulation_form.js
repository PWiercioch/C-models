var read_file = document.getElementById("read");
var columns = document.getElementById("columns");
var names_fields = document.getElementById("names");
var df_fields = document.getElementById("df");
var drag_fields = document.getElementById("drag");

const df_form = df_fields.innerHTML;
const drag_form = drag_fields.innerHTML;

const files_form = '<b>File general info: <input type="file" name="general"></b>' +
              '<b>File with downforce: <input type="file" name="df"></b>' +
              '<b>File with drag: <input type="file" name="drag"></b>'

function hideContent()
{
    if (read_file.checked) {
        df_fields.innerHTML = files_form;
        drag_fields.innerHTML = "";
        hidden = true;
    }
    else {
        df_fields.innerHTML = df_form;
        drag_fields.innerHTML = drag_form;
        hidden = false;
    }
}