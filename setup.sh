mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"jroakes@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[global]\n\
logLevel = \"warning\"\n\
" > ~/.streamlit/config.toml
