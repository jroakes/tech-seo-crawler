mkdir -p ~/.streamlit/


pip install torch==1.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

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
