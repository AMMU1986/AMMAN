/*
=====================================================================
  QUESTION 2  |  STUDENT ID CARD APPLICATION (LOGIC)
  -----------------------------------------------------------------
  Student Name : AMMAN JAKHAR
  Student UID  : 2025EB01187
  Date of Birth: 29.08.1986
  -----------------------------------------------------------------
  File         : StudentApp.js
  Purpose      : Supplies the three graded pieces of behaviour:
                   (1) five independent field-validation routines,
                   (2) a Student class whose object is printed with
                       console.log, and
                   (3) helper functions that save/read a cookie.
                 Section 4 wires everything to the form's submit.
=====================================================================
*/

"use strict";                                 // Opt into stricter JS error checking

/* ==================================================================
   SECTION 1 : FIELD VALIDATION (5 checks)              [5 points]
   Each routine returns "" (empty string) when the input is good,
   or a short, readable message describing what went wrong.
   ================================================================== */

// Check 1 : Full name must be letters/spaces only and 3+ characters long.
function validateFullName(value) {
    const name = value.trim();                // Drop surrounding whitespace
    if (name === "") {                        // Nothing typed at all?
        return "Full name is required.";      // Ask the user to fill it in
    }
    if (!/^[A-Za-z ]{3,}$/.test(name)) {      // Only letters/spaces, min length 3
        return "Name must be at least 3 letters (alphabets and spaces only).";
    }
    return "";                                // Passed every rule
}

// Check 2 : UID must match 4 digits + 2 letters + 5 digits (e.g. 2025EB01187).
function validateUID(value) {
    const uid = value.trim().toUpperCase();   // Trim and normalise letters to caps
    if (uid === "") {                         // Empty field?
        return "UID is required.";
    }
    if (!/^[0-9]{4}[A-Z]{2}[0-9]{5}$/.test(uid)) { // Enforce the exact pattern
        return "UID must look like 2025EB01187 (4 digits, 2 letters, 5 digits).";
    }
    return "";                                // Valid UID
}

// Check 3 : Email must contain text, an @, and a dotted domain.
function validateEmail(value) {
    const email = value.trim();               // Remove stray spaces
    if (email === "") {                       // Empty field?
        return "Email is required.";
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { // Simple but solid email shape
        return "Please enter a valid email address.";
    }
    return "";                                // Looks like an email
}

// Check 4 : Phone must be exactly ten digits.
function validatePhone(value) {
    const phone = value.trim();               // Clean up whitespace
    if (phone === "") {                       // Empty field?
        return "Phone number is required.";
    }
    if (!/^[0-9]{10}$/.test(phone)) {         // Exactly 10 numeric characters
        return "Phone number must be exactly 10 digits.";
    }
    return "";                                // Valid phone number
}

// Check 5 : Date of birth is required and must sit in the past.
function validateDOB(value) {
    if (value === "") {                       // No date chosen?
        return "Date of birth is required.";
    }
    const dob = new Date(value);              // Convert the picker value to a Date
    const today = new Date();                 // Current moment for comparison
    if (dob >= today) {                       // A future (or today) DOB is impossible
        return "Date of birth must be in the past.";
    }
    return "";                                // Valid date of birth
}

/* Helper : paint or clear the inline error text for one field,
   and toggle the red ".invalid" highlight on its input. */
function showError(fieldId, message) {
    const input = document.getElementById(fieldId);         // The input element
    const errorBox = document.getElementById("err-" + fieldId); // Its message slot
    errorBox.textContent = message;           // Write (or blank out) the message
    if (message === "") {                     // No message means the field is fine
        input.classList.remove("invalid");    // Remove the red highlight
    } else {                                  // Otherwise flag the problem
        input.classList.add("invalid");       // Add the red highlight
    }
}

/* ==================================================================
   SECTION 2 : STUDENT CLASS + OBJECT USAGE             [3 points]
   ================================================================== */

class Student {                               // Blueprint for one student record
    constructor(fullName, uid, email, phone, dob, course) { // Runs when "new Student(...)" is called
        this.fullName = fullName;             // Store the full name on the object
        this.uid = uid;                       // Store the UID
        this.email = email;                   // Store the email address
        this.phone = phone;                   // Store the phone number
        this.dob = dob;                       // Store the date of birth (string)
        this.course = course;                 // Store the chosen course
    }

    // Work out the student's age in whole years from the stored DOB.
    getAge() {
        const birth = new Date(this.dob);     // Parse the DOB into a Date
        const now = new Date();               // Today's date
        let age = now.getFullYear() - birth.getFullYear(); // Rough year difference
        const monthDiff = now.getMonth() - birth.getMonth(); // Compare months
        // Subtract a year if the birthday has not occurred yet this year
        if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birth.getDate())) {
            age--;                            // Birthday still to come this year
        }
        return age;                           // Final, corrected age
    }

    // Produce a tidy one-line description of this student.
    getSummary() {
        return `${this.fullName} (UID: ${this.uid}) | ${this.course} | Age: ${this.getAge()}`;
    }
}

/* ==================================================================
   SECTION 3 : COOKIE SAVE / READ                       [2 points]
   ================================================================== */

// Save a cookie "name=value" that stops being valid after "days" days.
function setCookie(name, value, days) {
    const expires = new Date();               // Start from right now
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000); // Add N days in ms
    document.cookie = name + "=" + encodeURIComponent(value) + // Encode to stay cookie-safe
                      ";expires=" + expires.toUTCString() +    // When it should expire
                      ";path=/";                               // Available site-wide
}

// Read back the value of a named cookie, or "" when it is absent.
function getCookie(name) {
    const cookies = document.cookie.split(";"); // Split the cookie string into pieces
    for (let i = 0; i < cookies.length; i++) {   // Walk through each cookie
        const parts = cookies[i].trim().split("="); // Separate name from value
        if (parts[0] === name) {                 // Found the one we want?
            return decodeURIComponent(parts[1]); // Decode and return its value
        }
    }
    return "";                                   // Not found
}

/* ==================================================================
   SECTION 4 : FORM WIRING
   Connects validation, the Student class, and the cookie helpers
   to the form's submit event.
   ================================================================== */

document.addEventListener("DOMContentLoaded", function () { // Wait until the DOM is ready

    // When the page opens, report any student kept from a previous visit.
    const saved = getCookie("lastStudent");     // Try to read the stored cookie
    if (saved !== "") {                         // Only log if something was stored
        console.log("Retrieved previously saved student from cookie: " + saved);
    }

    const form = document.getElementById("studentForm"); // Grab the form element

    form.addEventListener("submit", function (event) {    // React to the submit button
        event.preventDefault();                 // Stop the browser reloading the page

        // Read the live value of every field.
        const fullName = document.getElementById("fullName").value;
        const uid      = document.getElementById("uid").value;
        const email    = document.getElementById("email").value;
        const phone    = document.getElementById("phone").value;
        const dob      = document.getElementById("dob").value;
        const course   = document.getElementById("course").value;

        // Run all checks and gather each result in one object.
        const errors = {
            fullName: validateFullName(fullName),
            uid:      validateUID(uid),
            email:    validateEmail(email),
            phone:    validatePhone(phone),
            dob:      validateDOB(dob),
            course:   course === "" ? "Please select a course." : "" // Extra dropdown check
        };

        // Show (or clear) every message and remember whether all passed.
        let isValid = true;                     // Assume success until proven otherwise
        for (const field in errors) {           // Loop over each result
            showError(field, errors[field]);    // Reflect it on screen
            if (errors[field] !== "") {          // A non-empty message = failure
                isValid = false;                 // Mark the form invalid
            }
        }

        // Abort if anything failed validation.
        if (!isValid) {
            console.log("Validation failed. Please correct the highlighted fields.");
            return;                             // Do not build a Student object
        }

        // ---- Everything is valid : build the Student object ----
        const student = new Student(fullName, uid, email, phone, dob, course);

        // Print the object and its derived details to the console.
        console.log("=== New Student object created ===");
        console.log(student);                   // The raw object (expandable in DevTools)
        console.log("Summary : " + student.getSummary()); // One-line summary
        console.log("Age     : " + student.getAge() + " years"); // Computed age

        // ---- Persist the summary in a cookie for 7 days ----
        setCookie("lastStudent", student.getSummary(), 7); // Write the cookie
        console.log("Student saved to cookie: " + getCookie("lastStudent")); // Read it back

        // ---- Reveal the green success banner on the page ----
        const result = document.getElementById("result"); // The banner element
        result.style.display = "block";         // Make it visible
        result.textContent =                    // Fill it with a readable summary
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
