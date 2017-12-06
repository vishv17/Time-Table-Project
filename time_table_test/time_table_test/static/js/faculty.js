const addNewFaculty = $('#addNewFaculty');
const Facultys = $('#Facultys');
const addNewSubject = $('.addNewSubject');
const addSubjects = $('#addSubjects');
const btnSave = $('#btnSave');

const f = 2;

$(function () {

	btnSave.click(() => {
		var datas = [];
		data.Faculty = getfaculty();

		var jsondata = JSON.stringify(datas);
	});


	addNewFaculty.click(() => {
		Facultys.append(`

			<div class="faculty">
				<div class="card card-color">
					<div class="card-content white-text row">
					<span class="card-title">Faculty</span>
					<form class="col s12 m6 l6" style="width: 100%">
						<div class="row row-flex">
							<div class="col s9">
								<div class="input-field row no-Margin">
									<input name="first_name_${f}" placeholder="First Name" id="first_name" type="text" class="validate">
								</div>
								<div class="input-field row no-Margin">
									<input name="position_${f}" placeholder="Position" id="position" type="text" class="validate">
								</div>
								<div class="input-field row no-Margin">
									<input name="workload_${f}" placeholder="Position" id="workload" type="text" class="validate">
								</div>
							</div>
							<div class="input-field col s3 btn-add" onclick="subject(this)">
								<a class="addSubjects btn btn-floating trans_cyan pulse"><i class="material-icons">add</i></a>
							</div>
						</div>
					</form>
				</div>
			</div>
		</div>
		`);

		f++;
	});
});


var AsubjectContent = `
	<div class="row">
		<div class="input-field col s12 no-Margin">
			<input placeholder="Subject" id="subject" type="text" class="validate">
		</div>
		<div class="input-field col s12 no-Margin">
			<input placeholder="Class Name" id="className" type="text" class="validate">
		</div>
	</div>
`;

var newSubject = function (element) {
	$(element).siblings('.row').find('#subjects').append('<hr/>' + AsubjectContent);
};

var subject = function (element) {
	$(element).closest('.faculty').append(`
		<div id="subjectsDiv">
			<div class="card card-color">
				<div class="card-content white-text row">
					<span class="card-title">Subjects</span>
					<form class="col s12 m6 l6" style="width:100%">
						<div id="subjects">${AsubjectContent}</div>
					</form>
				</div>
				<div class="card-action" onclick="newSubject(this)">
					<a class="addNewSubject btn-flat waves-effect waves-dark">
						<i class="material-icons left">add</i>
						Add Subject
					</a>
				</div>
			</div>
		</div>
	`);
	$(element).remove();
};
