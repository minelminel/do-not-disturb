const APP_DIV = document.getElementById('app');
const API_URL = '/api';
const colorFree = 'forestgreen';
const colorBusy = 'tomato';

function toggleStatus(key) {
    console.log(`toggle: ${key}`);
    const HTTP = new XMLHttpRequest();
    HTTP.open('POST', `${API_URL}?name=${key}`);
    HTTP.send();
    init();
};

function makeBox(key, obj) {
    console.log(`key: ${key} value: ${JSON.stringify(obj)}`);
    const bgColor = obj.doNotDisturb ? colorBusy : colorFree;
    return `<div class="box" style="background-color: ${bgColor}" onclick="toggleStatus('${key}')" >${obj.name}</div>`;
};

function init() {
    APP_DIV.innerHTML = '';
    fetch(API_URL)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            for (const [key, obj] of Object.entries(data)) {
                APP_DIV.innerHTML += makeBox(key, obj);
            };
        })
        .catch(error => {
            console.error(error);
            APP_DIV.innerHTML += `<div style="background-color: red" >Error Fetching Data</div>`
        });
};

window.addEventListener('load', init);
