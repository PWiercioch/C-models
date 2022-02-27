function hideContent()
{
    if (read_file.checked) {
        columns.innerHTML = names_div;
        hidden = true;
        files.style.visibility = "visible";
    }
    else {
        columns.innerHTML = names_div + df_div + drag_div;
        hidden = false;
        files.style.visibility = "hidden";
    }
}