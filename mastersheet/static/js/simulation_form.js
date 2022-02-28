const read_file = document.getElementById("read");
const df_fields = document.getElementById("df");
const drag_fields = document.getElementById("drag");
const general_fields = document.getElementById("general_info");

const df_form = df_fields.innerHTML;
const drag_form = drag_fields.innerHTML;
const general_form = general_fields.innerHTML;

const general_files_form = '<b>File general info: <input type="file" name="general"></b>'

const force_files_form = '<b>File with downforce: <input type="file" name="df"></b>' +
              '<b>File with drag: <input type="file" name="drag"></b>'

function hideContent()
{
    if (read_file.checked) {
        general_fields.innerHTML = general_files_form;
        df_fields.innerHTML = force_files_form;
        drag_fields.innerHTML = "";
        hidden = true;
    }
    else {
        general_fields.innerHTML = general_form;
        df_fields.innerHTML = df_form;
        drag_fields.innerHTML = drag_form;
        hidden = false;
    }
}