$(function () {
  $(".ham-icon").click(function () {
    $(".primary-menu").addClass("active");
    $("body").addClass("overflow-hidden");
    $(".overlay").addClass("active");

    $(".ham-close").click(function () {
      $(".primary-menu").removeClass("active");
      $("body").removeClass("overflow-hidden");
      $(".overlay").removeClass("active");
    });
  });

  $(".overlay").click(function () {
    $(".primary-menu").removeClass("active");
    $("body").removeClass("overflow-hidden");
    $(".overlay").removeClass("active");
  });
  

  $(document).ready(function() {
    $("#appointment-form").on('submit', function(e) {
        e.preventDefault();  // Prevent the default form submission
        var button = document.getElementById("book-now");
        button.disabled = true;

        
        // Fetch CSRF token from cookies (Django's recommended method)
        var csrftoken = $("#appointment-form input[name='csrfmiddlewaretoken']").val();
        
        // Fetch values from form fields
        var doctor = $("#appointment-form select").val();
        var name = $("#appointment-form input[name='name']").val();
        var phone = $("#appointment-form input[name='phone']").val();
        var email = $("#appointment-form input[name='email']").val();
        var date = $("#appointment-form input[type='date']").val();
        
        // Prepare data to send via AJAX
        var formData = {
            doctor: doctor,
            name: name,
            phone: phone,
            email: email,
            date: date,
            csrfmiddlewaretoken: csrftoken  // Include CSRF token in the data
        };
        
        // Send AJAX POST request
        $.ajax({
            type: "POST",
            url: window.location.href,  // Send to the current URL
            data: formData,
            beforeSend: function(xhr, settings) {
                // Set CSRF token in the header for Django
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                $("#book-now").html("Processing...");
            },
            success: function(response) {
                window.location.href = response.data;
            },
            error: function(xhr, status, error) {
                console.error("AJAX request failed:", error);
            }
        });
    });
});

// Function to get CSRF token from cookies (Django's recommended method)
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



});
