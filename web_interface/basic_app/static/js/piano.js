const note = [
  "C3",
  "Db3",
  "D3",
  "Eb3",
  "E3",
  "F3",
  "Gb3",
  "G3",
  "Ab3",
  "A3",
  "Bb3",
  "B3",
  "C4",
  "Db4",
  "D4",
  "Eb4",
  "E4",
  "F4",
  "Gb4",
  "G4",
  "Ab4",
  "A4",
  "Bb4",
  "B4",
  "C5",
  "Db5",
  "D5",
  "Eb5",
  "E5",
  "F5",
  "Gb5",
  "G5",
  "Ab5",
  "A5",
  "Bb5",
  "B5",
  "C6",
  "Db6",
  "D6",
  "Eb6",
  "E6",
  "F6",
  "Gb6",
  "G6",
  "Ab6",
  "A6",
  "Bb6",
  "B6",
];

const keys = document.querySelectorAll(".key");
const notes = document.querySelectorAll(".id"); //returns numbers co# = 1 ......

function playSound(newUrl) {
  new Audio(newUrl).play();
}

var allnote = new Set();



function keypressed(newUrl, notes, i) {
  // console.log(`Note played: ${note[notes]}`);
  keys[i].classList.add("played");
  playSound(newUrl);
  setTimeout(() => {
    keys[i].classList.remove("played");
  }, 100);

  
}

const order = [
  "z",
  "1",
  "x",
  "2",
  "c",
  "v",
  "3",
  "b",
  "4",
  "n",
  "5",
  "m",
  ",",
  "6",
  ".",
  "7",
  "q",
  "w",
  "8",
  "e",
  "9",
  "r",
  "/",
  "t",
  "y",
  ";",
  "u",
  "'",
  "i",
  "o",
  "[",
  "p",
  "]",
  "a",
  "0",
  "s",
  "d",
  "-",
  "f",
  "=",
  "g",
  "h",
  "@",
  "j",
  " ",
  "k",
  "`",
  "l",
];
let pressed_keys = new Set();
let pressed_keys2 = [];
function clear_set() {}
let counter = 0;
let startTime = null;



document.addEventListener("keypress", (event) => {
  pressed_keys.add(event.key);

  if (startTime === null) {
    startTime = Date.now();
    console.log("Timer started." + startTime);
    var note_duration = document.getElementById("Duration");
    note_duration.innerHTML = "0 s";
  } 
  else {
    if(((Date.now() - startTime) /1000) >=4){
      startTime = Date.now();
      console.log("Timer started." + startTime);
      var note_duration = document.getElementById("Duration");
      note_duration.innerHTML = "0 s";
    }
    else{

      let elapsedSeconds = (Date.now() - startTime) /1000;
      console.log(`Key pressed after ${elapsedSeconds.toFixed(2)} seconds.`);
      
      var note_duration = document.getElementById("Duration");
      note_duration.innerHTML = elapsedSeconds;
      startTime = Date.now();
    }
  
     
  }
  
  setTimeout(() => {
    pressed_keys.clear();
    allnote.clear();
  }, 100);

  if (pressed_keys.size === 1) {
    // console.log("note detected");

    order.forEach((odr) => {
      if (event.key === `${odr}`) {
        const newUrl = "media/piano-mp3/" + `${note[order.indexOf(odr)]}` + ".mp3";
        keypressed(newUrl, order.indexOf(odr), order.indexOf(odr));

        // var note_played = document.getElementById("sequence");
        // note_played.innerHTML = note[order.indexOf(odr)];
        allnote.add(note[order.indexOf(odr)]);

        let notestr = "";
        for (const x of allnote.values()) {
          notestr += x + " ";
        }
        var note_played = document.getElementById("piano_sequence");
        note_played.innerHTML = notestr;
      }
    });
  } else {
    // console.log("chord detected");

    // for (each_key in pressed_keys){

    order.forEach((odr) => {
      if (event.key === `${odr}`) {
        const newUrl = "media/piano-mp3/" + `${note[order.indexOf(odr)]}` + ".mp3";
        keypressed(newUrl, order.indexOf(odr), order.indexOf(odr));

        allnote.add(note[order.indexOf(odr)]);

        let notestr = "";
        for (const x of allnote.values()) {
          notestr += x + " ";
        }
        var note_played = document.getElementById("piano_sequence");
        note_played.innerHTML = notestr;

              }
            });
            // }
          }
         if(counter === 2) counter = 1;
});


keys.forEach((key, notes) => {
  const number = notes < 9 ? "0" + (notes + 1) : notes + 1;
  const newUrl = "24-piano-keys/key" + number + ".mp3";
  key.addEventListener("click", () => {
    // console.log(`Note played: ${note[notes]}`);
    key.classList.add("played");
    playSound(newUrl);
    setTimeout(() => {
      key.classList.remove("played");
    }, 100);
  });
});


