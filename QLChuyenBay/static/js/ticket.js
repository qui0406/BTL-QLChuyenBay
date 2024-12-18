


const addBtn = document.querySelector('#add-customer')
const subBtn = document.querySelector('#sub-customer')
const price = document.querySelector('.price span')
const select = document.querySelector('#package')
const btnAccept= document.getElementById('accept_ticket')
const btnSeat= document.getElementById('choose_seat')

const priceTicket= parseFloat(price.innerHTML.replace(/[^0-9.]/g, ''))


//const quantityCustomner = (inputList.length - 2) / 3

let quantityCustomner= 1

let packagePrice = 0;

select.onchange = (e) => {
    updatePrice(priceTicket* quantityCustomner, 0)
    if (e.target.value == 0) {
        packagePrice = 0
    }
    if (e.target.value == 12) {
        packagePrice = 320000*quantityCustomner
    }
    if (e.target.value == 20) {
        packagePrice = 400000*quantityCustomner
    }
    updatePrice(parseFloat(price.innerHTML.replace(/[^0-9.]/g, '')), packagePrice)
}

function updatePrice(priceTicket, packagePrice){
    total= priceTicket + packagePrice
    price.innerHTML = `${Intl.NumberFormat().format(parseInt(total))} VNĐ`
}

addBtn.onclick=()=>{
    quantityCustomner++
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
        updatePrice(priceTicket*quantityCustomner, packagePrice* quantityCustomner)
    }
}

subBtn.onclick = () => {
    quantityCustomner--
    const listCustomer = document.querySelectorAll(".customer-info")
    const current = listCustomer.length
    if (current > 1) {
        listCustomer[current - 1].remove()
        updatePrice(parseFloat(price.innerHTML.replace(/[^0-9.]/g, ''))- parseFloat(priceTicket)- parseFloat(packagePrice), 0)
    }
}

btnSeat.onclick=()=>{
    event.preventDefault()

    const inputList = document.querySelectorAll('form input[required]')
    const inpValidateErr = Array.from(inputList).find(inp => inp.value.length < inp.getAttribute('minlength'))
    const inpErr = Array.from(inputList).find(inp => !inp.value)

    if (inpErr) {
        inpErr.focus()
        return Swal.fire("Lỗi", "Vui lòng nhập đủ thông tin!", "error")
    }
    if (inpValidateErr) {
        inpValidateErr.focus()
        return Swal.fire("Lỗi", `Vui lòng nhập ít nhất ${inpValidateErr.getAttribute('minlength')} kí tự!`, "error")
    }
    scrollToMiddle()
}

function scrollToMiddle() {
  const windowHeight = window.innerHeight;
  const documentHeight = document.body.scrollHeight;
  const middle = documentHeight / 2;
  window.scrollTo(0, middle - windowHeight / 2);
}

const chooseSeatNumber= document.querySelectorAll('.seat')
const userChooseSeatNumber=[]
    Array.from(chooseSeatNumber).forEach((seatNumber, index) =>{
        seatNumber.onchange=()=>{
//            if(userChooseSeatNumber.length > quantityCustomner){
//                return Swal.fire("Lỗi", "Vui lòng chọn đúng số lượng ghế!", "error")
//            }
            if(seatNumber.checked){
                userChooseSeatNumber.push(index)
            }
        }
    })

btnAccept.onclick=(e)=>{
    e.preventDefault()
    const inputList = document.querySelectorAll('form input[required]')

    function findInp(name) {
        return Array.from(inputList).find(inp => inp.classList.contains(name))
    }
    const customerInfo = []
    let cntCustomer=0;
    Array.from(inputList).forEach((inp, index) => {
        if (index == 2 || index == 5 || index == 8) {
            const obj = {
                id: index,
                name: inp.value,
                phone: inputList[index + 1].value,
                id_customer: inputList[index + 2].value,
                seat_number: userChooseSeatNumber[cntCustomer++]
            }
            customerInfo.push(obj)
        }
    })

    const pathNames = window.location.pathname
    const arr = pathNames.split('/')
    const fId= arr[arr.length-1]

    const data = {
        'contact_info': {
            'name': findInp('name').value,
            'phone': findInp('phone').value
        },
        'customers_info': [
            {
                'quantity': customerInfo.length,
                'data': customerInfo
            }
        ],
        'package_price': packagePrice,
        'f_id': fId,
        'ticket_type': document.querySelector('span.ticket-type').innerHTML,
        'total': parseFloat(price.innerHTML.replace(/[^0-9.]/g, '')),
        'seat_number': userChooseSeatNumber
    }
    if(userChooseSeatNumber.length < quantityCustomner){
         return Swal.fire("Lỗi", `Vui lòng chọn thêm ${quantityCustomner - userChooseSeatNumber.length} ghế!`, "error")
    }
    if(userChooseSeatNumber.length==0){
        return Swal.fire("Lỗi", "Vui lòng chọn ghế!", "error")
    }
    console.log(data)
    fetch(`/api/ticket/${fId}`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type':'application/json'
        }
    })
    .then(res=>res.json())
    .then(data=>{
        if (data.status == 200) {
            console.log(data)
            window.location.href = "/list-flight-payment/" + data.data
        }
        if (data.status == 500) {
            Swal.fire("Lỗi", data.data, "error")
        }
    })
    .catch(err => {
        Swal.fire("Lỗi", err.data, "error")
    })
}

