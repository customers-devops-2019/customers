$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_first_name").val(res.firstname);
        $("#customer_last_name").val(res.lastname);
        $("#customer_email").val(res.email);
        $("#customer_address_1").val(res.address.address1);
        $("#customer_address_2").val(res.address.address2);
        $("#customer_city").val(res.address.city);
        $("#customer_province").val(res.address.province);
        $("#customer_country").val(res.address.country);
        $("#customer_zip").val(res.address.zip);
        if (res.subscribed == true) {
            $("#customer_subscribed").val("true");
        } else {
            $("#customer_subscribed").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_first_name").val("");
        $("#customer_last_name").val("");
        $("#customer_email").val("");
        $("#customer_subscribed").val("");
        $("#customer_address_1").val("");
        $("#customer_address_2").val("");
        $("#customer_city").val("");
        $("#customer_province").val("");
        $("#customer_country").val("");
        $("#customer_zip").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        var firstname = $("#customer_first_name").val();
        var lastname = $("#customer_last_name").val();
        var email = $("#customer_email").val();
        var subscribed = $("#customer_subscribed").val() == "true";
        var address1 = $("#customer_address_1").val();
        var address2 = $("#customer_address_2").val();
        var city = $("#customer_city").val();
        var province = $("#customer_province").val();
        var country = $("#customer_country").val();
        var zip = $("#customer_zip").val();

        var data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "subscribed": subscribed,
            "address": {
                "address1": address1,
                "address2":address2,
                "city": city,
                "province": province,
                "country": country,
                "zip": zip
            }
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        var customer_id = $("#customer_id").val();
        var firstname = $("#customer_first_name").val();
        var lastname = $("#customer_last_name").val();
        var email = $("#customer_email").val();
        var subscribed = $("#customer_subscribed").val() == "true";
        var address1 = $("#customer_address_1").val();
        var address2 = $("#customer_address_2").val();
        var city = $("#customer_city").val();
        var province = $("#customer_province").val();
        var country = $("#customer_country").val();
        var zip = $("#customer_zip").val();

        var data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "subscribed": subscribed,
            "address": {
                "address1": address1,
                "address2":address2,
                "city": city,
                "province": province,
                "country": country,
                "zip": zip
            }
        };

        var ajax = $.ajax({
            type: "PUT",
            url: "/customers/" + customer_id,
            contentType:"application/json",
            data: JSON.stringify(data)
        });

        ajax.done(function(res){
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {
        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType:"application/json",
            data: ''
        });

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + customer_id,
            contentType:"application/json",
            data: ''
        });

        ajax.done(function(res){
            clear_form_data();
            flash_message("Customer Deleted!");
        });

        ajax.fail(function(res){
            flash_message("Server error!");
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data();
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        var firstname = $("#customer_first_name").val();
        var lastname = $("#customer_last_name").val();
        var email = $("#customer_email").val();
        var subscribed = $("#customer_subscribed").val() == "true";
        var address1 = $("#customer_address_1").val();
        var address2 = $("#customer_address_2").val();
        var city = $("#customer_city").val();
        var province = $("#customer_province").val();
        var country = $("#customer_country").val();
        var zip = $("#customer_zip").val();

        var queryString = "";

        if (firstname) {
            queryString += 'firstname=' + firstname;
        }
        if (lastname) {
            if (queryString.length > 0) {
                queryString += '&lastname=' + lastname;
            } else {
                queryString += 'lastname=' + lastname;
            }
        }if (email) {
            if (queryString.length > 0) {
                queryString += '&email=' + email;
            } else {
                queryString += 'email=' + email;
            }
        }if (subscribed) {
            if (queryString.length > 0) {
                queryString += '&subscribed=' + subscribed;
            } else {
                queryString += 'subscribed=' + subscribed;
            }
        }if (address1) {
            if (queryString.length > 0) {
                queryString += '&address1=' + address1;
            } else {
                queryString += 'address1=' + address1;
            }
        }if (address2) {
            if (queryString.length > 0) {
                queryString += '&address2=' + address2;
            } else {
                queryString += 'address2=' + address2;
            }
        }if (city) {
            if (queryString.length > 0) {
                queryString += '&city=' + city;
            } else {
                queryString += 'city=' + city;
            }
        }if (province) {
            if (queryString.length > 0) {
                queryString += '&province=' + province;
            } else {
                queryString += 'province=' + province;
            }
        }if (country) {
            if (queryString.length > 0) {
                queryString += '&country=' + country;
            } else {
                queryString += 'country=' + country;
            }
        }if (zip) {
            if (queryString.length > 0) {
                queryString += '&zip=' + zip;
            } else {
                queryString += 'zip=' + zip;
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType:"application/json",
            data: ''
        });

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>';
            header += '<th style="width:10%">ID</th>';
            header += '<th style="width:10%">First Name</th>';
            header += '<th style="width:10%">Last Name</th>';
            header += '<th style="width:10%">Email</th>';
            header += '<th style="width:10%">Subscribed</th>';
            header += '<th style="width:10%">Address 1</th>';
            header += '<th style="width:10%">Address 2</th>';
            header += '<th style="width:10%">City</th>';
            header += '<th style="width:10%">Province</th>';
            header += '<th style="width:10%">Country</th>';
            header += '<th style="width:10%">Zip</th></tr>';
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                var customer = res[i];
                var row = "<tr><td>"+customer.id+"</td><td>"+customer.firstname+"</td><td>"+customer.lastname+"</td><td>"+customer.email+"</td><<td>"+customer.subscribed+"</td><td>"+customer.address1+"</td><td>"+customer.address2+"</td><td>"+customer.city+"</td><td>"+customer.province+"</td><td>"+customer.country+"</td><td>"+customer.zip+"</td>/tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });

    });

});
