#!/bin/sh

cmd="npm"
cmd_opt="install -g"
targets="textlint
textlint-filter-rule-whitelist
textlint-rule-no-start-duplicated-conjunction
textlint-rule-no-doubled-conjunction
textlint-rule-ng-word
textlint-rule-no-dead-link
textlint-rule-terminology
textlint-rule-max-ten
textlint-rule-no-doubled-joshi
textlint-rule-no-double-negative-ja
textlint-rule-ja-no-redundant-expression
textlint-rule-ja-no-abusage
textlint-rule-sentence-length
textlint-rule-first-sentence-length
textlint-rule-no-dropping-the-ra
textlint-rule-no-doubled-conjunctive-particle-ga
textlint-rule-no-doubled-conjunction
textlint-rule-ja-hiragana-keishikimeishi
textlint-rule-ja-hiragana-fukushi
textlint-rule-ja-hiragana-hojodoushi
@textlint-ja/textlint-rule-no-insert-dropping-sa
textlint-rule-prefer-tari-tari
textlint-rule-preset-jtf-style"

for package in $targets; do
  $cmd "$cmd_opt" "$package"
done
