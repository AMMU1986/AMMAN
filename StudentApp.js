/*
  =====================================================================
  QUESTION 2  ::  STUDENT ID CARD APPLICATION  ::  THE LOGIC
  ---------------------------------------------------------------------
  Author : AMMAN JAKHAR  |  UID : 2025EB01187  |  DOB : 29.08.1986
  ---------------------------------------------------------------------
  This one file contains the three graded pieces:
      PART 1  - five independent field validators        [5 marks]
      PART 2  - a Student class + an object I console.log [3 marks]
      PART 3  - cookie write + read helpers              [2 marks]
      PART 4  - the glue: wait for load, listen for the submit,
                and run the parts above in order.

  Convention used by every validator below: it RETURNS a string.
  An empty string "" means the field is valid; any other text is the
  exact message to display. Returning (rather than firing an alert)
  keeps each check self-contained and reusable.

  Naming is mine throughout: ids are ajName / ajUid / ..., and the
  helpers are ruleXxx / paintError / writeCookie / readCookie.
  =====================================================================
*/

"use strict"; // strict mode turns quiet mistakes into visible errors

/* =================================================================
   PART 1  ::  THE FIVE FIELD VALIDATORS                  [5 marks]
   Each one trims first, so a box of only spaces counts as empty.
   ================================================================= */

// (1) Full name - letters and spaces only, three or more characters.
function ruleName(text) {
  const cleaned = text.trim();                 // strip leading/trailing spaces
  if (cleaned === "") {                         // reject "nothing typed" first
    return "Full name is required.";
  }
  // ^...$ anchors the whole value; [A-Za-z ] = letters/spaces; {3,} = 3 or more
  if (!/^[A-Za-z ]{3,}$/.test(cleaned)) {
    return "Name must be at least 3 letters (alphabets and spaces only).";
  }
  return "";                                     // reached here => valid
}

// (2) UID - 4 digits, 2 letters, 5 digits, e.g. 2025EB01187.
function ruleUid(text) {
  const cleaned = text.trim().toUpperCase();     // upper-case so "eb" == "EB"
  if (cleaned === "") {
    return "UID is required.";
  }
  if (!/^[0-9]{4}[A-Z]{2}[0-9]{5}$/.test(cleaned)) {
    return "UID must look like 2025EB01187 (4 digits, 2 letters, 5 digits).";
  }
  return "";
}

// (3) Email - broadly "text @ text . text" with no spaces.
function ruleMail(text) {
  const cleaned = text.trim();
  if (cleaned === "") {
    return "Email is required.";
  }
  // [^\s@]+ = one or more chars that are neither a space nor an @
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleaned)) {
    return "Please enter a valid email address.";
  }
  return "";
}

// (4) Phone - exactly ten digits, nothing else.
function ruleTel(text) {
  const cleaned = text.trim();
  if (cleaned === "") {
    return "Phone number is required.";
  }
  if (!/^[0-9]{10}$/.test(cleaned)) {            // {10} fixes the length at ten
    return "Phone number must be exactly 10 digits.";
  }
  return "";
}

// (5) Date of birth - required, and must be a date already in the past.
function ruleBorn(text) {
  if (text === "") {                             // the picker returns "" when untouched
    return "Date of birth is required.";
  }
  const chosen = new Date(text);                 // parse the YYYY-MM-DD string
  const rightNow = new Date();                   // the current moment
  if (chosen >= rightNow) {                       // cannot be born today or later
    return "Date of birth must be in the past.";
  }
  return "";
}

/* A small UI helper used by the submit handler. It writes a message
   into a field's matching .aj-err box and toggles the red "aj-bad" look. */
function paintError(fieldId, message) {
  const box  = document.getElementById(fieldId);          // the input/select
  const slot = document.getElementById("err-" + fieldId); // its paired error <div>
  slot.textContent = message;                             // textContent avoids HTML injection
  if (message === "") {
    box.classList.remove("aj-bad");                       // valid => clear the red style
  } else {
    box.classList.add("aj-bad");                          // invalid => turn it red
  }
}

/* =================================================================
   PART 2  ::  THE STUDENT CLASS                          [3 marks]
   The class is a blueprint; "new Student(...)" stamps out one object.
   It carries two helper methods so an instance can describe itself.
   ================================================================= */
class Student {
  constructor(fullName, uid, email, phone, dob, course) {
    this.fullName = fullName;   // "this" is the specific object being built
    this.uid      = uid;
    this.email    = email;
    this.phone    = phone;
    this.dob      = dob;        // kept as the raw YYYY-MM-DD text
    this.course   = course;
  }

  // Derive a whole-number age from the stored date of birth.
  calcAge() {
    const born  = new Date(this.dob);
    const today = new Date();
    let years = today.getFullYear() - born.getFullYear();   // rough difference
    const monthGap = today.getMonth() - born.getMonth();    // before/after birthday month?
    // if this year's birthday has not occurred yet, the rough figure is one too high
    if (monthGap < 0 || (monthGap === 0 && today.getDate() < born.getDate())) {
      years--;
    }
    return years;
  }

  // A tidy one-line description (this exact string is what I log and store).
  asLine() {
    return `${this.fullName} (UID: ${this.uid}) | ${this.course} | Age: ${this.calcAge()}`;
  }
}

/* =================================================================
   PART 3  ::  COOKIE HELPERS                             [2 marks]
   writeCookie stores "name=value" that expires after N days;
   readCookie fetches one back by name. Values are URI-encoded on the
   way in and decoded on the way out so spaces/symbols survive.
   ================================================================= */

function writeCookie(name, value, days) {
  const dies = new Date();
  dies.setTime(dies.getTime() + days * 24 * 60 * 60 * 1000); // add N days in ms
  document.cookie =
    name + "=" + encodeURIComponent(value) +   // encode so the value is cookie-safe
    ";expires=" + dies.toUTCString() +         // the browser deletes it after this instant
    ";path=/";                                  // readable across the whole site
}

function readCookie(name) {
  const jar = document.cookie.split(";");       // ["a=1", " b=2", ...]
  for (let i = 0; i < jar.length; i++) {
    const pair = jar[i].trim().split("=");      // trim the leading space, split on "="
    if (pair[0] === name) {
      return decodeURIComponent(pair[1]);       // undo the encoding and return it
    }
  }
  return "";                                     // not found
}

/* =================================================================
   PART 4  ::  WIRING IT ALL TOGETHER
   Everything waits for DOMContentLoaded; running earlier could make
   getElementById return null before the form exists.
   ================================================================= */
document.addEventListener("DOMContentLoaded", function () {

  // On each visit, peek at the cookie so a returning student can be greeted.
  const remembered = readCookie("lastStudent");
  if (remembered !== "") {
    console.log("Retrieved previously saved student from cookie: " + remembered);
  }

  const theForm = document.getElementById("ajForm");

  theForm.addEventListener("submit", function (event) {
    event.preventDefault(); // stop the default page reload that would wipe the form

    // read the current value of every field
    const nameVal   = document.getElementById("ajName").value;
    const uidVal    = document.getElementById("ajUid").value;
    const mailVal   = document.getElementById("ajMail").value;
    const telVal    = document.getElementById("ajTel").value;
    const bornVal   = document.getElementById("ajBorn").value;
    const courseVal = document.getElementById("ajCourse").value;

    // run each validator once; key every result by its field id
    const results = {
      ajName:   ruleName(nameVal),
      ajUid:    ruleUid(uidVal),
      ajMail:   ruleMail(mailVal),
      ajTel:    ruleTel(telVal),
      ajBorn:   ruleBorn(bornVal),
      // the dropdown is not one of the five, but an empty choice is still rejected
      ajCourse: courseVal === "" ? "Please select a course." : ""
    };

    // reflect each verdict on screen and note whether anything failed
    let everythingOk = true;
    for (const id in results) {
      paintError(id, results[id]);
      if (results[id] !== "") {
        everythingOk = false;
      }
    }

    // if any field failed, stop - I will not build an object from bad data
    if (!everythingOk) {
      console.log("Validation failed. Please correct the highlighted fields.");
      return;
    }

    // ---- all five passed: build the Student object from the clean values ----
    const student = new Student(nameVal, uidVal, mailVal, telVal, bornVal, courseVal);

    console.log("=== New Student object created ===");
    console.log(student);                                   // expandable in DevTools
    console.log("Summary : " + student.asLine());
    console.log("Age     : " + student.calcAge() + " years");

    // ---- remember this student for 7 days in a cookie ----
    writeCookie("lastStudent", student.asLine(), 7);
    console.log("Student saved to cookie: " + readCookie("lastStudent")); // read back as proof

    // ---- reveal the green banner with a readable summary ----
    const panel = document.getElementById("ajResult");
    panel.style.display = "block";
    // each "\n" becomes a real line break because .aj-out sets white-space: pre-line
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
