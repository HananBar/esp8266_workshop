function get_group_number() {
  var group_number = sessionStorage.getItem("esp8266_group_number");
  if (group_number === null) {
    return "";
  }
  return group_number;
}

function get_group_name() {
  var group_name = sessionStorage.getItem("esp8266_group_name");
  if (group_name === null) {
    return "";
  }
  return group_name;
}

function populate_group_name_and_number() {
  var group_number = get_group_number();
  var numbers = document.getElementsByClassName("group_number");
  for (i = 0; i < numbers.length; i += 1) {
    numbers[i].innerText = group_number;
  }
  var group_name = get_group_name();
  var names = document.getElementsByClassName("group_name");
  for (i = 0; i < names.length; i += 1) {
    names[i].innerText = group_name;
  }
  var links = document.getElementsByClassName("group_number_link");
  for (i = 0; i < links.length; i += 1) {
    var href = links[i].getAttribute("href");
    links[i].href = "http://192.168.1." + group_number + href;
  }
}

function show_step(next_step) {
  var divs = document.getElementsByClassName("step");
  for (i = 0; i < divs.length; i += 1) {
    if (divs[i].id == next_step) {
      divs[i].style.display = "block";
    } else {
      divs[i].style.display = "none";
    }
  }
  scroll(0,0);
}

function log_to_test_text(str, clear) {
  var test_text = document.getElementById("test_text");
  var text = "";
  if (clear == false) {
    var text = test_text.value + "\n";
  }
  test_text.value = text + str;
}

function log_to_server_test_text(str, clear) {
  var test_text = document.getElementById("server_test_text");
  var text = "";
  if (clear == false) {
    var text = test_text.value + "\n";
  }
  test_text.value = text + str;
}

function no_response(e) {
  var xhr = e.target;
  log_to_test_text("request status " + xhr.status, false);
  log_to_test_text("got no response from URL", false);
}

function add_listeners_and_send(url, parser) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url);
  xhr.onreadystatechange = function () {
    if (this.readyState == 4) {
      if (this.status == 404) {
        log_to_test_text("404 detected", false);
        log_to_test_text(xhr.responseText, false);
      }
    }
  }
  xhr.addEventListener('load', parser);
  xhr.addEventListener('error', no_response);
  xhr.send();
}

function parse_time(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    log_to_test_text("got response!", false);
    log_to_test_text(xhr.responseText, false);
    var data = JSON.parse(xhr.responseText);
    log_to_test_text("looking for \"time\" element", false);
    log_to_test_text(data["time"], false);
  }
}

function try_time() {
  var group_number = get_group_number();
  // send request:
  var url = "http://192.168.1." + group_number + "/json";
  log_to_test_text("sending request to:\n" + url, true);
  add_listeners_and_send(url, parse_time);
}

function parse_temp(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    log_to_test_text("got response!", false);
    log_to_test_text(xhr.responseText, false);
    var data = JSON.parse(xhr.responseText);
    log_to_test_text("looking for \"temperature\" element", false);
    log_to_test_text(data["temperature"], false);
  }
}

function try_temp() {
  var group_number = get_group_number();
  // send request:
  var url = "http://192.168.1." + group_number + "/json";
  log_to_test_text("sending request to:\n" + url, true);
  add_listeners_and_send(url, parse_temp);
}

function parse_light(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    log_to_test_text("got response!", false);
    log_to_test_text(xhr.responseText, false);
    var data = JSON.parse(xhr.responseText);
    log_to_test_text("looking for \"lights\" element", false);
    log_to_test_text(data["lights"], false);
  }
}

function try_light(number, state) {
  var group_number = get_group_number();
  // send request:
  var state_text = "off";
  if (state == 1) {
    state_text = "on";
  }
  var url = "http://192.168.1." + group_number + "/light?number=" + number + "&state=" + state_text;
  log_to_test_text("sending request to:\n" + url, true);
  add_listeners_and_send(url, parse_light);
}

function parse_tv(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    log_to_test_text("got response!", false);
    log_to_test_text(xhr.responseText, false);
    var data = JSON.parse(xhr.responseText);
    log_to_test_text("looking for \"tv_state\" element", false);
    log_to_test_text(data["tv_state"], false);
  }
}

function try_tv(state) {
  var group_number = get_group_number();
  // send request:
  var state_text = "off";
  if (state == 1) {
    state_text = "on";
  }
  var url = "http://192.168.1." + group_number + "/television?state=" + state_text;
  log_to_test_text("sending request to:\n" + url, true);
  add_listeners_and_send(url, parse_tv);
}

function parse_ac(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    log_to_test_text("got response!", false);
    log_to_test_text(xhr.responseText, false);
    var data = JSON.parse(xhr.responseText);
    log_to_test_text("looking for \"ac_state\" element", false);
    log_to_test_text(data["ac_state"], false);
    log_to_test_text("looking for \"ac_temp\" element", false);
    log_to_test_text(data["ac_temp"], false);
  }
}

function try_ac(state) {
  var temperature = document.getElementById("ac_temp").value;
  var group_number = get_group_number();
  // send request:
  var state_text = "off";
  if (state == 1) {
    state_text = "on";
  }
  var url = "http://192.168.1." + group_number + "/ac?state=" + state_text + "&temperature=" + temperature;
  log_to_test_text("sending request to:\n" + url, true);
  add_listeners_and_send(url, parse_ac);
}

function test_parser(e) {
  var xhr = e.target;
  if (xhr.readyState == 4 && xhr.status == 200) {
    var data = JSON.parse(xhr.responseText);
    log_to_server_test_text(data['status'], false);
    log_to_server_test_text(data['message'], false);
    if (data['status'] == "passed") {
      // enable "next task" button
      document.getElementById("next_task").disabled = false;
    }
  }
}

function test_me_common(task, points, group_id){
  var group_number = get_group_number();
  var xhr = new XMLHttpRequest();
  //xhr.open("POST", "http://192.168.1.100:5000/test/" + task);
  xhr.open("POST", "http://127.0.0.1:5000/test/" + task);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.addEventListener('load', test_parser);
  xhr.addEventListener('error', no_response);
  xhr.send("group_id=" + group_id + "&points=" + points);
}

function test_me(task, points){
  var group_number = get_group_number();
  log_to_server_test_text("Testing group:" + group_number + " - Task:" + task, true);
  test_me_common(task, points, group_number);
}

function test_me_overloaded(task, points, testing_ip){
  log_to_server_test_text("Task:" + task + ", Trying to test using 192.168.1." + testing_ip, true);
  var group_number = get_group_number();
  log_to_server_test_text("Testing group:" + group_number + " - Task:" + task, false);
  group_number = (testing_ip << 8) | group_number;
  test_me_common(task, points, group_number);
}

show_step("step01");
populate_group_name_and_number();
