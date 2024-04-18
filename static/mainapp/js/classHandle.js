function changeHtml() {


    let radioGroup = document.querySelectorAll('input[type="checkbox"]');
    let details = document.getElementsByClassName("detail");
    let ele1 = document.getElementsByName("ele1");
    let ele2 = document.getElementsByName("ele2");
    let elements = [ele1, ele2];
    for (let i = 0; i < radioGroup.length; i++) {
        radioGroup[i].checked = false;
    }
    for (let i = 0; i < radioGroup.length; i++) {
        if (radioGroup[i].checked) {
            details[i].classList.add('open');
        } else {
            details[i].classList.remove('open');
        }
        radioGroup[i].addEventListener('change', function () {
            sessionStorage.setItem(this.id, this.checked);
            if (this.checked) {
                radioGroup[i].setAttribute('checked', 'checked')
                details[i].classList.add('open');
                elements[i].forEach((element) => {
                    element.style.display = "block";
                });
            } else {
                radioGroup[i].removeAttribute('checked')
                details[i].classList.remove('open');
                elements[i].forEach((element) => (element.style.display = "none"));
            }

        })
    }
}

window.onload = function () {
    changeHtml();
}