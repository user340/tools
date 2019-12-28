#!/bin/sh

cmd="npm"
cmd_opt="install -g"
targets="textlint
@textlint-ja/textlint-rule-no-insert-dropping-sa
@textlint-ja/textlint-rule-no-synonyms
sudachi-synonyms-dictionary
textlint-filter-rule-whitelist
textlint-plugin-html
textlint-rule-first-sentence-length
textlint-rule-ja-hiragana-fukushi
textlint-rule-ja-hiragana-hojodoushi
textlint-rule-ja-hiragana-keishikimeishi
textlint-rule-ja-no-abusage
textlint-rule-ja-no-mixed-period
textlint-rule-ja-no-redundant-expression
textlint-rule-ja-no-successive-word
textlint-rule-ja-no-weak-phrase
textlint-rule-max-ten
textlint-rule-ng-word
textlint-rule-no-dead-link
textlint-rule-no-double-negative-ja
textlint-rule-no-doubled-conjunction
textlint-rule-no-doubled-conjunctive-particle-ga
textlint-rule-no-doubled-joshi
textlint-rule-no-dropping-the-ra
textlint-rule-no-mix-dearu-desumasu
textlint-rule-no-start-duplicated-conjunction
textlint-rule-prefer-tari-tari
textlint-rule-preset-jtf-style
textlint-rule-sentence-length
textlint-rule-terminology"

for package in $targets; do
  $cmd "$cmd_opt" "$package"
done
