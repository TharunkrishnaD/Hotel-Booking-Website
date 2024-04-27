function hiderooms(hotelCode) {
    document.getElementById(hotelCode).style.display = 'none';
    var showButton = document.getElementById(hotelCode+'2');
    var hideButton = document.getElementById(hotelCode+'1');
    showButton.style.display = 'block';
    hideButton.style.display = 'none';
    // document.getElementById(hotelCode).style.display = 'none';
}

function handleSelectRoom(hotelCode, traceId, resultIndex, tokenId) {
    // Your existing code for hiding rooms...
    document.getElementById(hotelCode).innerHTML = "<div id='loading'></div>"
    // AJAX request to send data to views.py
    var showButton = document.getElementById(hotelCode+'2');
    var hideButton = document.getElementById(hotelCode+'1');
    showButton.style.display = 'none';
    hideButton.style.display = 'block';
    document.getElementById(hotelCode).style.display='block'
    var csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
    $.ajax({
        url: "/get_room_details/",  // Replace with the actual URL of your views.py
        type: "POST",
        data: {
            'hotelCode': hotelCode,
            'traceId': traceId,
            'resultIndex': resultIndex,
            'tokenId': tokenId
        },
        headers: {
            'X-CSRFToken': csrftoken  // Include the CSRF token in the headers
        },
        success: function(response) {
            // var roomDetailsData = response.room_details;
            // updateRoomDetails(roomDetailsData, hotelCode);
            document.getElementById(hotelCode).innerHTML = response.room_details_html;
            // console.log(roomDetailsData);
        },
        error: function(error) {
            document.getElementById(hotelCode).innerHTML = "<a>No Room Available</a>"
            console.error(error);
        }
    });
}

function sortHotels(criteria) {
    var hotelList = document.getElementById('hotelList');
    var hotels = Array.from(hotelList.getElementsByClassName('hotel'));

    var sortOrder = hotelList.getAttribute('data-sort-order') || 'asc';

    hotels.sort(function(a, b) {
        var aValue = a.getAttribute('data-' + criteria);
        var bValue = b.getAttribute('data-' + criteria);

        // Handle numeric or string comparisons based on the criteria
        if (criteria === 'Price' || criteria === 'Rating') {
            return sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
        } else if (criteria === 'Name') {
            return sortOrder === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
        }
    });

    // Clear the existing hotel list
    hotelList.innerHTML = '';

    // Append the sorted hotels to the list
    hotels.forEach(function(hotel) {
        hotelList.appendChild(hotel);
    });

    // Toggle sort order for the next click
    hotelList.setAttribute('data-sort-order', sortOrder === 'asc' ? 'desc' : 'asc');
}

// function bookRoom() {
//     var roomJsonElement = document.querySelector('.hide-elements .room-json');
//     var dataJsonElement = document.querySelector('.hide-elements .data-json');
//     var hotelName = document.querySelector('.hotel-name p').innerText;
//     // var hotelName = document.getElementById("hotelNameElement").innerText.trim();

//     if (roomJsonElement && dataJsonElement) {
//         var currentRoomJson = JSON.parse(roomJsonElement.innerText);
//         var currentDataJson = JSON.parse(dataJsonElement.innerText);
//         console.log(currentRoomJson);
//         console.log(currentDataJson);

//         var payload = {
//             ResultIndex: currentDataJson.ResultIndex,
//             HotelCode: currentDataJson.HotelCode,
//             HotelName: hotelName,
//             GuestNationality:"IN",
//             NoOfRooms: "1",
//             ClientReferenceNo: "0",
//             IsVoucherBooking: "true",
//             HotelRoomsDetails: [
//                 {
//                     RoomIndex: currentRoomJson.RoomIndex,
//                     RoomTypeCode: currentRoomJson.RoomTypeCode,
//                     RoomTypeName: currentRoomJson.RoomTypeName,
//                     RatePlanCode:currentRoomJson.RatePlanCode,
//                     BedTypeCode:null,
//                     SmokingPreference:0,
//                     Supplements:null,
//                     Price:currentRoomJson.Price
//                 }
//             ],
//             EndUserIp: '123.1.1.1',  // Replace with actual end user IP
//             TokenId: currentDataJson.TokenId,
//             TraceId: currentDataJson.TraceId,
//         };
//         var csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
//         // Assuming you have jQuery available
//         $.ajax({
//             url: '/hotelreview/',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify(payload),
//             headers: {
//                 'X-CSRFToken': csrftoken  // Include the CSRF token in the headers
//             },
//             success: function(response) {
//                 console.log(response);
//                 var newWindow = window.open();
//                 newWindow.document.write(response.html);
//                 // Handle the response as needed
//             },
//             error: function(error) {
//                 console.error(error);
//             }
//         });
//     }
// }
// function bookRoom() {
//     var roomJsonElement = document.querySelector('.hide-elements .room-json');
//     var dataJsonElement = document.querySelector('.hide-elements .data-json');
//     var hotelName = document.querySelector('.hotel-name p').innerText;
//     // var hotelName = document.getElementById("hotelNameElement").innerText.trim();


//     if (roomJsonElement && dataJsonElement) {
//         var currentRoomJson = JSON.parse(roomJsonElement.innerText);
//         var currentDataJson = JSON.parse(dataJsonElement.innerText);
//         console.log(currentRoomJson);
//         console.log(currentDataJson);

//         var payload = {
//             ResultIndex: currentDataJson.ResultIndex,
//             HotelCode: currentDataJson.HotelCode,
//             HotelName: hotelName,
//             GuestNationality:"IN",
//             NoOfRooms: "1",
//             ClientReferenceNo: "0",
//             IsVoucherBooking: "true",
//             HotelRoomsDetails: [
//                 {
//                     RoomIndex: currentRoomJson.RoomIndex,
//                     RoomTypeCode: currentRoomJson.RoomTypeCode,
//                     RoomTypeName: currentRoomJson.RoomTypeName,
//                     RatePlanCode:currentRoomJson.RatePlanCode,
//                     BedTypeCode:null,
//                     SmokingPreference:0,
//                     Supplements:null,
//                     Price:currentRoomJson.Price
//                 }
//             ],
//             EndUserIp: '123.1.1.1',  // Replace with actual end user IP
//             TokenId: currentDataJson.TokenId,
//             TraceId: currentDataJson.TraceId,
//         };

//         var csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
        
//         // Assuming you have jQuery available
//         $.ajax({
//             url: '/hotelreview/',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify(payload),
//             headers: {
//                 'X-CSRFToken': csrftoken  // Include the CSRF token in the headers
//             },
//             success: function(response) {
//                 console.log(response);
//                 var newWindow = window.open();
//                 newWindow.document.write(response.html);
//                 // Handle the response as needed
//             },
//             error: function(error) {
//                 console.error(error);
//             }
//         });
//     }
// }
// function bookRoom(groupIndex) {
//     var groupContainer = document.querySelector('.hide-room' + groupIndex);
//     var roomJsonElements = groupContainer.querySelectorAll('.hide-elements .room-json');
//     var dataJsonElement = groupContainer.querySelector('.hide-elements .data-json');
//     var hotelName = document.querySelector('.hotel-name p').innerText;

//     if (roomJsonElements.length > 0 && dataJsonElement) {
//         var roomDetails = [];

//         roomJsonElements.forEach(function(roomJsonElement) {
//             var currentRoomJson = JSON.parse(roomJsonElement.innerText);
//             roomDetails.push({
//                 RoomIndex: currentRoomJson.RoomIndex,
//                 RoomTypeCode: currentRoomJson.RoomTypeCode,
//                 RoomTypeName: currentRoomJson.RoomTypeName,
//                 RatePlanCode: currentRoomJson.RatePlanCode,
//                 BedTypeCode: null,
//                 SmokingPreference: 0,
//                 Supplements: null,
//                 Price: currentRoomJson.Price
//             });
//         });

//         var currentDataJson = JSON.parse(dataJsonElement.innerText);

//         var payload = {
//             ResultIndex: currentDataJson.ResultIndex,
//             HotelCode: currentDataJson.HotelCode,
//             HotelName: hotelName,
//             GuestNationality: "IN",
//             NoOfRooms: roomDetails.length.toString(),
//             ClientReferenceNo: "0",
//             IsVoucherBooking: "true",
//             HotelRoomsDetails: roomDetails,
//             EndUserIp: '123.1.1.1',  // Replace with actual end-user IP
//             TokenId: currentDataJson.TokenId,
//             TraceId: currentDataJson.TraceId,
//         };

//         var csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];

//         // Assuming you have jQuery available
//         $.ajax({
//             url: '/hotelreview/',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify(payload),
//             headers: {
//                 'X-CSRFToken': csrftoken  // Include the CSRF token in the headers
//             },
//             success: function(response) {
//                 console.log(response);
//                 var newWindow = window.open();
//                 newWindow.document.write(response.html);
//                 // Handle the response as needed
//             },
//             error: function(error) {
//                 console.error(error);
//             }
//         });
//     }
// }

function bookRoom1() {
    var roomJsonElement = document.querySelector('.hide-elements .room-json');
    var dataJsonElement = document.querySelector('.hide-elements .data-json');
    var hotelName = document.querySelector('.h-name p').innerText;
    console.log(hotelName)

    if (roomJsonElement && dataJsonElement) {
        var currentRoomJson = JSON.parse(roomJsonElement.innerText);
        var currentDataJson = JSON.parse(dataJsonElement.innerText);
        console.log(currentRoomJson);
        console.log(currentDataJson);

        var payload = {
            ResultIndex: currentDataJson.ResultIndex,
            HotelCode: currentDataJson.HotelCode,
            HotelName: hotelName,
            GuestNationality:"IN",
            NoOfRooms: "1",
            ClientReferenceNo: "0",
            IsVoucherBooking: "true",
            HotelRoomsDetails: [
                {
                    RoomIndex: currentRoomJson.RoomIndex,
                    RoomTypeCode: currentRoomJson.RoomTypeCode,
                    RoomTypeName: currentRoomJson.RoomTypeName,
                    RatePlanCode:currentRoomJson.RatePlanCode,
                    BedTypeCode:null,
                    SmokingPreference:0,
                    Supplements:null,
                    Price:currentRoomJson.Price
                }
            ],
            EndUserIp: '123.1.1.1',  // Replace with actual end user IP
            TokenId: currentDataJson.TokenId,
            TraceId: currentDataJson.TraceId,
        };
        var csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
        // Assuming you have jQuery available
        $.ajax({
            url: '/hotelreview/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            headers: {
                'X-CSRFToken': csrftoken  // Include the CSRF token in the headers
            },
            success: function(response) {
                console.log(response);
                var newWindow = window.open();
                newWindow.document.write(response.html);
                // Handle the response as needed
            },
            error: function(error) {
                console.error(error);
            }
        });
    }
}


function showForm() {
    var x = document.getElementById("form")
    if (x.style.display === "none") {
        x.style.display = "block" ;
    } else {
        x.style.display = "none" ;
    }
}


// function getAdultCount() {
//     $rowno = $("#attribute_table tr").length-2
//     totaladult=0
//     totalchild=0
//     roominfo=[]
//     totalroominf0=[]

//     for(i=1;i<=$rowno;i++) {
//         totaladult=parseInt(totaladult) + parseInt($("#adult_"+i).val())
//         totalchild=parseInt(totalchild) + parseInt($("#child_"+i).val())

//         var childAge = parseInt($("#child_"+i).val()) !== 0 ? [parseInt($("#childage_"+i).val())] : null;

//         roominfo[i-1]={"NoOfAdults":parseInt($("#adult_"+i).val()) ,"NoOfChild": parseInt($("#child_"+i).val()),"ChildAge": childAge }
//     }

//     var roomCount = $rowno + " " + "Room" +" " + "&" + " " + totaladult +" " + "Adults";
    
//     document.getElementById('room').value = roomCount;


//     document.getElementById('roomInfoInput').value = JSON.stringify(roominfo);
//     document.getElementById('totalRoomInfoInput').value = JSON.stringify({
//         "TotalRooms": $rowno,
//     });
// }


// function add_attribute_row() {
//     $rowno = $("#attribute_table tr").length-1 ;
//     $("#attribute_table tr:last").after("<tr id='row" + $rowno + "'><td>Room" + $rowno + "<td><select name='attribute_name' onchange='getAdultCount()' id='adult_" + $rowno + "' class='form-control attribute_name'><option value='0'>Select</option><option value='1'>1</option><option value='2'>2</option><option value='3'>3</option><option value='4'>4</option><option value='5'>5</option><option value='6'>6</option></select></td><td><select name='attribute_id' id='child_" + $rowno + "' onchange='getAdultCount()' class='form-control attribute_value'><option data-parent='0' value='0'>Select</option><option data-parent='Colour' value='1'>1</option><option data-parent='Colour' value='2'>2</option><option data-parent='Colour' value='3'>3</option></select></td><td><select name='attribute_id' id='childage_" + $rowno + "' onchange='getAdultCount()' class='form-control attribute_value'><option data-parent='0' value='0'>Select</option><option data-parent='Colour' value='1'>1</option><option data-parent='Colour' value='2'>2</option><option data-parent='Colour' value='3'>3</option><option data-parent='Colour' value='4'>4</option><option data-parent='Colour' value='5'>5</option><option data-parent='Colour' value='6'>6</option><option data-parent='Colour' value='7'>7</option><option data-parent='Colour' value='8'>8</option><option data-parent='Colour' value='9'>9</option><option data-parent='Colour' value='10'>10</option><option data-parent='Colour' value='11'>11</option><option data-parent='Colour' value='12'>12</option></select></td></tr>");
//     getAdultCount()
// }

// function del_att_row() {
//     rowno = $("#attribute_table tr").length-2
//     if(rowno > 1)
//     $('#row' + rowno).remove();
//     getAdultCount()
// }


function updateStars() {
    var starInput = document.getElementById('starInput');
    var starViews = document.querySelectorAll('.star-view');

    var starValue = parseInt(starInput.value);

    starViews.forEach(function(starView, index) {
        if (index + 3 === starValue) {
            starView.style.display = 'block';
            markStars(starView, index + 3);
        } else {
            starView.style.display = 'none';
        }
    });
}

function markStars(starView, count) {
    var stars = starView.querySelectorAll('.fa-star');
    for (var i = 0; i < count; i++) {
        stars[i].classList.add('checked');
    }
}



