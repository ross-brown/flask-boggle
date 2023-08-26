"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");
const $currentScore = $("#current-score");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  const $tBody = $("<tbody>");

  for (let row of board) {

    const $tr = $("<tr>");
    for (let letter of row) {

      $tr.append($("<td>").text(letter));
    }
    $tBody.append($tr);
  }
  $table.append($tBody);
}



function addWordToList(word, score) {
  $playedWords.append($("<li>", { text: word.toUpperCase() }));

  let currentScore = Number($currentScore.text());

  currentScore += score;

  $currentScore.text(currentScore);

}

function displayMessage(result) {
  if (result === 'not-word') {
    $message.text("That word does not exist").addClass("err");
  } else if (result === 'not-on-board') {
    $message.text("That word is not on the board").addClass("err");
  } else if (result === 'duplicate') {
    $message.text("You've already played that word.").addClass("err");
  } else {
    $message.text("Valid word!").removeClass("err").addClass("ok");
  }
}


async function handleSumbit(evt) {
  evt.preventDefault();

  const word = $wordInput.val();

  const response = await fetch("/api/score-word", {
    method: "POST",
    body: JSON.stringify({ word, gameId }),
    headers: {
      "Content-Type": "application/json"
    }
  });

  const { result, score } = await response.json();

  if (result === 'ok') addWordToList(word, score);

  displayMessage(result);

  $wordInput.val("");
}

$form.on("submit", handleSumbit);


start();
