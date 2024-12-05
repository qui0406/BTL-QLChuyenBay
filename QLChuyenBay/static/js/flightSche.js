const btnAddBwAirport = document.querySelector('.add-bw-airport')
const airportBetween= document.querySelectorAll('.airport-between')
const submitBtn = document.querySelector('.submit-btn')
const start = document.querySelector('#time-start')
const end = document.querySelector('#time-end')
const da = document.querySelector('#departure_airport_sche')
const aa = document.querySelector('#arrival_airport_sche')
const price_type_1= document.querySelector('#price_type_1')
const price_type_2= document.querySelector('#price_type_2')
const quantity_1st_ticket= document.querySelector('#quantity-1st-ticket')
const quantity_2nd_ticket= document.querySelector('#quantity-2nd-ticket')
const inpR = document.querySelectorAll("form input[required]")

function addBetweenAirport(max) {
    const airportBetween= document.querySelectorAll('.airport-between')
    let currentLength= airportBetween.length - 1
    if(currentLength < max){
        const html= `
            <div class="row airport-between mt-3">
                <div class="col-lg-3">
                    <label for="airport-bw-${currentLength}" class="form-label">Sân bay trung gian ${currentLength + 1}:
                    </label>
                    <input name="airport_bw_${currentLength}" type="text" class="form-control" id="airport-bw-${currentLength}" list="airports">
                </div>
                <div class="col-lg-3">
                    <label for="airport-bw-stay-${currentLength}" class="form-label">Thời gian dừng (giờ):</label>
                    <input name="airport_bw_stay_${currentLength}" min="0" type="number" class="form-control" id="airport-bw-stay-${currentLength}">
                </div>
                <div class="col-lg-6">
                    <label for="airport-bw-note-${currentLength}" class="form-label">Ghi chú:</label>
                    <input name="airport_bw_note_${currentLength}" type="text" class="form-control" id="airport-bw-note-${currentLength}">
                </div>
            </div>`
        airportBetween[currentLength].insertAdjacentHTML('afterend', html )
        btnAddBwAirport.innerHTML = `Thêm sân bay trung gian (Còn lại ${max - currentLength - 1})`
    }else{
        alert('Vượt quá quy định số sân bay trung gian')
    }
}

function getData(){
//    const checkTime= validateDateTime(new Date(start.value)) &&
//         new Date(end.time).getTime() - new Date(start.value).getTime()
//
//    const checkAirport= da.value && da.value=== aa.value
//
//    inpR.forEach(inp => {
//       if (!inp.value) {
//           inp.focus()
//           return Swal.fire("Lỗi", "Vui lòng điền đầy đủ thông tin!", "error");
//       }
//    })
//
//    if (checkAirport) {
//       return Swal.fire("Lỗi", "Vui lòng chọn lại chuyến bay phù hợp", "error");
//    }
//
//    if (checkTime <= 0) {
//       return Swal.fire("Lỗi", "Thời gian không hợp lệ", "error");
//    }
    const airportBetween= document.querySelectorAll('.airport-between')
    let airportBetweenList=[]
    let check= false

    airportBetween.forEach((ab, index)=>{
       const ap_id = ab.querySelector("div:first-child > input").value
       const ap_stay = ab.querySelector("div:nth-child(2) > input").value
       const ap_note = ab.querySelector("div:nth-child(3) > input").value

       if (ap_id && (ap_id == da.value || ap_id == aa.value)) {
          check= true
       }
       if (ap_id && ap_stay) {
           const obj = {
              id: index + 1,
              ap_id: ap_id.split(".")[0],
              ap_stay,
              ap_note
           }
           airportBetweenList.push(obj)
       }
    })
     fetch('/api/flight-schedule', {
           method: "POST",
           headers: {
                'Content-Type': 'application/json',
           },
           body: JSON.stringify({
                "depart_airport": da.value.split(".")[0],
                "arrival_airport": aa.value.split(".")[0],
                "time_start": start.value,
                "time_end": end.value,
                "quantity_1st_ticket": quantity_1st_ticket.value,
                "quantity_2nd_ticket": quantity_2nd_ticket.value,
                "price_type_1": price_type_1.value,
                "price_type_2": price_type_2.value,
                "airportBetweenList": airportBetweenList
           }),
        })
        .then(res => res.json())
        .then(data => {
            Swal.fire({
              position: "top-end",
              icon: "success",
              title: "Your work has been saved",
              showConfirmButton: false,
              timer: 1500});
            location.reload()
        })
        .catch(error => {
            console.error(error);
        });

}

