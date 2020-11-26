const BRIGHTNESS_ROUTE = "set/brightness/";
const COLOR_ROUTE = "set/color/";
const STATUS_ROUTE = "status/";
const ON_ROUTE = "on/";
const OFF_ROUTE = "off/";

let brightnessControl, picker;

function sendRequest(route_mask, path = "") {
  return new Promise((res, rej) => {
    fetch(route_mask + path)
      .then(response => response.json())
      .then(data => res(data));
  });
}

window.onload = async function() {
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

  let r = await sendRequest(STATUS_ROUTE);
  updateInputs(r);
  //console.log(data);
}

function updateInputs(status) {
  picker.value = floatToHex(status.color);
  brightnessControl.value = status.brightness;
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
    return "#" + v.toString(16);
}
