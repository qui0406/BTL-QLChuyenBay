const btnSeat= document.getElementById('choose_seat')
const addBtn = document.querySelector('#add-customer')
const subBtn = document.querySelector('#sub-customer')
const price = document.querySelector('.price span')
const select = document.querySelector('form select')

//btnSeat.onclick=()=>{
//    event.preventDefault()
//    window.location.href='/choose-seat'
//}

packagePrice = 0;

function updatePrice(value) {
    const data = price.innerHTML.split(",")
    let total = ""
    data.forEach(d => {
        total += d
    })
    price.innerHTML = new Intl.NumberFormat().format(parseInt(total) + parseInt(value))
}

addBtn.onclick=()=>{
    const listCustomer = document.querySelectorAll(".customer-info")
    const current = listCustomer.length

     customer = listCustomer[listCustomer.length - 1]
    if (current < 3) {
        const html = `
            <div class="customer-info d-flex gap-4 bg-white p-2 rounded-2 mt-3">
                <div class="flex-grow-1 mb-3">
                    <label for="name-${current + 1}" class="fw-bold form-label">Họ và tên: </label>
                    <input placeholder="Nguyễn Văn A" required type="text" minlength="4" name="name-${current + 1}" class="name-${current + 1} form-control" id="name-${current + 1}">
                </div>
                <div class="flex-grow-1 mb-3">
                    <label for="phone-${current + 1}" class="fw-bold form-label">Số điện thoại: </label>
                    <input placeholder="XXXXXXXXXX" required type="text" minlength="10" maxlength="10" name="phone-${current + 1}" class="phone-${current + 1} form-control" id="phone-${current + 1}">
                </div>
                <div class="flex-grow-1 mb-3">
                    <label for="id-${current + 1}" class="fw-bold form-label">CMND/CCCD: </label>
                    <input placeholder="XXXXXXXXXX" required type="text" minlength="10" maxlength="10" name="id-${current + 1}" class="id-${current + 1} form-control" id="id-${current + 1}">
                </div>
            </div>
        `
        customer.insertAdjacentHTML("afterend", html)
        updatePrice(parseInt(price.dataset.price))
    }
}

subBtn.onclick = () => {
    const listCustomer = document.querySelectorAll(".customer-info")
    const current = listCustomer.length
    if (current > 1) {
        listCustomer[current - 1].remove()
        updatePrice(parseInt(-price.dataset.price))
    }
}

select.onchange = (e) => {
    updatePrice(-packagePrice)
    if (e.target.value == 0) {
        packagePrice = 0
    }
    if (e.target.value == 12) {
        packagePrice = 320000
    }
    if (e.target.value == 20) {
        packagePrice = 400000
    }
    updatePrice(packagePrice)
}

btnSeat.onclick=(e)=>{
    e.preventDefault()

    const inputList = document.querySelectorAll('form input[required]')
    const inpErr = Array.from(inputList).find(inp => !inp.value)
//    if (inpErr) {
//        inpErr.focus()
//        return alert('loi')
//        //return Swal.fire("Lỗi", "Vui lòng nhập đủ thông tin!", "error")
//    }
//
//    const inpValidateErr = Array.from(inputList).find(inp => inp.value.length < inp.getAttribute('minlength'))
//
//    if (inpValidateErr) {
//        inpValidateErr.focus()
//        return alert('loi')
//      //  return Swal.fire("Lỗi", `Vui lòng nhập ít nhất ${inpValidateErr.getAttribute('minlength')} kí tự!`, "error")
//    }
//
//    function findInp(name) {
//        return Array.from(inputList).find(inp => inp.classList.contains(name))
//    }

    const customerInfo = []
    const quantityCustomner = (inputList.length - 2) / 3
    Array.from(inputList).forEach((inp, index) => {
        if (index == 2 || index == 5 || index == 8) {
            const obj = {
                id: index,
                name: inp.value,
                phone: inputList[index + 1].value,
                id_customer: inputList[index + 2].value
            }
            customerInfo.push(obj)
        }
    })
    window.location.href='/choose-seat'
}