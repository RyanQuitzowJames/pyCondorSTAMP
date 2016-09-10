function build_info_cell (cell_item, row_element) {
    var table_cell = document.createElement("td");
    var labels = cell_item["label_info"];
    for (i = 0; i < labels.length; i++) {
        var label_text = document.createElement("p");
        label_text.textContent = labels[i];
        table_cell.appendChild(label_text)
    };
    row_element.appendChild(table_cell);
};

function build_row (plotinfo_list, tableBodyID, indices = null) {
    var table_body = document.getElementById(tableBodyID);
    var table_row = document.createElement("tr");
    build_info_cell(plotinfo_list, table_row);
    var plot_subdirs = select_subinfo(plotinfo_list["plot_subdirs"], indices);
    for (i = 0; i < plot_subdirs.length; i++) {
        build_image_cell(plot_subdirs[i], table_row)
    };
    table_body.appendChild(table_row)
};

function build_cell (cell_item, row_element) {
    var table_cell = document.createElement("td");
    table_cell.textContent = cell_item;
    row_element.appendChild(table_cell);
};

function build_image_cell (cell_item, row_element) {
    var table_cell = document.createElement("td");
    row_element.appendChild(table_cell);
    var link_element = document.createElement("a");
    link_element.href = cell_item;
    table_cell.appendChild(link_element);
    var image_element = document.createElement("img");
    image_element.src = cell_item;
    image_element.height = "200";
    image_element.width = "200";
    link_element.appendChild(image_element)
};

function reset_element (element_ID) {
    var element_object = document.getElementById(element_ID);
    element_object.innerHTML = "";
};

function plotTitles (func, jsonObject, indices = null, second_arg = null, third_arg = null) {
    var plot_names = select_subinfo(jsonObject["simple_plotnames"], indices);
    for (i = 0; i < plot_names.length; i++) {
        func(plot_names[i], second_arg, third_arg)
    }
};

function build_header_row (jsonObject, tableHeadID, indices = null) {
    var table_head = document.getElementById(tableHeadID);
    var table_row = document.createElement("tr");
    build_cell("Job info", table_row);
    plotTitles(build_cell, jsonObject, indices, table_row);
    table_head.appendChild(table_row)
};

function select_subinfo (plotinfo_list, indices = null) {
    if (indices) {
        var info_subset = [];
        for (i = 0; i < indices.length; i++) {
            info_subset.push(plotinfo_list[indices[i]])
        }
    } else {
        info_subset = plotinfo_list
    };
    return info_subset
};

function build_table (jsonString, tableID, indices = null, start_plotindex = 0, single_page_limit = 25) {
    if (start_plotindex < 0) {
        start_plotindex = 0
    };
    var jsonObject = JSON.parse(jsonString);
    var table_size = jsonObject["plot_info"].length;
    var end_plotindex = start_plotindex + single_page_limit;
    if (start_plotindex < table_size) {
        if (table_size < end_plotindex) {
            end_plotindex = table_size
        };
        reset_element(tableID[1]);
        reset_element(tableID[2]);
        build_header_row(jsonObject, tableID[1], indices);
        for (j = start_plotindex; j < end_plotindex; j++) {
            build_row(jsonObject["plot_info"][j], tableID[2], indices)
        }
    } else {
        var plotnum = start_plotindex + 1;
        alert("Warning: Attempted to start viewing at plot number " + plotnum.toString() + ". Only " + table_size.toString() + " viewable plots.")
    }
};

function build_table_function (table_info, indices = null, start_plotindex = 0, single_page_limit = 25) {
    return function (jsonString) {
        build_table (jsonString, table_info, indices, start_plotindex, single_page_limit)
    }
};
