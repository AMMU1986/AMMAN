/*
=====================================================================
  QUESTION 2 - STUDENT ID CARD APPLICATION (the logic)
  -----------------------------------------------------------------
  Author : AMMAN JAKHAR  |  UID : 2025EB01187  |  DOB : 29.08.1986
  -----------------------------------------------------------------
  This file carries the three things Q2 is marked on:
      SECTION 1  five separate validation functions        [5 marks]
      SECTION 2  a Student class + an object I console.log  [3 marks]
      SECTION 3  cookie save + read helpers                 [2 marks]
  SECTION 4 is the "glue": it waits for the page, listens for the
  submit button, and calls the pieces above in order.

  Design choice I made throughout: every validator RETURNS a string.
  An empty string "" means "all good"; any other text is the exact
  message to show the user. Returning instead of alert()-ing keeps
  the checks pure and easy to reuse or test on their own.
=====================================================================
*/

"use strict";                                 // strict mode: turns silent mistakes into real errors early

/* ==================================================================
   SECTION 1 : THE FIVE FIELD CHECKS                     [5 marks]
   Each one takes the raw text from a field and hands back "" or a
   message. I trim() first everywhere so stray spaces never pass by
   accident (e.g. "   " should still count as empty).
   ================================================================== */

// (1) Full name: letters and spaces only, and at least 3 characters.
function validateFullName(value) {
    const name = value.trim();                // remove leading/trailing spaces first
    if (name === "") {                        // guard the empty case before the regex
        return "Full name is required.";
    }
    // ^...$ anchors the WHOLE string; [A-Za-z ] = letters or space; {3,} = three or more
    if (!/^[A-Za-z ]{3,}$/.test(name)) {
        return "Name must be at least 3 letters (alphabets and spaces only).";
    }
    return "";                                // reached here => the name is fine
}

// (2) UID: the fixed shape 4 digits + 2 letters + 5 digits, e.g. 2025EB01187.
function validateUID(value) {
    const uid = value.trim().toUpperCase();   // force caps so "eb" and "EB" are both accepted
    if (uid === "") {
        return "UID is required.";
    }
    // [0-9]{4} four digits, [A-Z]{2} two letters, [0-9]{5} five digits - nothing else allowed
    if (!/^[0-9]{4}[A-Z]{2}[0-9]{5}$/.test(uid)) {
        return "UID must look like 2025EB01187 (4 digits, 2 letters, 5 digits).";
    }
    return "";
}

// (3) Email: must have "something @ something . something" with no spaces.
function validateEmail(value) {
    const email = value.trim();
    if (email === "") {
        return "Email is required.";
    }
    // [^\s@]+ = one-or-more chars that are NOT a space or @, repeated around an @ and a dot
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        return "Please enter a valid email address.";
    }
    return "";
}

// (4) Phone: exactly ten digits - no +, no spaces, no dashes.
function validatePhone(value) {
    const phone = value.trim();
    if (phone === "") {
        return "Phone number is required.";
    }
    if (!/^[0-9]{10}$/.test(phone)) {         // {10} pins the length to ten, the ^$ forbid extras
        return "Phone number must be exactly 10 digits.";
    }
    return "";
}

// (5) Date of birth: required, and it has to be a date that already happened.
function validateDOB(value) {
    if (value === "") {                       // the date picker gives "" when untouched
        return "Date of birth is required.";
    }
    const dob = new Date(value);              // turn the "YYYY-MM-DD" string into a real Date
    const today = new Date();                 // "now", to compare against
    if (dob >= today) {                       // being born today or in the future makes no sense
        return "Date of birth must be in the past.";
    }
    return "";
}

/* Small UI helper (shared by all five checks above).
   Given a field id and a message, it writes the message into that
   field's .error box and toggles the red ".invalid" look on/off. */
function showError(fieldId, message) {
    const input = document.getElementById(fieldId);          // the input/select itself
    const errorBox = document.getElementById("err-" + fieldId); // its matching error <div>
    errorBox.textContent = message;           // textContent (not innerHTML) = safe, no HTML injection
    if (message === "") {
        input.classList.remove("invalid");    // happy path: strip the red styling
    } else {
        input.classList.add("invalid");       // problem: paint it red
    }
}

/* ==================================================================
   SECTION 2 : THE STUDENT CLASS                         [3 marks]
   A class is my blueprint; "new Student(...)" stamps out one object
   from it. I gave it two methods so the object can describe itself.
   ================================================================== */

class Student {
    // the constructor copies each argument onto the new object as a property
    constructor(fullName, uid, email, phone, dob, course) {
        this.fullName = fullName;             // "this" = the specific object being built
        this.uid = uid;
        this.email = email;
        this.phone = phone;
        this.dob = dob;                       // kept as the raw "YYYY-MM-DD" string
        this.course = course;
    }

    // method: turn the stored DOB into an age in whole years
    getAge() {
        const birth = new Date(this.dob);     // parse the stored string
        const now = new Date();
        let age = now.getFullYear() - birth.getFullYear(); // first pass: just subtract the years
        const monthDiff = now.getMonth() - birth.getMonth(); // how far we are into the year, by month
        // if this year's birthday hasn't arrived yet, I counted one year too many, so take it back
        if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birth.getDate())) {
            age--;
        }
        return age;
    }

    // method: a compact one-liner about the student (I log and store this)
    getSummary() {
        // template literal (backticks) lets me drop values straight into the text with ${...}
        return `${this.fullName} (UID: ${this.uid}) | ${this.course} | Age: ${this.getAge()}`;
    }
}

/* ==================================================================
   SECTION 3 : COOKIES                                   [2 marks]
   Two tiny helpers. setCookie writes one that expires in N days;
   getCookie reads one back by name. I encode/decode the value so
   spaces and symbols survive the trip (cookies dislike raw spaces).
   ================================================================== */

// write document.cookie = "name=value; expires=...; path=/"
function setCookie(name, value, days) {
    const expires = new Date();               // start from now...
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000); // ...+ N days expressed in milliseconds
    document.cookie = name + "=" + encodeURIComponent(value) + // encode makes the value cookie-safe
                      ";expires=" + expires.toUTCString() +    // the browser deletes it after this moment
                      ";path=/";                               // "/" = valid across the whole site
}

// read back a single cookie's value, or "" if that name isn't stored
function getCookie(name) {
    const cookies = document.cookie.split(";"); // the whole cookie string -> ["a=1"," b=2", ...]
    for (let i = 0; i < cookies.length; i++) {
        const parts = cookies[i].trim().split("="); // trim the leading space, then split name from value
        if (parts[0] === name) {              // is this the cookie I asked for?
            return decodeURIComponent(parts[1]); // undo the encoding from setCookie and return it
        }
    }
    return "";                                // fell through the loop => not found
}

/* ==================================================================
   SECTION 4 : WIRING IT ALL TOGETHER
   Nothing here runs until the HTML is parsed, so I wrap it in the
   DOMContentLoaded event - otherwise getElementById could return
   null because the form wouldn't exist yet.
   ================================================================== */

document.addEventListener("DOMContentLoaded", function () {

    // On every load, peek at the cookie so a returning user is recognised.
    const saved = getCookie("lastStudent");
    if (saved !== "") {                       // only shout about it if there actually is one
        console.log("Retrieved previously saved student from cookie: " + saved);
    }

    const form = document.getElementById("studentForm");

    // the single event that drives the whole page: the form being submitted
    form.addEventListener("submit", function (event) {
        event.preventDefault();               // stop the browser's default "reload and clear" behaviour

        // snapshot every field's current value
        const fullName = document.getElementById("fullName").value;
        const uid      = document.getElementById("uid").value;
        const email    = document.getElementById("email").value;
        const phone    = document.getElementById("phone").value;
        const dob      = document.getElementById("dob").value;
        const course   = document.getElementById("course").value;

        // run all checks once and keep each result under its field's name
        const errors = {
            fullName: validateFullName(fullName),
            uid:      validateUID(uid),
            email:    validateEmail(email),
            phone:    validatePhone(phone),
            dob:      validateDOB(dob),
            // the dropdown isn't one of the five, but I still refuse an empty choice
            course:   course === "" ? "Please select a course." : ""
        };

        // paint every message (or clear it) and note if ANY field failed
        let isValid = true;                   // optimistic until proven otherwise
        for (const field in errors) {         // loop the keys: fullName, uid, ...
            showError(field, errors[field]);  // reflect this field's result on screen
            if (errors[field] !== "") {       // a non-empty string means this field is bad
                isValid = false;
            }
        }

        // if anything was wrong, stop here - do NOT build an object from bad data
        if (!isValid) {
            console.log("Validation failed. Please correct the highlighted fields.");
            return;
        }

        // ---- all clear: build the Student object from the clean inputs ----
        const student = new Student(fullName, uid, email, phone, dob, course);

        // show the object (and its derived info) in the browser console
        console.log("=== New Student object created ===");
        console.log(student);                 // logging the object itself lets me expand it in DevTools
        console.log("Summary : " + student.getSummary());
        console.log("Age     : " + student.getAge() + " years");

        // ---- remember this student for 7 days via a cookie ----
        setCookie("lastStudent", student.getSummary(), 7);
        console.log("Student saved to cookie: " + getCookie("lastStudent")); // read it straight back as proof

        // ---- finally, reveal the green banner with a human-readable summary ----
        const result = document.getElementById("result");
        result.style.display = "block";       // flip it from hidden to visible
        // each "\n" becomes a real line break because the CSS set white-space: pre-line
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
