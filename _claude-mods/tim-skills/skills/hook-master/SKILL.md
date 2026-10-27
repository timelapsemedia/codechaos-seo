---
name: hook-master
description: "Fix the first seconds of a Short, Reel or TikTok: diagnose why viewers swipe, rewrite the hook in six formats, match it to the footage, write the payoff. No fake stats. Auch: Hook verbessern, Einstieg kritisieren."
---

# Hook Master

Use this when someone wants a better hook, opening line, first three seconds, scroll stopper or intro for a Reel, TikTok, Short or short ad, or says people swipe away early. It runs the whole job and calls eight smaller skills by name.

Your job: make this video's opening clearer and more wanted for the people it is for, using only what the footage and the creator can back up. Then hand back exact words to say, exact on-screen text, the first shot, and the next few seconds. You are not promising views.

## The suite

All eight stages live in this skill's `stages/` folder (upstream they were eight separate skills; here they are one skill to keep the always-on cost low). Read a stage file only when you reach that stage.

| Stage | File | What it settles |
|---|---|---|
| 1 | [stages/four-failures-check.md](stages/four-failures-check.md) (+ failure-examples.md) | Which of the four failures (delay, confusion, irrelevance, disinterest) the current opening commits, pointing at the exact words and shot |
| 2 | [stages/viewer-panel.md](stages/viewer-panel.md) | Six viewers watch the first 3 seconds. Each says swipe or stay, and why |
| 3 | [stages/the-council.md](stages/the-council.md) | The panel's verdicts turned into the top 3 changes, ranked |
| 4 | [stages/hook-formats.md](stages/hook-formats.md) (+ format-bank.md) | The idea rewritten in six formats, each built on a real contrast |
| 5 | [stages/niche-tuner.md](stages/niche-tuner.md) | Words, proof and stakes tuned to this niche and this viewer |
| 6 | [stages/visual-match.md](stages/visual-match.md) | The first-second visual, the on-screen text and the spoken words all say the same thing |
| 7 | [stages/lock-in.md](stages/lock-in.md) (+ dead-stretches.md) | The next 1 to 3 sentences pay the hook off, so attention turns into trust |
| any | [stages/viral-scout.md](stages/viral-scout.md) (+ pattern-sheet.md) | Patterns from real examples. Without web access it asks the user to paste examples. It never invents what is "trending" |

**How to use them.** When the text below names a stage (for example `four-failures-check`), read `stages/<name>.md` in this skill folder. If a file can't be found, the rules in this file are enough; never stop because a stage file is missing.

## Tims Regeln (gehen vor)

- **Social Media Rules 2026** (`C:/Users/moonc/Downloads/Social Media Rules 2026.md`, vor dem Schnitt lesen): Der Hook sitzt in den ersten **1,5 s** und ist **dreischichtig**: gesprochen + Bild + Text gleichzeitig. Dazu Re-Hooks alle 10 bis 15 s, Payoff, dann CTA/Loop in den letzten 3 bis 5 s, Safe Zones, Captions 4 bis 7 Wörter. Wo diese Datei „first 3 seconds“ sagt, gilt für Tims Kanäle das 1,5-s-Fenster.
- **DRUWIDS und Mitragyna Forschungsarchiv: Gate vor jedem Hook.** Erst Skill `druwids-social-operator` laden (DRUWIDS) bzw. das Compliance-Gate der Routine „Mitragyna Archiv – Betrieb“ beachten. Kein Hook, kein Text und keine Variante mit Aussagen oder Andeutungen zu Einnahme, Konsum, Wirkung, Dosierung oder Zubereitung. Der gesprochene Text des fertigen Clips muss durch `python E:/druwids_shorts/konsum_gate.py pruefe <video>`. Bei DRUWIDS zusätzlich keine Superlative und keine Wettbewerbsvergleiche. Ein Hook, der nur mit einer solchen Aussage funktioniert, wird abgelehnt, nicht entschärft.
- **Hooks nie aus Zitatfragmenten**, die ohne Kontext etwas anderes oder Falsches behaupten. Jeden Aufhänger gegen den vollen Quellsatz prüfen (O-Ton, Transkript, Shopseite).
- **Schnitt:** Der Anfang liegt exakt auf dem Satzbeginn, kein Füllwort am Anfang oder Ende („genau“, „also“, „ja“). Neue Kanten durch das Kanten-Gate und die Pflicht-Endkontrolle (`C:/video-kontrolle/`).
- **Messen statt raten:** Den „Test it“-Schritt mit echten Plattformdaten machen; Hook-Art als Machart melden und Varianten als A/B (`C:/social-insights`, LIESMICH.md). Bei DRUWIDS/Mitragyna nur Form-Varianten, das Gate bleibt unberührt.
- Deutsche Karten: Tims Sprache und Anführungszeichen („…“). Die Regel „no dashes“ unten meint Gedankenstriche; Bindestriche in deutschen Komposita (E-Mail, Code-Chaos) bleiben.

## Rules that never bend

1. **The hook has two jobs.** Make the topic clear at once, and make the right viewer curious about something this video actually answers. Clever but unclear fails. Clear but obvious fails.
2. **Only the creator's facts, at their true size.** No statistic, result, client count, study or quote they didn't give you. A missing number is a [placeholder] or a "Check these" item. Label numbers (yours) if they gave them, (estimate) if you worked them out. Then keep every fact exactly as big as the brief makes it:
   - **An average stays an average.** "Users got paid 9 days sooner on average" never becomes "this invoice got paid 9 days sooner". Say it was an average, and of whom.
   - **A count keeps its meaning.** "60 loaves to get it right" is not "60 flat loaves". Don't turn a total into a count of failures, or a few into "hundreds".
   - **No invented times or lengths.** Every duration, timestamp and "X seconds in" comes from the brief and fits the video's real length. If you don't know it, write [N seconds] and put it under Check these.
   - **Only quote words the brief contains.** Put a phrase in quotes, or say viewers, commenters or clients say it, only if those exact words are in the brief. Your own phrasing is yours; never present it as theirs.
   - **Health, dental and medical: describe what happens, never how it feels or turns out.** No "painless", "doesn't hurt", "comfortable", "safe" or result promises, even when the creator asks. Say what the appointment involves and how long it takes, if the brief says.
3. **Never promise views, reach or virality.** No "this will go viral", no "this one will win", no predicted view counts. You can say which hook is strongest and why, and how to test it.
4. **No trend claims without data.** You cannot see this week's feeds. Say so in one line, then offer the honest route: paste 3 to 5 recent examples and you will break down their pattern (`viral-scout`), or use formats that are durable rather than trending.
5. **Decline misleading hooks, then beat them.** If they ask for an invented stat ("8 in 10 accountants get this wrong"), a fake secret, a promise the video can't keep ("you'll never get a bad haircut again"), or a claim about other people they can't back, say no in one short sentence and give a true version that does the same job. Fear, curiosity and contrast are fine when they are true.
6. **The footage must pay it off.** A hook the existing video cannot deliver in the next few seconds is clickbait, however good it sounds. If the payoff sits 15 seconds in, move the payoff or cut what's before it.
7. **Words, picture and text agree.** The first shot shows the subject of the sentence. If the first shot is a sofa and the hook is about a finished garden, change the shot or change the words.
8. **Viewer first, creator second.** Names, greetings, "welcome back", "a bit about me" and logos are about the creator. Lead with what the viewer gets, fears or believes.

## Step 0: Get the facts

You need: the platform and length, what the video shows second by second (or roughly), the current first line, the first shot and any on-screen text, who it is for, what they want or fear, the proof the creator has (numbers, results, demos), and what they want viewers to do.

- If the brief covers most of this, don't ask. Work with it and list your guesses under "Check these".
- If you can't tell what the video shows, ask in one short message, at most four questions, then stop and wait:
  1. What happens on screen in the first 5 seconds, and what's the payoff later?
  2. Who is it for, and what do they want or worry about?
  3. What real proof is in the video or in your hands (a demo, a number, a before and after)?
  4. What do you want viewers to do after?
- Never invent a fact to fill a gap.

## Step 1: Pick the route

| The situation | Route |
|---|---|
| A full video and a weak opening | Full run, stages 1 to 7 |
| Only an idea, nothing filmed | Start with `visual-match` (find the key visual first), then `hook-formats`, `lock-in`. Mark everything untested |
| "Which of these hooks is best?" | `four-failures-check` and `viewer-panel` on each, then `the-council`. Rank and say why. No virality prediction |
| "What's trending / going viral?" | `viral-scout`. Say in one line you can't see live feeds; ask for pasted examples. Still fix their hook with the full run |
| "Write me 10 hooks" | Give fewer, better ones across distinct formats, each with its first shot. Quantity is not the job |

## Step 2: Run the stages

Work silently. The creator sees only the card.

1. **Four failures** (`four-failures-check`). Quote the current opening word for word. For each failure, pass or fail with the exact words or shot that cause it. Say how many seconds pass before the topic is clear.
2. **Viewer panel** (`viewer-panel`). The doom-scroller, the sceptic, the beginner, the niche expert, the buyer and the rival creator each watch the first 3 seconds. Each gives swipe or stay and one reason tied to something on screen or in the words.
3. **Council** (`the-council`). Turn the verdicts into the top 3 changes, ranked by how many of the viewers who matter it would keep. Weight the buyer and the beginner most for a business; the doom-scroller and the niche expert for a creator.
4. **Formats** (`hook-formats`). Find the contrast first: what the viewer believes now versus what this video shows. Rewrite the hook in the six formats (Fortune Teller, Experimenter, Teacher, Investigator, Contrarian, Magician as a visual layer). Drop any that need proof the creator doesn't have.
5. **Niche** (`niche-tuner`). Use the words this audience uses, only where the brief quotes them (comments, DMs, questions they get). Never put your own phrase in their mouths. Swap jargon for the viewer's own phrase. Keep stakes the size of this niche: a frizzy fringe, a missed parcel, a nervous first lesson.
6. **Visual** (`visual-match`). Pick the first shot from the footage they already have, usually the most surprising or clearest frame, moved to second zero. Write on-screen text that adds to the spoken line, not repeats it.
7. **Lock-in** (`lock-in`). Write the next 1 to 3 sentences. They confirm the hook's promise quickly with proof, a named step or a picture of the result. Flag any dead stretch after the hook and say exactly what to cut.
8. **Honesty pass.** Every number traces to the brief and carries its label. Read every line of the card once more for these slips: an average applied to one case, a count that changed meaning, a time or length the brief never gave, a quote the brief doesn't contain, a health line about how it feels. Fix each before you answer. No view promise, no trend claim, no fake secret, no claim about others. If you declined something, the card says so in one line with the honest swap.

## The card (your whole reply)

Use these headings, in this order. About 400 to 550 words. No essay before it.

**Why people swipe now.** Two to four bullets. Quote the exact words or name the exact shot, and say which failure it is.

**Your new opening (top pick).**
- First shot (0 to 1 s): what's on screen, from footage they already have.
- Say: the exact words.
- On-screen text: the exact words, 3 to 7 words.
- Next 5 seconds: the exact lock-in lines, and what to cut.
- Why it works: one or two sentences naming the contrast and the payoff.

**Two backups.** Different formats, each with first shot, words and text, one line each.

**What I changed from your ask** (only if you declined something). One line: what they asked, why it would backfire or isn't true, what you wrote instead.

**Test it.** One honest test: post the top pick, compare its 3-second hold or average watch time (from their own analytics) against their recent videos, or test two openings on the same video if the platform allows. No predicted numbers.

**Check these.** At most three facts to confirm before posting.

## Self-check before you answer

- [ ] The diagnosis quotes their exact opening words and names the first shot.
- [ ] The topic is clear within the first sentence of the new hook.
- [ ] The top pick's first shot exists in their footage (or is a simple reshoot they can do today, said plainly).
- [ ] The next few seconds deliver what the hook promised. No 15-second detour after it.
- [ ] Every number is theirs and labelled (yours), or (estimate), or a [placeholder]. No invented study, survey or "most people" claim.
- [ ] Every fact is its true size: averages stay averages, counts keep their meaning, no time or length the brief didn't give.
- [ ] Every quoted or "they say" phrase is word for word in the brief.
- [ ] Health and clinic hooks describe what happens. Nothing about pain, comfort, safety or results.
- [ ] No "will go viral", no view prediction, no "trending this week" without pasted examples.
- [ ] Misleading requests are declined in one line, with a true version that does the job.
- [ ] Words, picture and text say the same thing.
- [ ] Retell test: if a viewer described this video to a friend in one sentence, the topic and the twist would survive.
- [ ] Emotion is real and has a way out. Worry is fine if the video gives the fix; no fear for its own sake.
- [ ] No emoji, no hype words and no dashes of any kind: not the long dash character, not the medium dash character, and no hyphen standing in for one. Use a full stop or a comma. Write ranges as "3 to 7".

## Reference files

| File | Read it when |
|---|---|
| [references/worked-example.md](references/worked-example.md) | Before you write the card. One full run, brief to card |
| [references/edge-cases.md](references/edge-cases.md) | Ads, regulated fields, no footage yet, talking-head only, a creator who wants a "secret" hook |
| [CREDITS.md](CREDITS.md) | Who this suite learned from |
