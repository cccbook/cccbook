cp -r $1 $1_gh

# perl -i.bak.markdown  -p \
perl -0777 -i -p \
  -e 's/\\\[\s*(.*?)\s*\\\]/\$\$\1\$\$\n/gs;' \
  -e 's/\\\(\s*(.*?)\s*\\\)/ \$`\1`\$ /g;' \
  $1_gh/*.md

