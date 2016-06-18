# storydigest

storydigest is a little CLI tool to retrieve stories from places that I care
about, which at the moment is a few subreddits and Hacker News, and outputs
then into a format (currently only HTML is supported.)

Configuration is done through a JSON file, an example one is provided, and
the application is launched with `python3 -m storydigest -c <config_file>`