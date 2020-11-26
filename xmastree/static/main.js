const BRIGHTNESS_ROUTE = "set/brightness/";
const COLOR_ROUTE = "set/color/";
const STATUS_ROUTE = "status/";
const ON_ROUTE = "on/";
const OFF_ROUTE = "off/";
const ANIMATION_ROUTE = "play/";

let brightnessControl, picker, animationPicker;

function sendRequest(route_mask, path = "") {
  return new Promise((res, rej) => {
    fetch(route_mask + path)
      .then(response => response.json())
      .then(data => {
        updateInputs(data)
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
  console.log(animationPicker);
  animationPicker.addEventListener("change", (e) => {
    let v = e.target.selectedOptions[0].value;
    sendRequest(ANIMATION_ROUTE, v);
  });

  let r = await sendRequest(STATUS_ROUTE);
  //updateInputs(r);
  //console.log(data);
}

function updateInputs(status) {
  if (status.status == 0) {
    console.log(status);
    picker.value = floatToHex(status.color);
    brightnessControl.value = status.brightness * 100;
    document.body.style.backgroundColor = floatToHex(status.color);
  } else {
    alert(status.msg);
  }
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