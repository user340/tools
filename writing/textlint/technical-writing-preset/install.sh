#!/bin/sh

cmd="npm"
cmd_opt="install -g"
package="textlint-rule-preset-ja-technical-writing"
textlintrc="textlintrc"

for package in $targets; do
  $cmd "$cmd_opt" "$package"
done

if [ -f "$textlintrc" ]; then
    if [ -f "$HOME/.${textlintrc}" ]; then
        exit 0
    else
        cp "$textlintrc" "$HOME/.${textlintrc}"
    fi
fi
