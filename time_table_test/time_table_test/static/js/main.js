const primaryForm = $('#primaryForm');
const days = $('#days');
const classes = $('#classes');


$(function () {

  $('select').material_select();

  $('#classesDiv').change(function () {
    $('#daysDiv').show();
  });
  $('#daysDiv').change(function () {
    $('#btnProceed').show();
  });


  primaryForm.submit(() => {
    console.log(days.val());
    console.log(classes.val());
    return false;
  });

});


let getDaysForClasses = () => {
  var daysDiv = $('#daysDiv');
  daysDiv.html('');
  for (c = 1; c <= classes.val(); c++) {
    daysDiv.append(`
      <div class="row">
        <div class="col s12 m6 l4">
          For Class ${c} :
        </div>
        <div class="col s12 m6 l4">
          <select id="days" name="class${c}">
              <option value="0" disabled selected>Days</option>
              <option value="{{n}}" ng-repeat="n in range(1,7)">{{n}}</option>
            </select>
          <label>Days in a week?</label>
        </div>
      </div>
    `);
    $('select').material_select('destroy');
    $('select').material_select();

  }
}
