const inputContainer = document.getElementById('inputContainer');
const meterReading = document.getElementById('meterReading');
const waterCost = document.getElementById('waterCost');
const advance = document.getElementById('advance');
const submitBtn = document.getElementById('submitBtn');

const submitSound = document.getElementById('submitSound');

const resultContainer = document.getElementById('resultContainer');
const date= document.getElementById('date');
const thisMonth = document.getElementById('thisMonth');
const lastMonth = document.getElementById('lastMonth');
const unitConsumed = document.getElementById('unitConsumed');
const money = document.getElementById('money');
const waterCostDis = document.getElementById('waterCostDis');
const total = document.getElementById('tMoney');
const advanceDis = document.getElementById('advanceDis');
const grandTotal = document.getElementById('gtMoney');

const detailsBtn = document.getElementById('detailsBtn');
const detailsSlideArea = document.getElementById('detailsSlideArea');

const detailsBackButton = document.getElementById('detailsBackButton');

const monthSelect = document.getElementById('month');

const searchContainer = document.getElementById('searchContainer');
const nfMsg = document.getElementById('nfMsg');
const errMsg = document.getElementById('errMsg');


submitBtn.addEventListener('click', () => {
    submitSound.play();
    inputContainer.style.display = 'none';
    resultContainer.style.display = 'flex';
    const thisMR = meterReading.value;
    const wCost = waterCost.value;
    const adv = advance.value;
    fetch('/mr', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'cm_reading':thisMR, 
            'water_m':wCost, 
            'advance':adv
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success'){
            date.textContent = data.date;
            thisMonth.textContent = data.thismr;
            lastMonth.textContent = data.lastmr;
            unitConsumed.textContent = data.unit_consumed;
            money.textContent = data.money;
            waterCostDis.textContent = data.watercost;
            total.textContent = data.tmoney;
            advanceDis.textContent = data.advance;
            grandTotal.textContent = data.gt_money;
        }
    })
    .catch(error => {
        console.error('Error checking turn:', error);
    });
    
});

detailsBtn.addEventListener('click', () => {
    slideFunction(detailsSlideArea);
    fetch('/years',{
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success'){
            const yearSelect = document.getElementById('year');
            yearSelect.innerHTML = '';
            const yearList = data.years;
            yearList.forEach(year => {
                var option = document.createElement('option');
                option.value = year;
                option.textContent = year;
                yearSelect.appendChild(option);
            });
            checkSearch();
            setInterval(checkSearch, 500);
        }
    })
    .catch(error => {
        console.error('Error checking turn:', error);
    });
});

detailsBackButton.addEventListener('click', () => {
    slideFunction(detailsSlideArea);
});


function checkSearch(){
    var month = monthSelect.value;
    var year = document.getElementById('year').value;
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'month':month, 'year':year})
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success'){
            nfMsg.style.display = 'none';
            searchContainer.style.display = 'block';
            document.getElementById('SthisMonth').textContent = data.thismr;
            document.getElementById('SlastMonth').textContent = data.lastmr;
            document.getElementById('SunitConsumed').textContent = data.unit_consumed;
            document.getElementById('Smoney').textContent = data.money;
            document.getElementById('SwaterCostDis').textContent = data.watercost;
            document.getElementById('StMoney').textContent = data.tmoney;
            document.getElementById('SadvanceDis').textContent = data.advance;
            document.getElementById('SgtMoney').textContent = data.gt_money;
        }
        else if(data.status === 'nf'){
            searchContainer.style.display = 'none';
            nfMsg.style.display = 'block';
        }
        else{
            document.getElementById('SthisMonth').textContent = 'N/A';
            document.getElementById('SlastMonth').textContent = 'N/A';
            document.getElementById('SunitConsumed').textContent = 'N/A';
            document.getElementById('Smoney').textContent = 'N/A';
            document.getElementById('SwaterCostDis').textContent = 'N/A';
            document.getElementById('StMoney').textContent = 'N/A';
            document.getElementById('SadvanceDis').textContent = 'N/A';
            document.getElementById('SgtMoney').textContent = 'N/A';
        }
    })
    .catch(error => {
        console.error('Error checking turn:', error);
    });
}

function slideFunction(frame){
    if (frame.classList.contains('open')) {
        frame.classList.remove('open');
    } else {
        frame.classList.add('open');
    }
}