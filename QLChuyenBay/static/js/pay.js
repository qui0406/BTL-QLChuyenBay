const submitBtn = document.querySelector('#submit-btn')
const inputList = document.querySelectorAll('form input')

submitBtn.onclick = (e) => {
    e.preventDefault()
    const inputList = document.querySelectorAll('form input')
    const inpErr = Array.from(inputList).find(inp => !inp.value)
    if (inpErr) {
        inpErr.focus()
        return Swal.fire("Lỗi", "Vui lòng nhập đủ thông tin!", "error")
    }

    const data = {
        number_card: inputList[0].value.trim(),
        mmYY: inputList[1].value.trim(),
        cvcCode: inputList[2].value.trim(),
        name: inputList[3].value.trim(),
    }

    const pathNames = window.location.pathname
    const fId = pathNames[pathNames.length - 1]

    fetch(`/api/pay/${fId}`, {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.status==200){
            window.location.href = "/bill_ticket/" + data.data.id
        }
        if(data.status==500){
             Swal.fire("Lỗi", "Lỗi server!", "error")
        }
    })
    .catch(err => {
        Swal.fire("Lỗi", "Lỗi server!", "error")
    })
}