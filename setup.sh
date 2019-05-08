if [ -f /usr/local/bin/differ ]
then
    echo "Found a binary existing in /usr/local/bin named 'differ'. Do you want to overwrite it? (y/n): "
    read answer
    if [ "$answer" != "${answer#[Yy]}" ]; then
        echo "Updating differ..."
        rm /usr/local/bin/differ.py
        rm /usr/local/bin/differ
    else
        echo "Canceling install."
        exit 0
    fi
fi

DIFFER_DIR=$(dirname "$BASH_SOURCE")
cp "$DIFFER_DIR/differ.py" /usr/local/bin/differ.py
ln -s /usr/local/bin/differ.py /usr/local/bin/differ

echo "Done!"
exit 0