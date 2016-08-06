/**
 * Created by Aravind Balla on 06-08-2016.
 */
$(document).ready(function() {
    $('select').material_select();

    $('#id_date').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 5, // Creates a dropdown of 15 years to control year
        format: 'yyyy-mm-dd',
    });

    $('#id_starttime, #id_endtime').pickatime({
        default: 'now',
        twelvehour: false,
        donetext: 'OK',
        autoclose: false,
        vibrate: true,
    });
});
