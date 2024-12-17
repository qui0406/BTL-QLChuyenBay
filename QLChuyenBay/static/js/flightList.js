function selectTicketType1(ticketType, flightId) {
    event.preventDefault()
    window.location.href='/ticket/'+  flightId + '?ticket-type='+ticketType
}

function selectTicketType2(ticketType, flightId) {
    event.preventDefault()
    window.location.href='/ticket/'+  flightId + '?ticket-type='+ticketType
}

