// SLIDER -----------------------------------------------------

let slideIndex = 1;
const slides = document.getElementsByClassName("slide");
const dots = document.getElementsByClassName("dot");

function showSlides(n) {
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }

  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

function plusSlides(n) {
  showSlides((slideIndex += n));
}

function currentSlide(n) {
  showSlides((slideIndex = n));
}

setInterval(function () {
  plusSlides(1);
}, 5000);

showSlides(slideIndex);

// FORM FUNCTIONS ----------------------------------------

function showForm() {
    var x = document.getElementById("form")
    if (x.style.display === "none") {
        x.style.display = "block" ;
    } else {
        x.style.display = "none" ;
    }
}



// function getAdultCount() {
//   var $rowno = $("#attribute_table tr.room-info").length; // Get the total number of room rows
//   var totaladult = 0;
//   var totalchild = 0;
//   var roominfo = [];

//   for (var i = 1; i <= $rowno; i++) {
//       var adults = parseInt($("#adult_" + i).val());
//       var children = parseInt($("#child_" + i).val());
//       var childAge = [];

//       for (var j = 1; j <= children; j++) {
//           var age = parseInt($("#childage_" + j).val());
//           childAge.push(age);
//       }

//       totaladult += adults;
//       totalchild += children;

//       roominfo.push({
//           "NoOfAdults": adults,
//           "NoOfChild": children,
//           "ChildAge": childAge
//       });
//   }

//   var roomCount = $rowno + " Room & " + totaladult + " Adults";
//   document.getElementById('room').value = roomCount;

//   var totalroominfo = {
//       "TotalRooms": $rowno,
//       "NoOfAdults": totaladult,
//       "NoOfChild": totalchild
//   };

//   console.log(roominfo, totalroominfo);

//   document.getElementById('roomInfoInput').value = JSON.stringify(roominfo);
//   document.getElementById('totalRoomInfoInput').value = JSON.stringify(totalroominfo);
//   document.getElementById('totalNoOfRooms').value = $rowno;
// }
// function add_attribute_row() {
//   // Get the current number of rows
//   var $rowno = $("#attribute_table tr.room-info").length;

//   // Check if the limit of 6 rows has been reached
//   if ($rowno < 6) {
//       // Add a new row
//       $("#attribute_table tr:last").after("<tr id='row" + ($rowno + 1) + "' class='room-info'>" +
//           "<td>Room" + ($rowno + 1) + "</td>" +
//           "<td><select name='attribute_name' onchange='getAdultCount()' id='adult_" + ($rowno + 1) + "' class='form-control attribute_name'>" +
//           "<option value='0'>Select</option><option value='1' selected>1</option><option value='2'>2</option><option value='3'>3</option>" +
//           "<option value='4'>4</option><option value='5'>5</option><option value='6'>6</option></select></td>" +
//           "<td><select name='attribute_id' id='child_" + ($rowno + 1) + "' onchange='updateChildAgeSelectors()' class='form-control attribute_value'>" +
//           "<option data-parent='0' value='0'>Select</option><option value='1'>1</option><option value='2'>2</option><option value='3'>3</option></select></td>" +
//           "<td id='childAgeSelectors_" + ($rowno + 1) + "'>" +
//           "<select name='attribute_id' id='childage_" + ($rowno + 1) + "' class='form-control attribute_value' style='display: none;'>" +
//           "<option value='1'>1</option><option value='2'>2</option><option value='3'>3</option>" +
//           "<option value='4'>4</option><option value='5'>5</option><option value='6'>6</option>" +
//           "<option value='7'>7</option><option value='8'>8</option><option value='9'>9</option>" +
//           "<option value='10'>10</option><option value='11'>11</option><option value='12'>12</option>" +
//           "</select></td></tr>");

//       // Call the updateChildAgeSelectors function
//       updateChildAgeSelectors();
//   } else {
//       // Alert the user or handle the case where the limit is reached
//       alert("Only 6 rooms are allowed.");
//   }
// }


// function del_att_row() {
//         rowno = $("#attribute_table tr").length-2 ;
//         if(rowno > 1)
//         $('#row' + rowno).remove();
//         getAdultCount()
//     }

// $(document).ready(function() {
//     $("#adult_1").val("2");
//     getAdultCount();
//     });
// function getAdultCount() {
//   var $rowno = $("#attribute_table tr.room-info").length; // Get the total number of room rows
//   var totaladult = 0;
//   var totalchild = 0;
//   var roominfo = [];

//   for (var i = 1; i <= $rowno; i++) {
//     var adults = parseInt($("#adult_" + i).val());
//     var children = parseInt($("#child_" + i).val());
//     var childAge = [];

//     for (var j = 1; j <= children; j++) {
//       var age = parseInt($("#childage_" + j + "_" + i).val());
//       childAge.push(age);
//     }

//     totaladult += adults;
//     totalchild += children;

//     roominfo.push({
//       "NoOfAdults": adults,
//       "NoOfChild": children,
//       "ChildAge": childAge
//     });
//   }

//   var roomCount = $rowno + " Room & " + totaladult + " Adults";
//   document.getElementById('room').value = roomCount;

//   var totalroominfo = {
//     "TotalRooms": $rowno,
//     "NoOfAdults": totaladult,
//     "NoOfChild": totalchild
//   };

//   console.log(roominfo, totalroominfo);

//   document.getElementById('roomInfoInput').value = JSON.stringify(roominfo);
//   document.getElementById('totalRoomInfoInput').value = JSON.stringify(totalroominfo);
//   document.getElementById('totalNoOfRooms').value = $rowno;
// }

// function add_attribute_row() {
//   // Get the current number of rows
//   var $rowno = $("#attribute_table tr.room-info").length;

//   // Check if the limit of 6 rows has been reached
//   if ($rowno < 6) {
//     // Add a new row
//     var newRow = "<tr id='row" + ($rowno + 1) + "' class='room-info'>" +
//       "<td>Room" + ($rowno + 1) + "</td>" +
//       "<td><select name='attribute_name' onchange='getAdultCount()' id='adult_" + ($rowno + 1) + "' class='form-control attribute_name'>" +
//       "<option value='0'>Select</option><option value='1' selected>1</option><option value='2'>2</option><option value='3'>3</option>" +
//       "<option value='4'>4</option><option value='5'>5</option><option value='6'>6</option></select></td>" +
//       "<td><select name='attribute_id' id='child_" + ($rowno + 1) + "' onchange='updateChildAgeSelectors(this)' class='form-control attribute_value'>" +
//       "<option data-parent='0' value='0'>Select</option><option value='1'>1</option><option value='2'>2</option><option value='3'>3</option></select></td>" +
//       "<td id='childAgeSelectors_" + ($rowno + 1) + "'></td></tr>";

//     $("#attribute_table tr:last").after(newRow);

//     // Update the child age selectors for the newly added row
//     updateChildAgeSelectors($("#child_" + ($rowno + 1)));
//   } else {
//     // Alert the user or handle the case where the limit is reached
//     alert("Only 6 rooms are allowed.");
//   }
// }

// function add_attribute_row() {
//   var table = document.getElementById("attribute_table");
//   var rowCount = table.rows.length - 1;
//   var row = table.insertRow(rowCount);
  
//   var cell1 = row.insertCell(0);
//   var cell2 = row.insertCell(1);
//   var cell3 = row.insertCell(2);
//   var cell4 = row.insertCell(3);
  
//   cell1.innerHTML = "Room" + rowCount;
//   cell2.innerHTML = `<select name='attribute_name' class='form-control attribute_name' id='adult_${rowCount}' onchange='getAdultCount()'>
//                           <option value='0'>Select</option>
//                           <option value='1'>1</option>
//                           <option value='2'>2</option>
//                           <option value='3'>3</option>
//                           <option value='4'>4</option>
//                           <option value='5'>5</option>
//                           <option value='6'>6</option>
//                       </select>`;
//   cell3.innerHTML = `<select name='attribute_id' id='child_${rowCount}' class='form-control attribute_value' onchange='updateChildAgeSelectors(${rowCount}); getAdultCount();'>
//                           <option data-parent='0' value='0'>Select</option>
//                           <option value='1'>1</option>
//                           <option value='2'>2</option>
//                           <option value='3'>3</option>
//                           <option value='4'>4</option>
//                       </select>`;
//   cell4.innerHTML = `<div id='child_age_selectors_${rowCount}' style="display: flex;flex-direction: row;"></div>`;
//   getAdultCount();
// }


// function updateChildAgeSelectors(roomNumber) {
//   var childCountSelect = document.getElementById("child_" + roomNumber);
//   var childAgeSelectorsContainer = document.getElementById("child_age_selectors_" + roomNumber);
//   var childlabel =  document.getElementById("childage_label")
//   childAgeSelectorsContainer.innerHTML = ""; // Clear existing child age selectors
  
//   var childCount = parseInt(childCountSelect.value);
//   if (childCount > 0) {
//       for (var i = 1; i <= childCount; i++) {
//           var childAgeSelect = document.createElement("select");
//           childAgeSelect.name = "child_age_" + roomNumber + "_" + i;
//           childAgeSelect.id = "child_age_" + roomNumber + "_" + i;
//           childAgeSelect.className = "form-control child_age";
//           childAgeSelect.innerHTML = `
//               <option value='1'>1</option>
//               <option value='2'>2</option>
//               <option value='3'>3</option>
//               <option value='4'>4</option>
//               <option value='5'>5</option>
//               <option value='6'>6</option>
//               <option value='7'>7</option>
//               <option value='8'>8</option>
//               <option value='9'>9</option>
//               <option value='10'>10</option>
//               <option value='11'>11</option>
//               <option value='12'>12</option>
//           `;
//           childAgeSelectorsContainer.appendChild(childAgeSelect);
//           childlabel.style.display = "block";
//       }
//   }
//   childAgeSelectorsContainer.addEventListener('change', function(event) {
//       if (event.target && event.target.classList.contains('child_age')) {
//           getAdultCount();
//       }
//   });
// }

// function getAdultCount() {
//   var roomRows = $("#attribute_table tr.room-info"); // Get all room rows
//   var roominfo = [];

//   // Loop through each room row to collect information
//   roomRows.each(function(index, row) {
//       var adults = parseInt($(row).find(".attribute_name").val());
//       var children = parseInt($(row).find(".attribute_value").val());
//       var childAges = []; // Array to store child ages

//       // Loop through child age selectors and collect ages
//       $(row).find(".child_age").each(function(index, select) {
//           var age = parseInt($(select).val());
//           if (!isNaN(age)) {
//               childAges.push(age);
//           }
//       });

//       roominfo.push({
//           "NoOfAdults": adults,
//           "NoOfChild": children,
//           "ChildAges": childAges
//       });
//   });

//   // Update the roomInfoInput with the room information
//   $("#roomInfoInput").val(JSON.stringify(roominfo));

//   // Calculate total rooms, adults, children, and their ages
//   var totalRooms = roomRows.length;
//   var totalAdults = roominfo.reduce((acc, room) => acc + room.NoOfAdults, 0);
//   var totalChildren = roominfo.reduce((acc, room) => acc + room.NoOfChild, 0);
//   var totalChildAges = roominfo.reduce((acc, room) => acc.concat(room.ChildAges), []);

//   // Update the totalRoomInfoInput with the total room information
//   var totalRoomInfo = {
//       "TotalRooms": totalRooms,
//       "NoOfAdults": totalAdults,
//       "NoOfChild": totalChildren,
//       "ChildAges": totalChildAges
//   };
//   $("#totalRoomInfoInput").val(JSON.stringify(totalRoomInfo));

//   // Additional logic to update other fields if needed
// }






// function del_att_row() {
//   // Get the current number of rows
//   var table = document.getElementById("attribute_table");
//   var rowCount = table.rows.length - 1;
//   if (rowCount > 2) {
//       table.deleteRow(rowCount - 1); // Remove the last row (room)
//   } else {
//       alert("Cannot remove the last room.");
//   }
//   // Recalculate the counts
//   getAdultCount();
// }
// DATE FUNCTIONS -----------------------------------------------------

$(function () {
    // Initialize Datepicker for the first date
    $("#check-in").datepicker({
      minDate: 0, // Minimum date is today
      dateFormat: 'dd MM yy', // Set the date format
      onSelect: function (dateText, inst) {
        // Update the data-date attribute using moment.js
        $(this).attr("data-date", moment(dateText, "DD MMMM YYYY").format($(this).attr("data-date-format")));

        // Calculate the next date using moment.js
        var nextDate = moment(dateText, "DD MMMM YYYY").add(1, 'days').format("DD MMMM YYYY");

        // Set the default date for the second datepicker to one day after the selected date
        $("#check-out").datepicker("option", "minDate", nextDate);
        $("#check-out").datepicker("setDate", nextDate);
      }
    });

    // Initialize Datepicker for the second date
    $("#check-out").datepicker({
      minDate: 1, // Minimum date is one day after today
      dateFormat: 'dd MM yy', // Set the date format
    });

    // Set the default date to today for the first datepicker
    $("#check-in").datepicker("setDate", new Date());

    // Set the default date for the second datepicker to one day after today
    var nextDefaultDate = moment().add(1, 'days').format("DD MMMM YYYY");
    $("#check-out").val(nextDefaultDate);
  });

//   VALIDATION FUNCTIONS -------------------------------

function validateForm() {
    var des = document.getElementsByClassName("des")[0].value.trim();
    var room = document.getElementById("room").value.trim();
    if (des === "") {
        alert("Please Enter Your Destination");
        return false; // Prevent form submission
    } 
        if (room === "") {
        alert("Please Enter Room Information");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}