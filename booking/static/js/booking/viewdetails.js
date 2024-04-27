
//Handle click event
function handleClick(event) {
    var labels = document.querySelectorAll('.nav-item');
    
    labels.forEach(function(label) {
        label.classList.remove('active');
    });
    if (event.target.tagName === 'LI') {
        event.target.classList.add('active');
    }
}

//Bookroom API
function bookRoom() {
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = '/hotelreview/';
    var roomJsonList = document.getElementById('hide-123').value;
    var unescapedValue1 = roomJsonList.replace(/&quot;/g, '"');
    var parsedJSON1 = JSON.parse(unescapedValue1);
    var datalist = document.getElementById('data-123').value;
    var unescapedValue = datalist.replace(/&quot;/g, '"');
    var parsedJSON = JSON.parse(unescapedValue);
    var hotelCode = parsedJSON.HotelCode; 
    var hotelNameInputElement =  document.getElementById('hotelNameContainer').value;
    if (hotelNameInputElement) {
        var hotelName = hotelNameInputElement;
        var csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
        var csrfTokenField = document.createElement('input');
        csrfTokenField.type = 'hidden';
        csrfTokenField.name = 'csrfmiddlewaretoken';
        csrfTokenField.value = csrfToken;
        form.appendChild(csrfTokenField);
        var roomJsonElement = document.createElement('input');
        roomJsonElement.type = 'hidden';
        roomJsonElement.name = 'roomJsonElement';
        roomJsonElement.value = JSON.stringify(parsedJSON1);
        form.appendChild(roomJsonElement);
        var hotelNameField = document.createElement('input');
        hotelNameField.type = 'hidden';
        hotelNameField.name = 'hotelName';
        hotelNameField.value = hotelName;
        form.appendChild(hotelNameField);
        var hide123Value = document.createElement('input');
        hide123Value.type = 'hidden';
        hide123Value.name = 'hide123Value';
        hide123Value.value = JSON.stringify(parsedJSON);
        form.appendChild(hide123Value);
        var categoryid1 = document.getElementById('categoryid').value;
        var categoryidField = document.createElement('input');
        categoryidField.type = 'hidden';
        categoryidField.name = 'categoryid1';
        categoryidField.value = categoryid1;
        form.appendChild(categoryidField);
        document.body.appendChild(form);
        form.submit();
    } else {
        console.error('Hotel name input element not found.');
    }
}

function bookRoom() {
    var hiddenPhoneNumber = document.getElementById('hiddenPhoneNumber');
    
    if (hiddenPhoneNumber && hiddenPhoneNumber.value) {
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/hotelreview/';
        var roomJsonList = document.getElementById('hide-123').value;
        var unescapedValue1 = roomJsonList.replace(/&quot;/g, '"');
        var parsedJSON1 = JSON.parse(unescapedValue1);
        var datalist = document.getElementById('data-123').value;
        var unescapedValue = datalist.replace(/&quot;/g, '"');
        var parsedJSON = JSON.parse(unescapedValue);
        var hotelCode = parsedJSON.HotelCode; 
        var hotelNameInputElement =  document.getElementById('hotelNameContainer').value;
        if (hotelNameInputElement) {
            var hotelName = hotelNameInputElement;
            var csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
            var csrfTokenField = document.createElement('input');
            csrfTokenField.type = 'hidden';
            csrfTokenField.name = 'csrfmiddlewaretoken';
            csrfTokenField.value = csrfToken;
            form.appendChild(csrfTokenField);
            var roomJsonElement = document.createElement('input');
            roomJsonElement.type = 'hidden';
            roomJsonElement.name = 'roomJsonElement';
            roomJsonElement.value = JSON.stringify(parsedJSON1);
            form.appendChild(roomJsonElement);
            var hotelNameField = document.createElement('input');
            hotelNameField.type = 'hidden';
            hotelNameField.name = 'hotelName';
            hotelNameField.value = hotelName;
            form.appendChild(hotelNameField);
            var hide123Value = document.createElement('input');
            hide123Value.type = 'hidden';
            hide123Value.name = 'hide123Value';
            hide123Value.value = JSON.stringify(parsedJSON);
            form.appendChild(hide123Value);
            var categoryid1 = document.getElementById('categoryid').value;
            var categoryidField = document.createElement('input');
            categoryidField.type = 'hidden';
            categoryidField.name = 'categoryid1';
            categoryidField.value = categoryid1;
            form.appendChild(categoryidField);
            document.body.appendChild(form);
            form.submit();
        } else {
            console.error('Hotel name input element not found.');
        }
    } else {
        $("#log-btn").click();
    }
}
