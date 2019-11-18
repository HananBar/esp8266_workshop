function draw_light(canvas_number, light_number, is_on) {
  var c = document.getElementById("canvas_group_" + canvas_number);
  var ctx = c.getContext("2d");
  var start_x = 85 + (light_number - 1) * 17;
  var start_y = 25;
  ctx.fillStyle = "rgba(0,0,0,1)";
  ctx.beginPath();
  /*ctx.moveTo(start_x + 15, start_y);
  ctx.arcTo(start_x + 5, start_y, start_x + 5, start_y + 5, 10);
  ctx.arcTo(start_x + 5, start_y + 15, start_x + 10, start_y + 15, 5);
  ctx.lineTo(start_x + 10, start_y + 20);
  ctx.arcTo(start_x + 10,start_y + 25,start_x + 15,start_y + 25,5);
  ctx.arcTo(start_x + 20,start_y + 25,start_x + 20,start_y + 20,5);
  ctx.lineTo(start_x + 20,start_y + 15);
  ctx.arcTo(start_x + 25, start_y + 15, start_x + 25, start_y + 10, 5);
  ctx.arcTo(start_x + 25, start_y, start_x + 15, start_y, 10);
  */
  ctx.arc(start_x + 7, start_y + 7, 7, 0, 2 * Math.PI);
  ctx.stroke();
  ctx.closePath();
  ctx.fillText(light_number,start_x + 3, start_y + 27);
  if (is_on) {
  ctx.fillStyle = "rgba(255,255,0,1)";
  ctx.fill();
  }
}

function draw_ac(canvas_number, is_on, temp) {
  var c = document.getElementById("canvas_group_" + canvas_number);
  var ctx = c.getContext("2d");
  var start_x = 140;
  var start_y = 20;
  var ac_width = 70;
  var ac_height = 35;
  ctx.fillStyle = "rgba(0,0,0,1)";
  ctx.beginPath();
  ctx.moveTo(start_x + 5, start_y);
  ctx.lineTo(start_x + ac_width - 5, start_y);
  ctx.arcTo(start_x + ac_width, start_y, start_x + ac_width, start_y + 5, 5);
  ctx.lineTo(start_x + ac_width, start_y + ac_height - 5);
  ctx.arcTo(start_x + ac_width, start_y + ac_height, start_x + ac_width - 5, start_y + ac_height, 5);
  ctx.lineTo(start_x + 5, start_y + ac_height);
  ctx.arcTo(start_x, start_y + ac_height, start_x, start_y + ac_height - 5, 5);
  ctx.lineTo(start_x, start_y + 5);
  ctx.arcTo(start_x, start_y, start_x + 5, start_y, 5);
  ctx.moveTo(start_x + 10, start_y + ac_height);
  ctx.lineTo(start_x + 10, start_y + ac_height - 5);
  ctx.lineTo(start_x + ac_width - 10, start_y + ac_height - 5);
  ctx.lineTo(start_x + ac_width - 10, start_y + ac_height);
  ctx.stroke();
  ctx.closePath();
  if (is_on) {
  ctx.fillStyle = "rgba(0,128,0,1)";
    ctx.fillText("On: " + temp, start_x + 15, start_y + (ac_height/2) + 3);
  } else {
  ctx.fillStyle = "rgba(255,0,0,1)";
    ctx.fillText("Off", start_x + 20, start_y + (ac_height/2) + 3);
  }
}

function draw_tv(canvas_number, is_on) {
  var c = document.getElementById("canvas_group_" + canvas_number);
  var ctx = c.getContext("2d");
  var start_x = 140;
  var start_y = 60;
  var tv_width = 70;
  var tv_height = 50;
  ctx.fillStyle = "rgba(0,0,0,1)";
  ctx.beginPath();
  ctx.moveTo(start_x, start_y);
  ctx.lineTo(start_x + tv_width, start_y);
  ctx.lineTo(start_x + tv_width, start_y + tv_height);
  ctx.lineTo(start_x, start_y + tv_height);
  ctx.lineTo(start_x, start_y);
  ctx.stroke();
  ctx.fill();
  ctx.closePath();
  ctx.lineWidth = 5;
  ctx.beginPath();
  ctx.moveTo(start_x + tv_width/2, start_y + tv_height);
  ctx.lineTo(start_x + tv_width/2, start_y + tv_height + 5);
  ctx.stroke();
  ctx.closePath();
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(start_x + tv_width/4, start_y + tv_height + 5);
  ctx.lineTo(start_x + 3*tv_width/4, start_y + tv_height + 5);
  ctx.stroke();
  ctx.closePath();
  
  if (is_on) {
    ctx.drawImage(intel_image, start_x + 5, start_y + 5);
  }
}

function draw_group(number, current_task, points, is_online, temperature, current_time, is_light_1_on, is_light_2_on, is_light_3_on, is_ac_on, ac_temp, is_tv_on) {
  var c = document.getElementById("canvas_group_" + number);
  var ctx = c.getContext("2d");
  //erase content
  ctx.clearRect(0, 0, c.width, c.height);
  ctx.beginPath();
  ctx.fillStyle = "rgba(0,0,0,1)";
  ctx.font = "16px calibri";
  ctx.fillText("Progress:",2,15);
  ctx.fillText("Points: " + points,2,35);
  //set rectangles 
  ctx.lineWidth = 1;
  ctx.strokeStyle = "rgba(0,0,0,1)";
  ctx.fillStyle = "rgba(0,128,0,1)";
  for (var i = 0; i < 10; i += 1) {
    ctx.rect(65 + i*10,5,8,10);
  if (i < current_task - 1) {
    ctx.fill();
  }
  }
  ctx.stroke();
  if (is_online == 1) {
    ctx.fillStyle = "rgba(0,128,0,1)";
    ctx.fillText("Online",2,55);
    draw_light(number, 1, is_light_1_on);
    draw_light(number, 2, is_light_2_on);
    draw_light(number, 3, is_light_3_on);
    draw_ac(number, is_ac_on, ac_temp);
    draw_tv(number, is_tv_on);
    ctx.fillStyle = "rgba(0,0,0,1)";
    ctx.fillText("Temp: " + temperature,2,75);
    ctx.fillText("Time: " + current_time,2,95);
  } else {
    if (is_online == 0) {
      ctx.fillStyle = "rgba(255,0,0,1)";
      ctx.fillText("Offline",2,55);
    } else {
      ctx.fillStyle = "rgba(255,128,64,1)";
      ctx.fillText(is_online,2,55);
    }
  }
}
