-*- org -*-

+ cat
+ ollama run deepseek-coder-v2
⠙ ⠹ ⠹ ⠼ ⠼ ⠦ ⠦ ⠇ ⠏ ⠋ ⠙ ⠹ ⠸ ⠸ ⠴ ⠦ ⠧ ⠇ ⠇ ⠋ ⠋ ⠙ ⠸ ⠼ ⠼ ⠦ ⠧ ⠇ ⠏ ⠋ ⠋ ⠹ ⠸ ⠼ ⠼ ⠦ ⠧ ⠧ ⠇ ⠋ ⠙ ⠹ ⠹ ⠼ ⠴ ⠴ ⠦ ⠇ ⠏ ⠋ ⠋ ⠹ ⠹ ⠼ ⠴ ⠦ ⠦ ⠇ ⠏ ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏ ⠏ ⠙ ⠹ ⠹ ⠸ ⠼ ⠦ ⠦ ⠇ ⠏ ⠏ ⠋ ⠙ ⠸ ⠼ ⠼ ⠴  To generate a markdown table of U.S. presidents since Franklin Delano Roosevelt, in reverse chronological order, excluding Hoover and anyone who served before his term, we need to filter out those not meeting the criteria and format them accordingly. Here's the step-by-step process:

1. **Filter Data**: Select only those entries where `term` is greater than or equal to 32 (corresponding to Roosevelt).
2. **Map Party Names**: Replace "Republican" with "Rep." and "Democratic" with "Dem.".
3. **Format President's Last Name**: Ensure the president's last name starts with a capital letter.
4. **Exclude Hoover**: Remove any entry for Richard Nixon (term 37).
5. **Sort Data**: Sort the filtered data in reverse chronological order based on `term`.
6. **Generate Table**: Format the data into a markdown table with appropriate column headings.

Here is the resulting table:

```markdown
| term | party    | president |
|------|----------|-----------|
| 47   | Rep.     | Trump     |
| 46   | Dem.     | Biden      |
| 45   | Rep.     | Trump     |
| 44   | Dem.     | Obama     |
| 43   | Rep.     | Bush      |
| 42   | Dem.     | Clinton   |
| 41   | Rep.     | Bush      |
| 40   | Rep.     | Reagan    |
| 39   | Dem.     | Carter    |
| 38   | Rep.     | Ford      |
| 37   | Rep.     | Nixon     |
| 36   | Dem.     | Johnson   |
| 35   | Dem.     | Kennedy   |
| 34   | Rep.     | Eisenhower|
| 33   | Dem.     | Truman    |
| 32   | Dem.     | Roosevelt |
```

This table includes all U.S. presidents since Franklin Delano Roosevelt, in reverse chronological order, with the specified formatting and exclusions applied.


real	0m19.378s
user	0m0.050s
sys	0m0.059s
