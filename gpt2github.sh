cp -r $1 $1_bak 

# perl -i.bak.markdown  -p \
perl -0777 -i -p \
  -e 's/\\\[\s*(.*?)\s*\\\]/\$\$\1\$\$/gs;' \
  -e 's/\\\(\s*(.*?)\s*\\\)/\$\1\$/g;' \
  $1/*.md

