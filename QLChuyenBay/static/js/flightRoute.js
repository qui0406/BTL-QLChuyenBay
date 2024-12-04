function addRoute(){
    fetch('/api/admin-route-flight', {
        method: 'post'
    }).then(function(res){
        return res.json()
    }).then(function(data){
        if(data.status== 200){
            console.log(data.status)
            window.location.reload()
        }
    }).catch(function(err){
        console.error(err)
    })
    return Swal.fire({
         position: "top-end",
         icon: "success",
         title: "Your work has been saved",
         showConfirmButton: false,
         timer: 1500});
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