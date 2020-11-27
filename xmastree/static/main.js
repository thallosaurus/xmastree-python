const BRIGHTNESS_ROUTE = "set/brightness/";
const COLOR_ROUTE = "set/color/";
const STATUS_ROUTE = "status/";
const ON_ROUTE = "on/";
const OFF_ROUTE = "off/";
const ANIMATION_ROUTE = "play/";

let brightnessControl, picker, animationPicker, onBtn, offBtn;

function sendRequest(route_mask, path = "") {
  return new Promise((res, rej) => {
    fetch(route_mask + path)
      .then(response => response.json())
      .then(data => {
        // updateInputs(data)
        res(data)
      });
  });
}

window.onload = async function () {
  //let r = await sendRequest(STATUS_ROUTE);
  //console.log(r);

  picker = document.querySelector("#colorPicker");
  picker.addEventListener("change", (e) => {
    let v = e.target.value.substring(1);
    sendRequest(COLOR_ROUTE, v);
  });

  brightnessControl = document.querySelector("#brightness");
  brightnessControl.addEventListener("change", (e) => {
    let v = e.target.value;
    sendRequest(BRIGHTNESS_ROUTE, v);
  });

  animationPicker = document.querySelector("#animationPicker");
  animationPicker.addEventListener("change", (e) => {
    let v = e.target.selectedOptions[0].value;
    sendRequest(ANIMATION_ROUTE, v);
  });

  onBtn = document.querySelector("#onBtn");
  offBtn = document.querySelector("#offBtn");

  initSocket();
  
  sendRequest(STATUS_ROUTE);
  //updateInputs(r);
  //console.log(data);
}

function updateInputs(status) {
  if (status.status == 0) {
    // console.log(status);
    if (localStorage.verbose) {
      console.log(status);
    }
    picker.value = floatToHex(status.color);
    brightnessControl.value = status.brightness * 100;

    //Set color only in socket io responses
    // if (status.origin != "http") {
      document.body.style.backgroundColor = floatToHex(status.color);
    // }
    onBtn.disabled = status.on
    offBtn.disabled = !status.on

    updateTextColor(
      getContrastYIQ(
        floatToHex(status.color)
      )
    );
  } else {
    alert(status.msg);
  }
}

function on() {
  sendRequest(ON_ROUTE);
}

function off() {
  sendRequest(OFF_ROUTE);
}

// SHARED

function hexToFloat(col) {
  if (col[0] != "#") throw new Error("Colors must begin with a #-Sign");
  if (typeof col != "string") throw new Error("Color must be a string");

  let c = ("0x" + col.substring(1)).toString(16);
  let rgb = [];
  for (let i = 2; i >= 0; i--) {
    rgb.push(((c & (0xff << i * 8)) >> i * 8) / 255);
  }
  console.log(c, rgb);
  return rgb;
}

function floatToHex(f) {
  let v = 0;
  for (let i = 0; i < f.length; i++) {
    v |= (f[i] * 255) << (f.length - i - 1) * 8;
  }
  return "#" + pad(v.toString(16));
}

function pad(v) {
  let diff = 6 - v.length;
  let buf = "";
  for (let i = 0; i < diff; i++) {
      buf += "0";
  }
  return buf + v;
}

function getContrastYIQ(hexcolor){
  hexcolor = hexcolor.replace("#", "");
  var r = parseInt(hexcolor.substr(0,2),16);
  var g = parseInt(hexcolor.substr(2,2),16);
  var b = parseInt(hexcolor.substr(4,2),16);
  var yiq = ((r*299)+(g*587)+(b*114))/1000;
  return (yiq >= 128) ? 'black' : 'white';
}

function updateTextColor(color) {
  document.documentElement.style.setProperty('--text', color);
}