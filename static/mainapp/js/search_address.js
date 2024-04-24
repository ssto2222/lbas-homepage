let search = document.getElementById("zipcode");
search.addEventListener(
    "change",
    () => {
        let api = "https://zipcloud.ibsnet.co.jp/api/search?zipcode=";
        let error = document.getElementById("error");
        // let input = document.getElementById("zipcode");
        let address1 = document.getElementById("address1");
        let address2 = document.getElementById("address2");
        let address3 = document.getElementById("address3");

        let prefSelect = document.getElementById('pref_name');
        let options = prefSelect.options;

        let param = search.value.replace("-", ""); //入力された郵便番号から「-」を削除
        let url = api + param;
        fetchJsonp(url, {
            timeout: 10000, //タイムアウト時間
        })
            .then((response) => {
                error.textContent = ""; //HTML側のエラーメッセージ初期化
                return response.json();
            })
            .then((data) => {
                if (data.status === 400) {
                    //エラー時

                } else if (data.results === null) {
                    error.textContent = "郵便番号から住所が見つかりませんでした。";
                } else {
                    address1.value = data.results[0].address1;
                    for (let i = 0; i < options.length; i++) {
                        if (options[i].innerText === data.results[0].address1) {
                            options[i].selected = true;
                        }
                    }


                    address2.value = data.results[0].address2;
                    address3.value = data.results[0].address3;
                }
            })
            .catch((ex) => {
                //例外処理
                console.log(ex);
            });
    },
    false
);

let prefSelect = document.getElementById('pref_name');
prefSelect.addEventListener('change', () => {
    let address1 = document.getElementById("address1");
    let selectedIndex = prefSelect.selectedIndex
    address1.value = prefSelect.options[selectedIndex].innerText
})

// input要素のvalueを取得
let inputVal = document.getElementById("address1").value;
// select要素を取得

// option要素の数を取得
let optionCount = prefSelect.options.length;

// option要素をループ処理して、value値が一致するoption要素をselectedに設定
for (let i = 0; i < optionCount; i++) {
    let optionElem = prefSelect.options[i];
    if (optionElem.value === inputVal) {
        optionElem.selected = true;
        break;
    }
}


//address → zipcode
$(document).ready(function () {
    $("#search").on("click", function () {
        const pref = $("input#address1").val();
        const city = $("input#address2").val();
        const addr = $("input#address3").val();
        const error = $("#error")
        const address = pref + city + addr;

        $.ajax({
            url: "https://zipcoda.net/api",
            dataType: "jsonp",
            data: {
                address: address
            }
        }).then((data) => {
            console.log(data)
            if (data.status === 400 || data.status === 500) {
                //エラー時
                error.textContent = "住所を町域まで入力してください。";
            } else if (data.items === null) {
                error.textContent = "住所から郵便番号が見つかりませんでした。";
            } else {
                const zip = data.items[0].zipcode;
                $("input#zipcode").val(zip);
            }
        });
    });

    // $("#to-addr").on("click", function () {

    //     const zip = $("input#zip").val();

    //     $.ajax({
    //         url: "https://zipcoda.net/api",
    //         dataType: "jsonp",
    //         data: {
    //             zipcode: zip
    //         }
    //     }).then((data) => {
    //         const pref = data.items[0].components[0];
    //         const city = data.items[0].components[1];
    //         const addr = data.items[0].components[2];
    //         $("input#prefecture").val(pref);
    //         $("input#city").val(city);
    //         $("input#address").val(addr);
    //     });

    // });
});