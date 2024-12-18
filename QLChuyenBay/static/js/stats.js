const canvas = document.getElementById('canvas');
const canvasContext = document.getElementById('canvas').getContext("2d");

function setStatus(el, status) {
    el.style.display = status
}

function checkType() {
    const canvas = document.querySelector('#canvas')
    if (selectType.value == 1) {
        setStatus(canvas, 'none')
        setStatus(table, 'table')
    }
    if (selectType.value == 2) {
        setStatus(canvas, 'block')
        setStatus(table, 'none')
    }
}

function randColor(arr) {
    arrColor = []
    arr.forEach(item => {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        arrColor.push(`rgb(${r},${g},${b})`);
    })
    return arrColor
}


function drawStats(el, labels, data) {
    colors = randColor(data.prices)
    new Chart(el, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: 'Doanh thu',
            data: data.prices,
            borderWidth: 1,
            backgroundColor: colors,
          }, {
            label: 'Vé bán',
            data: data.tickets,
            borderWidth: 1,
            backgroundColor: colors,
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
}