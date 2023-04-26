mkdir -p ~/.streamlit/credentials.toml
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml