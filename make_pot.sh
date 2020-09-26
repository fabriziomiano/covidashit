# Run from within the environment
pybabel extract -F babel.cfg \
  --project=COVIDashIT \
  --version=2.0 \
  --msgid-bugs-address='fabriziomiano@gmail.com' \
  --copyright-holder='Fabrizio Miano' \
  -o messages.pot .
