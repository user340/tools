#!/bin/sh

cmd="npm"
cmd_opt="install -g"
targets="textlint-rule-no-start-duplicated-conjunction
textlint-rule-no-exclamation-question-mark
textlint-rule-ng-word
textlint-rule-no-dead-link
textlint-rule-date-weekday-mismatch
textlint-rule-terminology
textlint-rule-no-nfd
textlint-rule-no-surrogate-pair
textlint-rule-max-ten
textlint-rule-max-kanji-continuous-len
textlint-rule-no-doubled-joshi
textlint-rule-no-double-negative-ja
textlint-rule-no-hankaku-kana
textlint-rule-ja-no-redundant-expression
textlint-rule-ja-no-abusage
textlint-rule-no-mixed-zenkaku-and-hankaku-alphabet
textlint-rule-sentence-length
textlint-rule-first-sentence-length
textlint-rule-no-dropping-the-ra
textlint-rule-no-doubled-conjunctive-particle-ga
textlint-rule-no-doubled-conjunction
textlint-rule-ja-no-mixed-period
textlint-rule-max-appearence-count-of-words
textlint-rule-max-length-of-title
textlint-rule-incremental-headers
textlint-rule-ja-hiragana-keishikimeishi
textlint-rule-ja-hiragana-fukushi
textlint-rule-ja-hiragana-hojodoushi
textlint-rule-ja-unnatural-alphabet
@textlint-ja/textlint-rule-no-insert-dropping-sa
textlint-rule-prefer-tari-tari
textlint-rule-preset-jtf-style"

for package in $targets; do
  $cmd "$cmd_opt" "$package"
done
