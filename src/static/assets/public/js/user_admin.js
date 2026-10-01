```javascript
document.addEventListener("DOMContentLoaded", function () {
    const roleField = document.getElementById("id_role");

    if (!roleField) {
        return;
    }

    const studentFields = document.querySelectorAll(
        ".student-fields"
    );

    const teacherFields = document.querySelectorAll(
        ".teacher-fields"
    );

    function toggleFields() {
        const role = roleField.value;

        studentFields.forEach(function (field) {
            field.style.display =
                role === "student" ? "" : "none";
        });

        teacherFields.forEach(function (field) {
            field.style.display =
                role === "teacher" ? "" : "none";
        });
    }

    roleField.addEventListener(
        "change",
        toggleFields
    );

    toggleFields();
});
```
