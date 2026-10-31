// Pure matching logic, no DOM. Works in browser and Node (for tests).
(function (root) {
  function norm(s) { return (s || "").toLowerCase().replace(/[’]/g, "'"); }
  function words(s) { return norm(s).split(/[^a-z0-9']+/).filter(Boolean); }

  function isCrisis(q, keys) {
    var n = norm(q);
    return keys.some(function (k) { return n.indexOf(k) !== -1; });
  }

  // Score = phrase hits (weighted by length) + whole-word hits. Short keys like "pr" or "do"
  // only count as whole words so "product" can't trigger "pr".
  function score(q, entry) {
    var n = " " + norm(q).replace(/[^a-z0-9' ]+/g, " ") + " ";
    var s = 0;
    entry.keys.forEach(function (k) {
      var kk = norm(k);
      if (kk.indexOf(" ") !== -1 || kk.length > 4) {
        if (n.indexOf(kk) !== -1) s += 2 + kk.split(" ").length;
      } else if (n.indexOf(" " + kk + " ") !== -1) {
        s += 1;
      }
    });
    return s;
  }

  function answer(q, kb, crisisKeys) {
    if (isCrisis(q, crisisKeys)) return { crisis: true };
    var best = null, bestScore = 0;
    kb.forEach(function (e) {
      var sc = score(q, e);
      if (sc > bestScore) { best = e; bestScore = sc; }
    });
    return best ? { entry: best, score: bestScore } : { entry: null };
  }

  var api = { answer: answer, score: score, isCrisis: isCrisis, words: words };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.Engine = api;
})(typeof window !== "undefined" ? window : globalThis);
