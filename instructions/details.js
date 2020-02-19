g_names = [
  "Bugs Bunny",
  "Homer Simpson",
  "Mickey Mouse",
  "Charlie Brown",
  "Fred Flintstone",
  "Popeye",
  "SpongeBob",
  "Eric Cartman",
  "Daffy Duck",
  "Scooby-Doo",
  "George Jetson",
  "Pink Panther",
  "Donald Duck",
  "Tweety Bird",
  "Winnie the Pooh",
  "Mighty Mouse",
  "The Chipmunks",
  "Spiderman",
  "Superman",
  "Batman",
]

function set_group_number(number) {
  sessionStorage.setItem("esp8266_group_number", number);
}

function get_group_number() {
  var group_number = sessionStorage.getItem("esp8266_group_number");
  if (group_number === null) {
    return "";
  }
  return group_number;
}

function set_group_name(name) {
  sessionStorage.setItem("esp8266_group_name", name);
}

function get_group_name() {
  var group_name = sessionStorage.getItem("esp8266_group_name");
  if (group_name === null) {
    return "";
  }
  return group_name;
}

function random_name() {
  return g_names[Math.floor(Math.random() * 20)];
}

function print_error(error_msg) {
  document.getElementById("error_line").innerText = error_msg
}

function save_group_name_and_number() {
  print_error("")
  var number = document.getElementById("group_number").value;
  var int_number = parseInt(number);
  if ((int_number != NaN) && (int_number <= 20) && (int_number > 0)) {
    var name = document.getElementById("group_name").value;
    if (name == "") {
      name = random_name()
    }
    set_group_name(name);
    set_group_number(number);
    window.location.href = "./tasks/task_01.html"
  } else {
    print_error("Group number should be 1-20")
  }
}

function generate_group_name() {
  document.getElementById("group_name").value = random_name();
}

function populate_name_and_number() {
  var name = get_group_name()
  var number = get_group_number()
  if ((name != "") && (number != "")) {
    document.getElementById("group_name").value = name;
    document.getElementById("group_number").value = number;
  }
}

populate_name_and_number();