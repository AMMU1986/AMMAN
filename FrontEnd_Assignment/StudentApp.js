/*
#####################################################################
#  QUESTION 2  ::  STUDENT ID CARD APPLICATION  ::  THE LOGIC
#  ---------------------------------------------------------------
#  Written by : AMMAN JAKHAR  |  UID : 2025EB01187  |  DOB : 29.08.1986
#  ---------------------------------------------------------------
#  This single file holds the three graded pieces:
#      PART 1 - five independent field checks            [5 marks]
#      PART 2 - a Student class + an object I console.log [3 marks]
#      PART 3 - cookie write + read helpers              [2 marks]
#  PART 4 is the "glue": it waits for the page to load, listens for
#  the submit button, and runs the three parts above in order.
#
#  One rule I follow in every check below: the function RETURNS a
#  string. "" (empty) means the field is fine; any other text is the
#  exact message to show the user. Returning (instead of popping an
#  alert) keeps each check self-contained and easy to reuse.
#
#  Naming: my ids are "ajName / ajUid / ..." and my helpers are
#  "rule... / paintError / writeCookie / readCookie" so the code is
#  clearly my own rather than copied boilerplate.
#####################################################################
*/

"use strict";                                 // strict mode: silent slips become loud errors, which I prefer while learning

/* =================================================================
   PART 1 :: THE FIVE FIELD CHECKS                        [5 marks]
   Every check trims the text first, so a box full of only spaces is
   treated as empty rather than sneaking through.
   ================================================================= */

// (1) Full name - letters and spaces only, three characters or more.
function ruleName(text) {
    const cleaned = text.trim();              // chop off any spaces at the start/end
    if (cleaned === "") {                     // handle "typed nothing" before testing the pattern
        return "Full name is required.";
    }
    // ^ and $ clamp the WHOLE value; [A-Za-z ] allows letters/spaces; {3,} demands 3+ characters
    if (!/^[A-Za-z ]{3,}$/.test(cleaned)) {
        return "Name must be at least 3 letters (alphabets and spaces only).";
    }
    return "";                                // got here => the name passed
}

// (2) UID - the strict shape: 4 digits, then 2 letters, then 5 digits (e.g. 2025EB01187).
function ruleUid(text) {
    const cleaned = text.trim().toUpperCase(); // trim, and upper-case so "eb" counts the same as "EB"
    if (cleaned === "") {
        return "UID is required.";
    }
    // [0-9]{4} = four digits, [A-Z]{2} = two letters, [0-9]{5} = five digits, and nothing else
    if (!/^[0-9]{4}[A-Z]{2}[0-9]{5}$/.test(cleaned)) {
        return "UID must look like 2025EB01187 (4 digits, 2 letters, 5 digits).";
    }
    return "";
}

// (3) Email - roughly "text @ text . text", and no spaces anywhere.
function ruleMail(text) {
    const cleaned = text.trim();
    if (cleaned === "") {
        return "Email is required.";
    }
    // [^\s@]+ means "one or more characters that are NOT a space or an @", placed around the @ and the dot
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleaned)) {
        return "Please enter a valid email address.";
    }
    return "";
}

// (4) Phone - exactly ten digits (no +, no spaces, no dashes).
function ruleTel(text) {
    const cleaned = text.trim();
    if (cleaned === "") {
        return "Phone number is required.";
    }
    if (!/^[0-9]{10}$/.test(cleaned)) {       // {10} fixes the length at ten; the ^ and $ forbid anything extra
        return "Phone number must be exactly 10 digits.";
    }
    return "";
}

// (5) Date of birth - must be filled in, and must be a date in the past.
function ruleBorn(text) {
    if (text === "") {                        // the date picker reports "" when it is untouched
        return "Date of birth is required.";
    }
    const chosen = new Date(text);            // convert the "YYYY-MM-DD" string into a real Date object
    const rightNow = new Date();              // the current moment, to compare against
    if (chosen >= rightNow) {                 // you cannot be born today or in the future
        return "Date of birth must be in the past.";
    }
    return "";
}

/* A small UI helper that every check above leans on.
   Given a field's id and a message, it drops the message into that
   field's matching .aj-err box and flips the red ".aj-bad" look. */
function paintError(fieldId, message) {
    const box = document.getElementById(fieldId);            // the input/select itself
    const slot = document.getElementById("err-" + fieldId);  // its paired error <div> (same id, "err-" in front)
    slot.textContent = message;               // textContent (not innerHTML) keeps it safe from HTML injection
    if (message === "") {
        box.classList.remove("aj-bad");       // no message => remove the red styling
    } else {
        box.classList.add("aj-bad");          // a message => turn the control red
    }
}

/* =================================================================
   PART 2 :: THE STUDENT CLASS                            [3 marks]
   The class is a blueprint; "new Student(...)" presses out one
   object from it. I gave the object two helper methods so it can
   describe itself (its age, and a one-line summary).
   ================================================================= */

class Student {
    // the constructor runs once per "new Student(...)" and saves each argument onto the object
    constructor(fullName, uid, email, phone, dob, course) {
        this.fullName = fullName;             // "this" refers to the exact object being created right now
        this.uid = uid;
        this.email = email;
        this.phone = phone;
        this.dob = dob;                       // stored as the raw "YYYY-MM-DD" text
        this.course = course;
    }

    // method :: work out a whole-number age from the stored date of birth
    calcAge() {
        const born = new Date(this.dob);      // parse the stored date string
        const today = new Date();             // today
        let years = today.getFullYear() - born.getFullYear(); // rough answer: subtract the years
        const monthGap = today.getMonth() - born.getMonth();  // are we before or after the birthday month?
        // if this year's birthday hasn't happened yet, the rough answer is one too high, so step it back
        if (monthGap < 0 || (monthGap === 0 && today.getDate() < born.getDate())) {
            years--;
        }
        return years;
    }

    // method :: a neat single-line description (this exact string is what I log and store in the cookie)
    asLine() {
        // backtick template literal: ${...} drops each value straight into the sentence
        return `${this.fullName} (UID: ${this.uid}) | ${this.course} | Age: ${this.calcAge()}`;
    }
}

/* =================================================================
   PART 3 :: COOKIE HELPERS                               [2 marks]
   writeCookie saves a "name=value" that self-destructs after N days;
   readCookie fetches one back by name. I encode on the way in and
   decode on the way out so spaces and symbols survive (cookies choke
   on raw spaces).
   ================================================================= */

// save document.cookie = "name=value; expires=...; path=/"
function writeCookie(name, value, days) {
    const dies = new Date();                  // begin from the current moment...
    dies.setTime(dies.getTime() + days * 24 * 60 * 60 * 1000); // ...then add N days, converted into milliseconds
    document.cookie = name + "=" + encodeURIComponent(value) + // encode makes the value cookie-safe
                      ";expires=" + dies.toUTCString() +       // the browser auto-deletes it after this instant
                      ";path=/";                               // "/" keeps it readable across the whole site
}

// return one named cookie's value, or "" when that name isn't present
function readCookie(name) {
    const jar = document.cookie.split(";");   // the full cookie string, split into ["a=1", " b=2", ...]
    for (let i = 0; i < jar.length; i++) {    // walk each cookie in turn
        const pair = jar[i].trim().split("="); // trim the leading space, then split "name=value" into two halves
        if (pair[0] === name) {               // is this the one I'm after?
            return decodeURIComponent(pair[1]); // reverse the encoding writeCookie applied, and return it
        }
    }
    return "";                                // loop finished without a match => not found
}

/* =================================================================
   PART 4 :: WIRING EVERYTHING TOGETHER
   I delay all of this until DOMContentLoaded fires - if I ran it
   sooner, getElementById could hand back null because the form
   wouldn't have been built yet.
   ================================================================= */

document.addEventListener("DOMContentLoaded", function () {

    // on each visit, glance at the cookie so a returning student is greeted
    const remembered = readCookie("lastStudent");
    if (remembered !== "") {                  // only mention it if a cookie was actually there
        console.log("Retrieved previously saved student from cookie: " + remembered);
    }

    const theForm = document.getElementById("ajForm");

    // the whole page is driven by this one event: the form being submitted
    theForm.addEventListener("submit", function (event) {
        event.preventDefault();               // cancel the browser's default "reload the page and wipe it" action

        // grab the current text of each field
        const nameVal   = document.getElementById("ajName").value;
        const uidVal    = document.getElementById("ajUid").value;
        const mailVal   = document.getElementById("ajMail").value;
        const telVal    = document.getElementById("ajTel").value;
        const bornVal   = document.getElementById("ajBorn").value;
        const courseVal = document.getElementById("ajCourse").value;

        // run every check once; store each result under the matching field id
        const results = {
            ajName:   ruleName(nameVal),
            ajUid:    ruleUid(uidVal),
            ajMail:   ruleMail(mailVal),
            ajTel:    ruleTel(telVal),
            ajBorn:   ruleBorn(bornVal),
            // the dropdown isn't one of the five, but I still reject an empty choice
            ajCourse: courseVal === "" ? "Please select a course." : ""
        };

        // show (or clear) each message, and remember whether ANY field failed
        let everythingOk = true;              // start hopeful, flip to false on the first problem
        for (const id in results) {           // loop the keys: ajName, ajUid, ...
            paintError(id, results[id]);      // reflect this field's verdict on screen
            if (results[id] !== "") {         // a non-empty message means this field is bad
                everythingOk = false;
            }
        }

        // if anything failed, stop now - I will NOT build an object out of bad data
        if (!everythingOk) {
            console.log("Validation failed. Please correct the highlighted fields.");
            return;
        }

        // ---- all five passed: build the Student object from the clean values ----
        const student = new Student(nameVal, uidVal, mailVal, telVal, bornVal, courseVal);

        // print the object and the facts I derived from it, into the browser console
        console.log("=== New Student object created ===");
        console.log(student);                 // logging the raw object lets me expand its fields in DevTools
        console.log("Summary : " + student.asLine());
        console.log("Age     : " + student.calcAge() + " years");

        // ---- keep this student for 7 days inside a cookie ----
        writeCookie("lastStudent", student.asLine(), 7);
        console.log("Student saved to cookie: " + readCookie("lastStudent")); // read it straight back as proof it stuck

        // ---- finally, reveal the green banner with a tidy, readable summary ----
        const panel = document.getElementById("ajResult");
        panel.style.display = "block";        // switch it from hidden to visible
        // each "\n" turns into a real line break because the CSS set white-space: pre-line on .aj-out
        panel.textContent =
            "ID Card generated successfully!\n" +
            "Name   : " + student.fullName + "\n" +
            "UID    : " + student.uid + "\n" +
            "Email  : " + student.email + "\n" +
            "Phone  : " + student.phone + "\n" +
            "DOB    : " + student.dob + "\n" +
            "Course : " + student.course + "\n" +
            "Age    : " + student.calcAge() + " years\n" +
            "(Details also logged to the console and saved in a cookie.)";
    });
});
