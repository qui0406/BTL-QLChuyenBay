const btnSubmit= document.querySelector('.btn-submit')

const inp_da= document.getElementById('departure')
const inp_aa= document.getElementById('arrival')

function addRoute(){
    fetch('/api/admin-route-flight', {
        method: "POST",
        body: JSON.stringify({
            "depart_airport": inp_da.value,
            "arrival_airport": inp_aa.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res=>res.json())
    .then(data=>{
        Swal.fire({
              position: "top-end",
              icon: "success",
              title: "Your work has been saved",
              showConfirmButton: false,
              timer: 1500});
        location.reload()

    }).catch(err=>{
        console.error(err)
    })
}

function deleteRoute(id){
    return Swal.fire({
          title: "Are you sure?",
          text: "You won't be able to revert this!",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Yes, delete it!"
    }).then((result) => {
    if (result.isConfirmed) {
        fetch(`/api/delete-route/${id}`, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
             const routeElement = document.getElementById(`route${id}`);
             if (routeElement) {
                routeElement.style.display = "none";
             } else {
                console.warn("Element with id route", id, "not found");
             }
        })
        .catch(err => {
             console.error("Error deleting route:", err);
        });
            Swal.fire({
                title: "Deleted!",
                text: "Your file has been deleted.",
                icon: "success"
            });
        }
    })
}