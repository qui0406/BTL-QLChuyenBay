//function selectTicketType(ticketType, flightId) {
//    event.preventDefault()
//
//     fetch(`/ticket/${flightId}`, {
//        method: 'POST', // Use POST for sending data
//        headers: {
//            'Content-Type': 'application/json' // Set content type
//        },
//        body: JSON.stringify({
//            ticketType: ticketType
//        })
//    })
//    .then(response => response.json())
//    .then(data => {
//        // Handle the response from the backend (e.g., update price display)
//        console.log(data);
//    })
//    .catch(error => console.error('Error:', error));
//}