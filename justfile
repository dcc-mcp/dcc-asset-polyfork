default: check

check:
    vx python -m unittest discover -s tests -p "test_*.py" -q

# List only: never install into a user's agent configuration.
discover:
    vx npx --yes skills@1.5.22 add ./skill/polyfork-assets --list


# Verify the pinned VX and just toolchain.
toolchain-ci:
    vx just@1.58 --version
