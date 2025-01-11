cp -r $1 $1_bak 

# perl -i.bak.markdown  -p \
perl -i -p \
  -e 's/\\\[/\$\$/gm;' \
  -e 's/\\\]/\$\$/gm;' \
  -e 's/\\\(/\$/g;' \
  -e 's/\\\)/\$/g;' \
  $1/*.md