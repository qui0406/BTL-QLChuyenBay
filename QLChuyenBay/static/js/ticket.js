


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
            <div class="customer-info d-flex flex-wrap gap-4 bg-white p-2 rounded-2">
                <div class="flex-grow-1 mb-3">
                    <label for="name-1" class="form-label">Họ và tên:</label>
                    <input value="Nguyễn Văn B" placeholder="Nguyễn Văn B" required minlength="4"
                           type="text" name="name-1" class="name-1 form-control" id="name-1">
                </div>
                <div class="flex-grow-1 mb-3">
                    <label for="cccd-1" class="form-label">CCCD:</label>
                    <input value="096204015159" placeholder="096204015159" required minlength="12" maxlength="12"
                           type="text" name="cccd-1" class="cccd-1 form-control" id="cccd-1">
                </div>
                <div class="flex-grow-1 mb-3">
                    <label for="dob-1" class="form-label">Ngày sinh:</label>
                    <input value="2004-02-21"placeholder="YYYY-MM-DD" required type="date"
                           name="dob-1" class="dob-1 form-control" id="dob-1">
                </div>
                <!-- Ngắt dòng tại đây -->
                <div class="w-100"></div>
                <div class="flex-grow-1 mb-3">
                    <label for="phone-1" class="form-label">Số điện thoại:</label>
                    <input value="1234567890" placeholder="XXXXXXXXXX" required minlength="10" maxlength="10"
                           type="text" name="phone-1" class="phone-1 form-control" id="phone-1">
                </div>
                <div class="flex-grow-1 mb-3">
                    <label for="id-1" class="form-label">Email:</label>
                    <input value="abc@gmail.com" placeholder="abc@gmail.com" required type="email"
                           name="id-1" class="id-1 form-control" id="id-1">
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
                customer_cccd: inputList[index + 1].value,
                customer_date: inputList[index + 2].value,
                customer_phone: inputList[index + 3].value,
                customer_email: inputList[index + 4].value,
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