/* pip-strip.js — tapped certification level for the five-pip protocol strip.
 *
 * The markup is server-rendered in its "Show all" state by
 * scripts/mkdocs_pip_strip.py, so the page is complete and legible with
 * JavaScript off. This file only re-paints the same rows for a tapped level:
 * it never invents a level and never edits an action.
 *
 * State lives in data-states on each <tr> ("go,call,no,..."), which the hook
 * derived from the row's own level chip. Nothing here re-derives it.
 */
(function () {
  "use strict";

  var LETTER = ["R", "B", "A", "I", "P"];

  function tagFor(states) {
    var i;
    var allCall = states.every(function (s) { return s === "call"; });
    if (allCall) return ["call", "MC at every level"];
    var m = -1;
    for (i = 0; i < states.length; i++) { if (states[i] !== "no") { m = i; break; } }
    if (m < 0) return ["no", "no level authorised"];
    if (states[m] === "call") {
      var above = -1;
      for (i = m + 1; i < states.length; i++) { if (states[i] === "go") { above = i; break; } }
      return ["call", "MC at " + LETTER[m] + (above < 0 ? "" : ", standing from " + LETTER[above])];
    }
    return ["go", "standing from " + LETTER[m]];
  }

  function paint(block, level) {
    var rows = block.querySelectorAll("tr[data-states]");
    var go = 0, call = 0, no = 0, unv = 0;
    var n = 0;

    Array.prototype.forEach.call(rows, function (tr) {
      n++;
      var states = tr.getAttribute("data-states").split(",");
      var flagged = tr.hasAttribute("data-unverified");
      var tag = tr.querySelector(".pip-tag");
      var got;

      tr.classList.remove("pip-hit", "pip-hitcall", "pip-hitno", "pip-dim");

      if (flagged) {
        /* OWNER_REQUIRED: the page publishes a level the source does not
         * authorise. Never counted as standing or as permitted — it is its
         * own bucket so the tally stays true. */
        unv++;
        if (tag) { tag.className = "pip-tag flag"; tag.textContent = "level unverified \u2691"; }
        return;
      }

      if (level === "all") {
        got = tagFor(states);
      } else {
        var st = states[LETTER.indexOf(level)];
        got = st === "go" ? ["go", "standing"]
            : st === "call" ? ["call", "call MC"]
            : ["no", "not permitted"];
      }
      if (tag) { tag.className = "pip-tag " + got[0]; tag.textContent = got[1]; }

      if (level === "all") return;

      var st2 = states[LETTER.indexOf(level)];
      if (st2 === "go") { go++; tr.classList.add("pip-hit"); }
      else if (st2 === "call") { call++; tr.classList.add("pip-hitcall"); }
      else { no++; tr.classList.add("pip-dim", "pip-hitno"); }
    });

    var tally = block.querySelector(".pip-tally");
    if (tally) {
      if (level === "all") {
        tally.innerHTML = "Show all \u2014 " + n + " actions. Each row names the level its " +
          "action starts at; tap a level to see this protocol as you." +
          (unv ? " \u00b7 " + unv + " level unverified \u2691" : "");
      } else {
        tally.innerHTML = "<b>" + level + "</b>: of " + n + " actions on this protocol \u2014 " +
          "<b>" + go + "</b> standing, <b>" + call + "</b> need Medical Control, <b>" + no +
          "</b> not permitted (dimmed)." +
          (unv ? " <b>" + unv + "</b> level unverified \u2691." : "");
      }
    }

    Array.prototype.forEach.call(block.querySelectorAll(".pip-btn"), function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-level") === level ? "true" : "false");
    });
  }

  function init(block) {
    var pick = block.querySelector(".pip-pick");
    if (!pick) return;
    pick.addEventListener("click", function (ev) {
      var b = ev.target.closest("button");
      if (!b) return;
      paint(block, b.getAttribute("data-level"));
    });
    /* The default state must be painted on load, not only after a tap. */
    paint(block, "all");
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-pip-block]"), init);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
