/* ===========================================================================
   Web Development :: Graded Assignment (Weeks 1-6)  -  Question 2
   Field checks (onfocusout), an Applicant class, and cookie save/load.
   AMMAN JAKHAR  |  UID 2025eb01187

   Design notes:
     - Each checker returns true/false and writes a message beneath its field.
     - Name is tested character by character (letters + spaces only).
     - DOB is split on "/" and validated piece by piece, then age is derived.
     - Cookies use the max-age attribute and are read with Array.find().
   =========================================================================== */

"use strict";

/* tiny helpers ------------------------------------------------------------- */
const el = (id) => document.getElementById(id);

// write (or clear) the red note under a field; returns true when there is no error
function note(field, text) {
  el(field + "Error").textContent = text || "";
  return !text;
}

/* 1. NAME :: letters and spaces only, not empty --------------------------- */
function checkName() {
  const value = el("name").value.trim();
  if (value.length === 0) {
    return note("name", "Please enter your name.");
  }
  for (const ch of value) {
    const letter = (ch >= "a" && ch <= "z") || (ch >= "A" && ch <= "Z");
    if (!letter && ch !== " ") {
      return note("name", "Name may contain letters and spaces only.");
    }
  }
  return note("name", "");
}

/* 2. DOB :: strict dd/mm/yyyy, not empty; also fills the age box ----------- */
function checkDob() {
  const value = el("dob").value.trim();
  el("age").value = "";                       // reset age until DOB is valid

  if (value.length === 0) {
    return note("dob", "Please enter your date of birth.");
  }

  const parts = value.split("/");
  const shaped =
    parts.length === 3 &&
    parts[0].length === 2 &&
    parts[1].length === 2 &&
    parts[2].length === 4 &&
    parts.every((p) => /^[0-9]+$/.test(p));

  if (!shaped) {
    return note("dob", "Use the dd/mm/yyyy format, e.g. 29/08/1986.");
  }

  const day = Number(parts[0]);
  const month = Number(parts[1]);
  const year = Number(parts[2]);
  if (day < 1 || day > 31 || month < 1 || month > 12) {
    return note("dob", "That is not a valid calendar date.");
  }

  el("age").value = ageFrom(day, month, year);
  return note("dob", "");
}

/* AGE :: whole years between the DOB and today ---------------------------- */
function ageFrom(day, month, year) {
  const today = new Date();
  let years = today.getFullYear() - year;

  // step back a year if this year's birthday has not arrived yet
  const todayMonth = today.getMonth() + 1;
  const beforeBirthday =
    todayMonth < month || (todayMonth === month && today.getDate() < day);
  if (beforeBirthday) {
    years -= 1;
  }
  return years >= 0 ? years : "";
}

/* 3. MOBILE :: digits only, not empty, no leading zero -------------------- */
function checkMobile() {
  const box = el("mobile");
  const value = box.value.trim();

  const allDigits = value.length > 0 && [...value].every((c) => c >= "0" && c <= "9");
  if (!allDigits || value.charAt(0) === "0") {
    box.value = "";                           // rule: wipe the bad input
    return note("mobile", "Enter digits only; not blank and not starting with 0.");
  }
  return note("mobile", "");
}

/* 4. EMAIL :: has "@" (not first char) and ends in .com or .in ------------ */
function checkEmail() {
  const box = el("email");
  const value = box.value.trim();

  const atPos = value.indexOf("@");
  const goodTail = value.endsWith(".com") || value.endsWith(".in");
  if (atPos < 1 || !goodTail) {
    box.value = "";                           // rule: wipe the bad input
    return note("email", 'Needs "@" (not at the start) and must end with .com or .in.');
  }
  return note("email", "");
}

/* -------------------------------------------------------------------------
   Applicant :: one object that carries the whole form
   ------------------------------------------------------------------------- */
class Applicant {
  constructor(name, dob, age, mobile, email) {
    this.name = name;
    this.dob = dob;
    this.age = age;
    this.mobile = mobile;
    this.email = email;
  }

  // single-line summary, handy for the console
  summary() {
    return [this.name, this.dob, "age " + this.age, this.mobile, this.email].join(" | ");
  }
}

/* -------------------------------------------------------------------------
   Cookie save / load  (max-age style; read via find())
   ------------------------------------------------------------------------- */
function saveCookie(key, value, days) {
  const seconds = days * 24 * 60 * 60;
  document.cookie =
    key + "=" + encodeURIComponent(value) + "; max-age=" + seconds + "; path=/";
}

function loadCookie(key) {
  const prefix = key + "=";
  const jar = document.cookie ? document.cookie.split("; ") : [];
  const row = jar.find((item) => item.indexOf(prefix) === 0);
  return row ? decodeURIComponent(row.slice(prefix.length)) : null;
}

/* -------------------------------------------------------------------------
   Submit :: validate everything, build + log the object, store the cookie
   ------------------------------------------------------------------------- */
function onSubmit(event) {
  event.preventDefault();

  // run all four checks (keep them all so every message shows)
  const passed = [checkName(), checkDob(), checkMobile(), checkEmail()];
  if (passed.some((ok) => ok === false)) {
    alert("Please fix the fields marked in red, then submit again.");
    return false;
  }

  const applicant = new Applicant(
    el("name").value.trim(),
    el("dob").value.trim(),
    el("age").value.trim(),
    el("mobile").value.trim(),
    el("email").value.trim()
  );

  // requirement: show the object in the console
  console.log("Applicant created ->", applicant);
  console.log("Applicant summary ->", applicant.summary());

  // keep the record in a cookie for a week
  saveCookie("applicant", JSON.stringify(applicant), 7);

  // move to the retrieve panel
  el("formPage").style.display = "none";
  el("retrievePage").style.display = "block";
  return false;
}

/* -------------------------------------------------------------------------
   Retrieve :: match the typed mobile against the cookie and alert the data
   ------------------------------------------------------------------------- */
function onRetrieve() {
  const typed = el("retrieveMobile").value.trim();
  const stored = loadCookie("applicant");

  if (!stored) {
    alert("No application is stored in the cookie yet.");
    return;
  }

  const data = JSON.parse(stored);
  if (typed === data.mobile) {
    alert(
      "Details fetched from the cookie\n\n" +
      "Name   : " + data.name + "\n" +
      "DOB    : " + data.dob + "\n" +
      "Age    : " + data.age + "\n" +
      "Mobile : " + data.mobile + "\n" +
      "Email  : " + data.email
    );
  } else {
    alert("No stored record matches the mobile number " + typed + ".");
  }
}
