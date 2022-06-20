const canvas = document.getElementById("canvas")
const ctx = canvas.getContext("2d")

const INITIAL_COLOR = "orange"
const INITIAL_LINECAP = "round"
const colors = document.getElementsByClassName("jsColor");
const range = document.getElementById("jsRange");
const resetBtn = document.getElementById("jsReset");
const generateBtn = document.getElementById("jsChange");
const currentColor = document.getElementById("current_color");

let lineWidth = 10;
let painting = false;
let color = INITIAL_COLOR

canvas.width = 450;
canvas.height = 450;

ctx.lineWidth = lineWidth;
ctx.lineCap = INITIAL_LINECAP;
ctx.lineJoin = "round"
ctx.strokeStyle = INITIAL_COLOR;

Array.from(colors).forEach(color =>
    color.addEventListener("click", handleColorClick));

if (range) {
    range.addEventListener("input", handleRangeChange);
}

if (canvas) {
    canvas.addEventListener("mousemove", onMouseMove)
    canvas.addEventListener("mouseup", stopPainting)
    canvas.addEventListener("mouseleave", stopPainting)
    canvas.addEventListener("mousedown", startPainting)
}

if (resetBtn){
  resetBtn.addEventListener("click", resetCanvas);
}

if (generateBtn){
    generateBtn.addEventListener("click", generatePic)
}

resetCanvas()

function resetCanvas() {
    ctx.fillStyle = "lightskyblue";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

var isRun = false;
var generated = '../intro.png';

function generatePic() {

    // ajax 통신
    $.ajax({
        type: 'POST',
        url: '',
        data: {'data':canvas.toDataURL("image/png")},
        dataType:'json',
        success: function(return_data) {
            generated = return_data["filename"]
            isRun = false;
            console.log("success!")
        },
        beforeSend: function() {
            $('html').css("cursor", "wait");
            generateBtn.removeEventListener("click", generatePic)
            generateBtn.addEventListener("click", waitInfo)
            res_ctx.fillStyle = "white";
            res_ctx.font ="30pt 서울남산체";
            isRun = true;
            delayedWaiting();
        },
        complete: function(return_data) {
            $('html').css("cursor", "auto");
            generateBtn.removeEventListener("click", waitInfo)
            generateBtn.addEventListener("click", generatePic)
            console.log("complete!")
        },
        error: function() {
            alert("에러 발생");
        }
    });

}

function waitInfo() {
    alert("이전 작업이 끝나지 않았습니다. 기다려주십시오.");
}

function sleep(ms) {
  return new Promise(
    resolve => setTimeout(resolve, ms)
  );
}

async function delayedWaiting() {
    while(isRun){
        res_ctx.fillRect(0, 0, res_canvas.width, res_canvas.height);
        var text = "잠시만 기다려주세요.";
        res_ctx.strokeText(text, 80, 270);
        await sleep(500);
        res_ctx.fillRect(0, 0, res_canvas.width, res_canvas.height);
        text = "잠시만 기다려주세요..";
        res_ctx.strokeText(text, 80, 270);
        await sleep(500);
        res_ctx.fillRect(0, 0, res_canvas.width, res_canvas.height);
        text = "잠시만 기다려주세요...";
        res_ctx.strokeText(text, 80, 270);
        await sleep(500);
    }
    var res_img = new Image();
    res_img.src = generated
    res_img.onload = function ()
    {
      res_ctx.drawImage(res_img, 0, 0, 512, 512)
    }
}

function handleColorClick(event) {
    color = event.target.style.backgroundColor;
    ctx.strokeStyle = color;
    currentColor.style.backgroundColor = color;
}

function handleRangeChange(event) {
    lineWidth = event.target.value;
    ctx.lineWidth = lineWidth;
}

function stopPainting() {
    ctx.closePath();
    painting = false;
    console.log("stop painting");
}

function startPainting(event) {
    const x = event.offsetX;
    const y = event.offsetY;
    console.log("start painting");
    drawCircle(ctx, x, y, lineWidth/4, true, false)
    ctx.moveTo(x, y);
    ctx.beginPath();
    painting = true;
}

function onMouseMove(event) {
    const x = event.offsetX;
    const y = event.offsetY;
    if (painting) {
        ctx.lineTo(x, y);
        ctx.stroke();
    }
}

function drawCircle(ctx, x, y, radius, fill, stroke) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI, false);
    ctx.lineWidth = lineWidth;
    ctx.strokeStyle = stroke;
    ctx.stroke();
    ctx.closePath();
}