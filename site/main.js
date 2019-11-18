
function parse_and_update_firsts(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    var data = JSON.parse(xhr.responseText);
    var table = document.getElementById("first_table");
    table_content = "";
    for (var i=0; i < data['tasks'].length; i += 1) {
      table_content += "<tr><th>" + data['tasks'][i]['name'] + "</th><td>" + data['tasks'][i]['completed_by'] + "</td></tr>";
    }
    table.innerHTML = table_content;
  }
}

function parse_and_draw_groups(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    var data = JSON.parse(xhr.responseText);
    var leaders = new Array();
    for (var i = 0; i < 16; i += 1) {
      draw_group(i+1,
                 data['groups'][i]['current_task'],
                 data['groups'][i]['points'],
                 data['groups'][i]['is_online'],
                 data['groups'][i]['current_temp'],
                 data['groups'][i]['current_time'],
                 data['groups'][i]['is_light_1_on'],
                 data['groups'][i]['is_light_2_on'],
                 data['groups'][i]['is_light_3_on'],
                 data['groups'][i]['is_ac_on'],
                 data['groups'][i]['ac_temp'],
                 data['groups'][i]['is_tv_on']);
      leaders.push(data['groups'][i]);
      var group_name = document.getElementById("group_name_" + (i+1));
      if (data['groups'][i]['name'] != "") {
        group_name.innerHTML = data['groups'][i]['name'] + " (Group " + (i+1) + ")"
      } else {
        group_name.innerHTML = "Group " + (i+1)
      }
      var debug_line = document.getElementById("text_group_" + (i+1));
      debug_log = data['groups'][i]['dbg_msg'];
      debug_lines = debug_log.split('\n');
      debug_line.innerHTML = debug_lines[debug_lines.length - 1];
    }
    leaders.sort(function(a, b){
        if (b['points'] - a['points'] == 0){
            return a['acc_time'] - b['acc_time']
            }
        return b['points'] - a['points']
        });
    var table = document.getElementById("leaders_table");
    table_content = "<tr><th>Group</th><th>Points</th></tr>";
    for (var i = 0; i < 5; i += 1) {
      if (leaders[i]['name'] != "") {
        table_content += "<tr><th>" + leaders[i]['name'] + " (Group " + leaders[i]['number'] + ")</th><td>" + leaders[i]['points'] + "</td></tr>";
      }
      else {
        table_content += "<tr><th>Group " + leaders[i]['number'] + "</th><td>" + leaders[i]['points'] + "</td></tr>";
      }
    }
    table.innerHTML = table_content;
    var d = new Date();
    document.getElementById("site_debug_2").innerHTML = "Last response:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + d.toTimeString();
  }
}

function request_groups_data() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://127.0.0.1:5000/groups");
  xhr.addEventListener('load', function(e){parse_and_draw_groups(e);});
  xhr.send();
  var xhr1 = new XMLHttpRequest();
  xhr1.open("GET", "http://127.0.0.1:5000/tasks");
  xhr1.addEventListener('load', function(e){parse_and_update_firsts(e);});
  xhr1.send();
  var d = new Date();
  document.getElementById("site_debug_1").innerHTML = "Last request sent: " + d.toTimeString();
}

intel_image = new Image();
intel_image.src = './intel.png';
intel_image.onload = function(){
  setInterval(function() {
    request_groups_data();
  }, 2000);
}
