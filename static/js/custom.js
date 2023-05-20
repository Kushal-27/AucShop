// // to get current year
// function getYear() {
//     var currentDate = new Date();
//     var currentYear = currentDate.getFullYear();
//     document.querySelector("#displayYear").innerHTML = currentYear;
// }

// getYear();

$(document).ready(function () {
  $(".add_cart_btn").click(function (e) {
    e.preventDefault();
    var product_id = this.dataset.product[0];
    console.log(product_id)
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/add-to-cart",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
    });
  });
});



