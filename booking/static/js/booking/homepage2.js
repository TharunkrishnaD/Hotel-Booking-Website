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

// ---------------------------------------

function showForm() {
    var x = document.getElementById("form")
    if (x.style.display === "none") {
        x.style.display = "block" ;
    } else {
        x.style.display = "none" ;
    }
}

function hideForm() {
  var x = document.getElementById("form")
  if (x.style.display === "block") {
      x.style.display = "none" ;
  } else {
      x.style.display = "none" ;
  }
}

function getAdultCount() {
    $rowno = $("#attribute_table tr").length-2
    totaladult=0
    totalchild=0
    roominfo=[]
    totalroominf0=[]

    for(i=1;i<=$rowno;i++) {
        totaladult=parseInt(totaladult) + parseInt($("#adult_"+i).val())
        totalchild=parseInt(totalchild) + parseInt($("#child_"+i).val())

        var childAge = parseInt($("#child_"+i).val()) !== 0 ? [parseInt($("#childage_"+i).val())] : null;

        roominfo[i-1]={"NoOfAdults":parseInt($("#adult_"+i).val()) ,"NoOfChild": parseInt($("#child_"+i).val()),"ChildAge": childAge }
    }

    var roomCount = $rowno + " " + "Room" +" " + "&" + " " + totaladult +" " + "Adults";
    
    document.getElementById('room').value = roomCount;

    document.getElementById('roomInfoInput').value = JSON.stringify(roominfo);
    document.getElementById('totalRoomInfoInput').value = JSON.stringify({
        "TotalRooms": $rowno,
    });

    // totalroominf0={"TotalRooms":$rowno,"TotalAdult":totaladult,"TotalChild":totalchild }
    // console.log(roominfo,totalroominf0)
    // console.log(totalroominf0)
}

function add_attribute_row() {
    $rowno = $("#attribute_table tr").length-1 ;
    $("#attribute_table tr:last").after("<tr id='row" + $rowno + "'><td>Room" + $rowno + "<td><select name='attribute_name' onchange='getAdultCount()' id='adult_" + $rowno + "' class='form-control attribute_name'><option value='0'>Select</option><option value='1'>1</option><option value='2'>2</option><option value='3'>3</option><option value='4'>4</option><option value='5'>5</option><option value='6'>6</option></select></td><td><select name='attribute_id' id='child_" + $rowno + "' onchange='getAdultCount()' class='form-control attribute_value'><option data-parent='0' value='0'>Select</option><option data-parent='Colour' value='1'>1</option><option data-parent='Colour' value='2'>2</option><option data-parent='Colour' value='3'>3</option></select></td><td><select name='attribute_id' id='childage_" + $rowno + "' onchange='getAdultCount()' class='form-control attribute_value'><option data-parent='0' value='0'>Select</option><option data-parent='Colour' value='1'>1</option><option data-parent='Colour' value='2'>2</option><option data-parent='Colour' value='3'>3</option><option data-parent='Colour' value='4'>4</option><option data-parent='Colour' value='5'>5</option><option data-parent='Colour' value='6'>6</option><option data-parent='Colour' value='7'>7</option><option data-parent='Colour' value='8'>8</option><option data-parent='Colour' value='9'>9</option><option data-parent='Colour' value='10'>10</option><option data-parent='Colour' value='11'>11</option><option data-parent='Colour' value='12'>12</option></select></td></tr>");
    getAdultCount()
}

function del_att_row() {
    rowno = $("#attribute_table tr").length-2
    if(rowno > 1)
    $('#row' + rowno).remove();
    getAdultCount()
}


document.getElementById('checkInDate').addEventListener('input', function() {
  var checkInDate = new Date(this.value);
  var nextDay = new Date(checkInDate);
  nextDay.setDate(checkInDate.getDate() + 1);

  // Format the next date as 'YYYY-MM-DD'
  var nextDateString = nextDay.toISOString().split('T')[0];

  // Set the value of the Check-Out date
  document.getElementById('checkOutDate').value = nextDateString;
});



