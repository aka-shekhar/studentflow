
const searchInput = document.getElementById("search");
const studentTable = document.getElementById("studentTable");

searchInput.addEventListener("input", function () {
    const searchValue = searchInput.value.toLowerCase();
    const rows = studentTable.querySelectorAll("tr");

    rows.forEach(function (row) {
        const studentData = row.textContent.toLowerCase();

        if (studentData.includes(searchValue)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});
function showAddForm() {
    const form = document.getElementById("addStudentForm");

    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
const alerts = document.querySelectorAll(".alert");

alerts.forEach(function(alert) {
    setTimeout(function() {
        alert.style.opacity = "0";

        setTimeout(function() {
            alert.remove();
        }, 500);

    }, 3000);
});
const sortSelect = document.getElementById("sortStudents");

sortSelect.addEventListener("change", function () {

    const rows = Array.from(studentTable.querySelectorAll("tr"));

    const sortType = this.value;

    rows.sort((a, b) => {

        if (sortType === "name") {
            return a.cells[1].textContent.localeCompare(
                b.cells[1].textContent
            );
        }

        if (sortType === "roll") {
            return a.cells[0].textContent.localeCompare(
                b.cells[0].textContent,
                undefined,
                { numeric: true }
            );
        }

        if (sortType === "marks") {
            const marksA = Number(a.cells[4].dataset.marks);
            const marksB = Number(b.cells[4].dataset.marks);

            return marksB - marksA;
        }

        return 0;
    });

    rows.forEach(row => studentTable.appendChild(row));
});
const gradeFilter = document.getElementById("gradeFilter");

gradeFilter.addEventListener("change", function () {

    const selectedGrade = this.value;
    const rows = studentTable.querySelectorAll("tr");

    rows.forEach(row => {

        const studentGrade = row.dataset.grade;

        if (selectedGrade === "" || studentGrade === selectedGrade) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }

    });
});