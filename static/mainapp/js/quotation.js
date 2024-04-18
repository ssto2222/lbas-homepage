let saveStrage = document.getElementById("save");
let customerName = document.getElementById("customer-name");
let email = document.getElementById("email");
let tel = document.getElementById("tel");
let zipcode = document.getElementById("zipcode");
let address2 = document.getElementById("address2");
let address3 = document.getElementById("address3");
let address4 = document.getElementById("address4");
let area = document.getElementById("area");


let prefOpts = document.getElementById('pref_name').options;
let buildingOpts = document.getElementById("building-selection").options;
let roomOpts = document.getElementById("rooms-selection").options;
let floorOpts = document.getElementById("floor-selection").options;
let elevatorOpts = document.getElementById("elevator-selection").options;
let equipmentOpts = document.getElementById("equipment-selection").options;
let date = document.getElementById("date");

let formData = document.getElementById('form').elements;

let checkboxGroup = document.querySelectorAll('input[type="checkbox"]');
let selectedValues = [];
console.log(checkboxGroup[0].checked)

function saveFormData() {
  sessionStorage.setItem('name', customerName.value);
  sessionStorage.setItem('email', email.value);
  sessionStorage.setItem('tel', tel.value);
  sessionStorage.setItem('zipcode', zipcode.value);
  sessionStorage.setItem('address1', getSelected(prefOpts));
  sessionStorage.setItem('address2', address2.value);
  sessionStorage.setItem('address3', address3.value);
  sessionStorage.setItem('address4', address4.value);
  sessionStorage.setItem('area', area.value);
  sessionStorage.setItem('date', date.value);
  if (checkboxGroup[0].checked) {
    sessionStorage.setItem('building', getSelected(buildingOpts));
    sessionStorage.setItem('room', getSelected(roomOpts));
    sessionStorage.setItem('floor', getSelected(floorOpts));
    sessionStorage.setItem('elevator', getSelected(elevatorOpts));
  } else {
    sessionStorage.removeItem('building', getSelected(buildingOpts));
    sessionStorage.removeItem('room', getSelected(roomOpts));
    sessionStorage.removeItem('floor', getSelected(floorOpts));
    sessionStorage.removeItem('elevator', getSelected(elevatorOpts));
  }
  if (checkboxGroup[1].checked) {

    sessionStorage.setItem('equipment', getSelected(equipmentOpts));
  } else {
    sessionStorage.removeItem('equipment', getSelected(equipmentOpts));
  }
}



function loadStrageData() {
  for (let i = 0; i < formData.length; i++) {
    formData[i].value = sessionStorage.getItem(formData[i].name);
  }
  loadCheckboxData();

  setSelected(prefOpts, sessionStorage.getItem('address1'))
  if (checkboxGroup[0].checked) {
    setSelected(buildingOpts, sessionStorage.getItem('building'))
    setSelected(floorOpts, sessionStorage.getItem('floor'))
    setSelected(roomOpts, sessionStorage.getItem('room'))
    setSelected(elevatorOpts, sessionStorage.getItem('elevator'))
  } else {
    setSelected(buildingOpts, null)
    setSelected(floorOpts, null)
    setSelected(roomOpts, null)
    setSelected(elevatorOpts, null)

  }
  if (checkboxGroup[1].checked) {
    setSelected(equipmentOpts, sessionStorage.getItem('equipment'))
  } else {
    setSelected(equipmentOpts, null)
  }
}

function loadCheckboxData() {
  // チェックボックスグループを取得
  // sessionStorageから保存された選択状態を取得
  selectedValues = JSON.parse(sessionStorage.getItem("checkboxGroup"))

  // sessionStorageから取得した選択状態に応じてチェックボックスをオンオフ
  for (let i = 0; i < checkboxGroup.length; i++) {
    checkboxGroup[i].checked = selectedValues[i];
  }
}

// チェックボックスのチェンジイベント
for (let i = 0; i < checkboxGroup.length; i++) {
  checkboxGroup[i].addEventListener("change", function () {
    // チェックボックスグループから選択状態を取得
    if (this.checked) {
      selectedValues.push(true)
    } else {
      selectedValues.push(false)
    }
  })
}

// sessionStorageに選択状態を保存
sessionStorage.setItem("checkboxGroup", JSON.stringify(selectedValues));

function setSelected(options, getData) {
  for (let i = 0; i < options.length; i++) {
    if (options[i].innerText === getData) {
      options[i].selected = true;
    }
  }
}

function getSelected(optionsArray) {
  try {
    let index = optionsArray.selectedIndex;
    selected = optionsArray[index].value;
    return selected;
  } catch (err) {
    console.log(err, "optionsArray is undefined.")
    return null;
  }

}

function loadDate() {
  let defaultDate = new Date();
  defaultDate.setDate(defaultDate.getDate() + 14);
  let yyyy = defaultDate.getFullYear();
  let mm = ("0" + (defaultDate.getMonth() + 1)).slice(-2);
  let dd = ("0" + defaultDate.getDate()).slice(-2);
  document.getElementById("date").value = yyyy + "-" + mm + "-" + dd;
}


loadStrageData();



window.onload = function () {
  // ページロード時にsessionStorageからラジオボタンの選択状態を再表示

  loadDate();



}



