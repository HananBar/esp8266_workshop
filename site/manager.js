var g_tasks = new Array();
var g_groups_start = 0;
var data_keys = ["name", "number", "temperature", "time", "lights", "tv_state", "ac_state", "ac_temp"]

function reload_yaml() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://127.0.0.1:5000/reload_yaml");
  xhr.send();
}

function parse_group_response(e) {
  var debug_text = document.getElementById("debug_text");
  var xhr = e.target;
  debug_text.innerHTML += "request status: " + xhr.status + "<br>";
  debug_text.innerHTML += "raw response:<br>" + xhr.responseText + "<br><br><br>";
  if (xhr.readyState == 4 && xhr.status == 200) {
    var data = JSON.parse(xhr.responseText);
    var table_html = "<table id=\"debug_res_table\"><tr><th>Key</th><th>Value</th></tr>";
    for (var i = 0; i < data_keys.length; i += 1) {
      table_html += "<tr><td>" + data_keys[i] + "</td>";
      table_html += "<td>" + data[data_keys[i]] + "</td></tr>";
    }
    table_html += "</table>";
    debug_text.innerHTML += table_html;
  }
}

function no_response(e) {
  var xhr = e.target;
  var debug_text = document.getElementById("debug_text");
  debug_text.innerHTML += "request status " + xhr.status + "<br>";
  debug_text.innerHTML += "got no response from URL<br>";
}

function add_listeners_and_send(url) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url);
  xhr.addEventListener('load', parse_group_response);
  xhr.addEventListener('error', no_response);
  xhr.send();
}

function send_debug_bad_api() {
  var selected = document.getElementById("debug_group");
  var debug_text = document.getElementById("debug_text");
  var group_number = selected.value;
  debug_text.innerHTML = "group selected - " + group_number + "<br>";
  var url = "http://192.168.1." + (g_groups_start + parseInt(group_number)) + "/bad_api"
  debug_text.innerHTML += "sending API request to <br> " + url + "<br>";
  add_listeners_and_send(url);
}

function send_ac_api() {
  var selected = document.getElementById("debug_group");
  var debug_text = document.getElementById("debug_text");
  var group_number = selected.value;
  debug_text.innerHTML = "group selected - " + group_number + "<br>";
  selected = document.getElementById("debug_checkbox_ac");
  var ac_state = "off";
  if (selected.checked) {
    ac_state = "on";
  }
  selected = document.getElementById("debug_text_ac");
  var ac_temp = selected.value;
  var url = "http://192.168.1." + (g_groups_start + parseInt(group_number)) + "/ac?state=" + ac_state + "&temperature=" + ac_temp;
  debug_text.innerHTML += "sending API request to <br> " + url + "<br>";
  add_listeners_and_send(url);
}

function send_tv_api() {
  var selected = document.getElementById("debug_group");
  var debug_text = document.getElementById("debug_text");
  var group_number = selected.value;
  debug_text.innerHTML = "group selected - " + group_number + "<br>";
  selected = document.getElementById("debug_checkbox_tv");
  var tv_state = "off";
  if (selected.checked) {
    tv_state = "on";
  }
  var url = "http://192.168.1." + (g_groups_start + parseInt(group_number)) + "/television?state=" + tv_state;
  debug_text.innerHTML += "sending API request to <br> " + url + "<br>";
  add_listeners_and_send(url);
}

function send_lights_api(number) {
  var selected = document.getElementById("debug_group");
  var debug_text = document.getElementById("debug_text");
  var group_number = selected.value;
  debug_text.innerHTML = "group selected - " + group_number + "<br>";
  selected = document.getElementById("debug_checkbox_light_" + number);
  var light_state = "off";
  if (selected.checked) {
    light_state = "on";
  }
  var url = "http://192.168.1." + (g_groups_start + parseInt(group_number)) + "/light?number=" + number + "&state=" + light_state;
  debug_text.innerHTML += "sending API request to <br> " + url + "<br>";
  add_listeners_and_send(url);
}

function send_debug_api() {
  var selected = document.getElementById("debug_group");
  var debug_text = document.getElementById("debug_text");
  var group_number = selected.value;
  debug_text.innerHTML = "group selected - " + group_number + "<br>";
  var url = "http://192.168.1." + (g_groups_start + parseInt(group_number)) + "/json"
  debug_text.innerHTML += "sending API request to <br> " + url + "<br>";
  add_listeners_and_send(url);
}

function parse_control_response(e) {
  var debug_text = document.getElementById("debug_text");
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    var data = JSON.parse(xhr.responseText);
    debug_text.innerHTML += data['status'] + "<br>";
    lines = data['message'].split('\n');
    for (var i = 0; i < lines.length; i++) {
      debug_text.innerHTML += lines[i] + "<br>";
    }
  }
}

function send_to_server(task, number, action){
  var debug_text = document.getElementById("debug_text");
  debug_text.innerHTML = "sending " + action + " to group " + number + "<br>";
  var xhr = new XMLHttpRequest();
  if (action == 'test') {
    xhr.open("POST", "http://127.0.0.1:5000/test/" + task);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.addEventListener('load', parse_control_response);
    xhr.send("group_id=" + number + "&points=5");
  }
  if (action == 'skip') {
    xhr.open("POST", "http://127.0.0.1:5000/skip/" + task);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.addEventListener('load', parse_control_response);
    xhr.send("group_id=" + number);
  }
  if (action == 'bonus') {
    xhr.open("POST", "http://127.0.0.1:5000/bonus/" + task);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.addEventListener('load', parse_control_response);
    xhr.send("group_id=" + number + "&points=5");
  }
}

function create_button(group_number, group_task, is_bonus) {
  if (is_bonus) {
    text = "<button type=\"button\" onclick=\"send_to_server(1," + group_number + ",'bonus');\">Done 1</button>&nbsp;&nbsp;";
    text += "<button type=\"button\" onclick=\"send_to_server(2," + group_number + ",'bonus');\">Done 2</button>";
  } else {
    text = "<button type=\"button\" onclick=\"send_to_server(" + group_task+ "," + group_number + ",'test');\">Test</button>";
    text += "&nbsp;&nbsp;";
    text += "<button type=\"button\" onclick=\"send_to_server(" + group_task+ "," + group_number + ",'skip');\">Skip</button>";
    if (g_tasks[group_task - 1] == "MODE_MANUAL") {
      text = "<button type=\"button\" onclick=\"send_to_server(" + group_task+ "," + group_number + ",'skip');\">Pass</button>";
    }
  }
  return text;
}

function update_group(group_number, group_task, group_name) {
  var selected = document.getElementById("group_" + group_number);
  row_content = "<td>";
  if (group_name == "") {
    row_content += group_number;
  } else {
    row_content += group_name + " (Group " + group_number + ")";
  }
  row_content += "</td>";
  for (var i = 0; i < g_tasks.length; i += 1) {
    row_content += "<td>";
    if (group_task == i + 1) {
      row_content += create_button(group_number, group_task, false);
    }
    row_content += "</td>";
  }
  // add bonus task column
  if (group_task > g_tasks.length) {
    row_content += "<td>";
    row_content += create_button(group_number, group_task, true);
    row_content += "</td>";
  } else {
    row_content += "<td></td>";
  }
  selected.innerHTML = row_content;
}

function parse_and_update_groups(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    var data = JSON.parse(xhr.responseText);
    for (var i = 0; i < 16; i += 1) {
      update_group(i+1,
                  data['groups'][i]['current_task'],
                  data['groups'][i]['name']);
    }
  }
}

function request_groups_data() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://127.0.0.1:5000/groups");
  xhr.addEventListener('load', function(e){parse_and_update_groups(e);});
  xhr.send();
}
 
function parse_and_update_tasks(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    var data = JSON.parse(xhr.responseText);
    var table = document.getElementById("tasks_table");
    table_content = "<tr><th>Group</th>";
    for (var i=0; i < data['tasks'].length; i += 1) {
      table_content += "<th>" + data['tasks'][i]['name'] + "</th>";
      g_tasks.push(data['tasks'][i]['mode'])
    }
    // add bonus task column
    table_content += "<th>Bonus</th>";
    table_content += "</tr>";
    for (var i = 0; i < 16; i += 1) {
      table_content += "<tr id=\"group_" + (i + 1) + "\">";
      for (var j = 0; j < g_tasks.length + 1; j += 1) {
        if (j == 0) {
          table_content += "<td>" + (i + 1) + "</td>";
        } else {
          table_content += "<td></td>";
        }
      }
      // add bonus task column
      table_content += "<td></td>";
      table_content += "</tr>";
    }
    table.innerHTML = table_content;
    setInterval(function() {
      request_groups_data();
    }, 5000);
  }
}

function request_tasks_data() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://127.0.0.1:5000/tasks");
  xhr.addEventListener('load', function(e){parse_and_update_tasks(e);});
  xhr.send();
  var xhr1 = new XMLHttpRequest();
}

request_tasks_data();
