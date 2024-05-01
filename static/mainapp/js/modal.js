// 要素の取得
var modal = document.getElementById("myModal");
var modalContent = modal.querySelector(".modal-content");
var btn = document.getElementById("alertBtn");
var span = document.getElementsByClassName("close")[0];
var cancelbtn = document.getElementById("cancel");
var clickArea = document.getElementById("clickArea");

clickArea.onclick = function (event) {
    var x = event.clientX; // マウスクリックのX座標
    var y = event.clientY; // マウスクリックのY座標

    // モーダルの高さと画面の高さを取得
    var modalHeight = modalContent.offsetHeight;

    var windowHeight = window.innerHeight;
    var modalWidth = modalContent.offsetWidth;
    console.log(modalWidth)
    var windowWidth = window.innerWidth;

    // 画面の下端にモーダルがはみ出さないように調整
    if (y + modalHeight > windowHeight) {
        y = windowHeight - modalHeight; // モーダルが画面下端に収まるように調整
    }
    if (x + modalWidth > windowWidth) {
        x = windowWidth - modalWidth; // モーダルが画面下端に収まるように調整
    }

    modal.style.left = x + "px";
    modal.style.top = y + "px";
    // modal.style.display = "block";
}

// ボタンクリック時の処理
btn.onclick = function () {
    modal.style.display = "block";
}

// xボタンクリックで閉じる
span.onclick = function () {
    modal.style.display = "none";
}

// xボタンクリックで閉じる
cancelbtn.onclick = function () {
    modal.style.display = "none";
}

// モーダルの外側をクリックで閉じる
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
