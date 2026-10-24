/*
====================================================================
  Student ID Card Application - Logic (Question 2)
  --------------------------------------------------------------
  Student Name : AMMAN JAKHAR
  Student UID  : 2025EB01187
  Date of Birth: 29.08.1986
  --------------------------------------------------------------
  File         : StudentApp.js
  Description  : Contains
                   (1) five field validation functions,
                   (2) a Student class and object usage with
                       console.log output, and
                   (3) cookie store / retrieve helpers.
====================================================================
*/

"use strict";

/* ==================================================================
   SECTION 1 : VALIDATION FUNCTIONS (5 fields)  [5 points]
   Each function returns an empty string "" when the value is valid,
   otherwise it returns a human-readable error message.
   ================================================================== */

// Field 1 : Full Name - letters and spaces only, at least 3 characters
function validateFullName(value) {
    const name = value.trim();
    if (name === "") {
        return "Full name is required.";
    }
    if (!/^[A-Za-z ]{3,}$/.test(name)) {
        return "Name must be at least 3 letters (alphabets and spaces only).";
    }
    return "";
}

// Field 2 : UID - exactly the pattern 4 digits + 2 letters + 5 digits (e.g. 2025EB01187)
function validateUID(value) {
    const uid = value.trim().toUpperCase();
    if (uid === "") {
        return "UID is required.";
    }
    if (!/^[0-9]{4}[A-Z]{2}[0-9]{5}$/.test(uid)) {
        return "UID must look like 2025EB01187 (4 digits, 2 letters, 5 digits).";
    }
    return "";
}

// Field 3 : Email - standard email pattern
function validateEmail(value) {
    const email = value.trim();
    if (email === "") {
        return "Email is required.";
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        return "Please enter a valid email address.";
    }
    return "";
}

// Field 4 : Phone - exactly 10 digits
function validatePhone(value) {
    const phone = value.trim();
    if (phone === "") {
        return "Phone number is required.";
    }
    if (!/^[0-9]{10}$/.test(phone)) {
        return "Phone number must be exactly 10 digits.";
    }
    return "";
}

// Field 5 : Date of Birth - required and must be a past date
function validateDOB(value) {
    if (value === "") {
        return "Date of birth is required.";
    }
    const dob = new Date(value);
    const today = new Date();
    if (dob >= today) {
        return "Date of birth must be in the past.";
    }
    return "";
}

/* Helper : show or clear the inline error message for a single field. */
function showError(fieldId, message) {
    const input = document.getElementById(fieldId);
    const errorBox = document.getElementById("err-" + fieldId);
    errorBox.textContent = message;
    if (message === "") {
        input.classList.remove("invalid");
    } else {
        input.classList.add("invalid");
    }
}

/* ==================================================================
   SECTION 2 : STUDENT CLASS + OBJECT USAGE  [3 points]
   ================================================================== */

class Student {
    constructor(fullName, uid, email, phone, dob, course) {
        this.fullName = fullName;
        this.uid = uid;
        this.email = email;
        this.phone = phone;
        this.dob = dob;
        this.course = course;
    }

    // Returns the student's age calculated from the DOB.
    getAge() {
        const birth = new Date(this.dob);
        const now = new Date();
        let age = now.getFullYear() - birth.getFullYear();
        const monthDiff = now.getMonth() - birth.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birth.getDate())) {
            age--;
        }
        return age;
    }

    // Returns a formatted one-line summary of the student object.
    getSummary() {
        return `${this.fullName} (UID: ${this.uid}) | ${this.course} | Age: ${this.getAge()}`;
    }
}

/* ==================================================================
   SECTION 3 : COOKIE STORE / RETRIEVE  [2 points]
   ================================================================== */

// Store a cookie that expires after the given number of days.
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + encodeURIComponent(value) +
                      ";expires=" + expires.toUTCString() + ";path=/";
}

// Retrieve the value of a named cookie (returns "" if not found).
function getCookie(name) {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
        const parts = cookies[i].trim().split("=");
        if (parts[0] === name) {
            return decodeURIComponent(parts[1]);
        }
    }
    return "";
}

/* ==================================================================
   SECTION 4 : FORM EVENT HANDLING
   Ties the above pieces together on form submission.
   ================================================================== */

document.addEventListener("DOMContentLoaded", function () {

    // On load, show any previously stored student (from the cookie).
    const saved = getCookie("lastStudent");
    if (saved !== "") {
        console.log("Retrieved previously saved student from cookie: " + saved);
    }

    const form = document.getElementById("studentForm");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // stop the page from reloading

        // Read the current field values.
        const fullName = document.getElementById("fullName").value;
        const uid      = document.getElementById("uid").value;
        const email    = document.getElementById("email").value;
        const phone    = document.getElementById("phone").value;
        const dob      = document.getElementById("dob").value;
        const course   = document.getElementById("course").value;

        // Run every validation and collect the results.
        const errors = {
            fullName: validateFullName(fullName),
            uid:      validateUID(uid),
            email:    validateEmail(email),
            phone:    validatePhone(phone),
            dob:      validateDOB(dob),
            course:   course === "" ? "Please select a course." : ""
        };

        // Display each error (or clear it) and track overall validity.
        let isValid = true;
        for (const field in errors) {
            showError(field, errors[field]);
            if (errors[field] !== "") {
                isValid = false;
            }
        }

        // Stop here if any field failed validation.
        if (!isValid) {
            console.log("Validation failed. Please correct the highlighted fields.");
            return;
        }

        // ---- All fields valid : create a Student object ----
        const student = new Student(fullName, uid, email, phone, dob, course);

        // Display the object and its details in the console log.
        console.log("=== New Student object created ===");
        console.log(student);
        console.log("Summary : " + student.getSummary());
        console.log("Age     : " + student.getAge() + " years");

        // ---- Store the student summary in a cookie (valid 7 days) ----
        setCookie("lastStudent", student.getSummary(), 7);
        console.log("Student saved to cookie: " + getCookie("lastStudent"));

        // ---- Show a success banner on the page ----
        const result = document.getElementById("result");
        result.style.display = "block";
        result.textContent =
            "ID Card generated successfully!\n" +
            "Name   : " + student.fullName + "\n" +
            "UID    : " + student.uid + "\n" +
            "Email  : " + student.email + "\n" +
            "Phone  : " + student.phone + "\n" +
            "DOB    : " + student.dob + "\n" +
            "Course : " + student.course + "\n" +
            "Age    : " + student.getAge() + " years\n" +
            "(Details also logged to the console and saved in a cookie.)";
    });
});
