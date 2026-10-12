/* =====================================================================
   Graded Assignment (Weeks 1-6) - Question 2
   JavaScript validation, Student class, and cookie handling
   Student ID: STU2024001
   =====================================================================
   Contents:
     1. Field validation functions (fire on the "onfocusout" event)
     2. Student class used to build an object from the form fields
     3. Cookie store (on submit) and cookie retrieve (on button click)
   ===================================================================== */


/* =====================================================================
   1. VALIDATION FUNCTIONS
   Each function returns true/false and shows an inline error message.
   ===================================================================== */

/* ---- Name: only alphabets and spaces, must not be blank ---- */
function validateName() {
    const field = document.getElementById("name");
    const error = document.getElementById("nameError");
    const value = field.value.trim();

    // Regular expression: one or more letters/spaces only
    const namePattern = /^[A-Za-z ]+$/;

    if (value === "") {
        error.textContent = "Name cannot be blank.";
        return false;
    }
    if (!namePattern.test(value)) {
        error.textContent = "Name must contain only alphabets and spaces.";
        return false;
    }

    error.textContent = "";
    return true;
}

/* ---- Date of Birth: must be in dd/mm/yyyy format, not blank ---- */
function validateDob() {
    const field = document.getElementById("dob");
    const error = document.getElementById("dobError");
    const value = field.value.trim();

    // dd/mm/yyyy : 2 digits / 2 digits / 4 digits
    const dobPattern = /^(\d{2})\/(\d{2})\/(\d{4})$/;

    if (value === "") {
        error.textContent = "Date of birth cannot be blank.";
        document.getElementById("age").value = "";
        return false;
    }

    const match = value.match(dobPattern);
    if (!match) {
        error.textContent = "Date of birth must be in dd/mm/yyyy format.";
        document.getElementById("age").value = "";
        return false;
    }

    // Basic range check on day and month
    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10);
    if (day < 1 || day > 31 || month < 1 || month > 12) {
        error.textContent = "Please enter a valid day and month.";
        document.getElementById("age").value = "";
        return false;
    }

    error.textContent = "";
    // Once the date is valid, calculate the age automatically
    calculateAge(match);
    return true;
}

/* ---- Age: calculated from the date of birth (read-only field) ---- */
function calculateAge(match) {
    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10);
    const year = parseInt(match[3], 10);

    const birthDate = new Date(year, month - 1, day);
    const today = new Date();

    let age = today.getFullYear() - birthDate.getFullYear();

    // Adjust if the birthday has not occurred yet this year
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }

    document.getElementById("age").value = age >= 0 ? age : "";
}

/* ---- Mobile: digits [0-9] only, not blank, cannot start with 0 ---- */
function validateMobile() {
    const field = document.getElementById("mobile");
    const error = document.getElementById("mobileError");
    const value = field.value.trim();

    // First digit 1-9, followed by any digits
    const mobilePattern = /^[1-9][0-9]*$/;

    if (value === "" || !mobilePattern.test(value)) {
        error.textContent =
            "Mobile must be digits only, not blank, and cannot start with 0.";
        field.value = "";          // Rule: clear the field on error
        return false;
    }

    error.textContent = "";
    return true;
}

/* ---- Email: must contain "@", not begin with "@", end with .com/.in ---- */
function validateEmail() {
    const field = document.getElementById("email");
    const error = document.getElementById("emailError");
    const value = field.value.trim();

    const hasAt = value.includes("@");
    const startsWithAt = value.startsWith("@");
    const endsCorrectly = value.endsWith(".com") || value.endsWith(".in");

    if (!hasAt || startsWithAt || !endsCorrectly) {
        error.textContent =
            'Email must contain "@", not start with "@", and end with ".com" or ".in".';
        field.value = "";          // Rule: clear the field on error
        return false;
    }

    error.textContent = "";
    return true;
}


/* =====================================================================
   2. STUDENT CLASS
   Used to bundle all form fields into a single object.
   ===================================================================== */
class Student {
    constructor(name, dob, age, mobile, email) {
        this.name = name;
        this.dob = dob;
        this.age = age;
        this.mobile = mobile;
        this.email = email;
    }

    // Convert the student object into a string for cookie storage
    toCookieString() {
        return JSON.stringify(this);
    }
}


/* =====================================================================
   3. COOKIE HELPERS
   ===================================================================== */

/* Store a cookie with a given name, value and lifetime (in days) */
function setCookie(cookieName, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    const expires = "expires=" + date.toUTCString();
    // encodeURIComponent keeps the JSON safe inside the cookie
    document.cookie =
        cookieName + "=" + encodeURIComponent(value) + ";" + expires + ";path=/";
}

/* Read a cookie by name; returns the decoded value or null */
function getCookie(cookieName) {
    const target = cookieName + "=";
    const parts = document.cookie.split(";");
    for (let part of parts) {
        part = part.trim();
        if (part.indexOf(target) === 0) {
            return decodeURIComponent(part.substring(target.length));
        }
    }
    return null;
}


/* =====================================================================
   FORM SUBMISSION
   Validate everything, build the Student object, store it in a cookie,
   log it to the console, and move to the retrieve page.
   ===================================================================== */
function submitForm(event) {
    event.preventDefault();   // stop the page from reloading

    // Run every validation; all must pass
    const valid =
        validateName() &
        validateDob() &
        validateMobile() &
        validateEmail();

    if (!valid) {
        alert("Please correct the highlighted fields before submitting.");
        return false;
    }

    // Build the object from the form using the Student class
    const student = new Student(
        document.getElementById("name").value.trim(),
        document.getElementById("dob").value.trim(),
        document.getElementById("age").value.trim(),
        document.getElementById("mobile").value.trim(),
        document.getElementById("email").value.trim()
    );

    // Requirement: display the object details in the console log
    console.log("Student object created:", student);

    // Store the object (as JSON) inside a cookie for 7 days.
    // The mobile number is also stored separately as the lookup key.
    setCookie("studentData", student.toCookieString(), 7);
    setCookie("studentMobile", student.mobile, 7);

    // "Navigate" to the next page by swapping the visible sections
    document.getElementById("formPage").classList.add("hidden");
    document.getElementById("retrievePage").classList.remove("hidden");

    return false;
}


/* =====================================================================
   RETRIEVE DETAILS FROM COOKIE
   The user types a mobile number; if it matches the stored one,
   the saved student details are shown in an alert.
   ===================================================================== */
function retrieveCookie() {
    const enteredMobile = document.getElementById("retrieveMobile").value.trim();
    const storedData = getCookie("studentData");

    if (!storedData) {
        alert("No student record was found in the cookie.");
        return;
    }

    const student = JSON.parse(storedData);

    if (enteredMobile === student.mobile) {
        const message =
            "Student Details Retrieved from Cookie:\n\n" +
            "Name   : " + student.name + "\n" +
            "DOB    : " + student.dob + "\n" +
            "Age    : " + student.age + "\n" +
            "Mobile : " + student.mobile + "\n" +
            "Email  : " + student.email;
        alert(message);
    } else {
        alert("No matching record found for mobile number: " + enteredMobile);
    }
}
