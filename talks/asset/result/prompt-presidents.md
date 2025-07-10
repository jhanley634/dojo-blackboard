-*- org -*-

| term | party                                        | name                   |
|------+----------------------------------------------+------------------------|
|   47 | Republican                                   | Donald Trump           |
|   46 | Democratic                                   | Joe Biden              |
|   45 | Republican                                   | Donald Trump           |
|   44 | Democratic                                   | Barack Obama           |
|   43 | Republican                                   | George W. Bush         |
|   42 | Democratic                                   | Bill Clinton           |
|   41 | Republican                                   | George H. W. Bush      |
|   40 | Republican                                   | Ronald Reagan          |
|   39 | Democratic                                   | Jimmy Carter           |
|   38 | Republican                                   | Gerald Ford            |
|   37 | Republican                                   | Richard Nixon          |
|   36 | Democratic                                   | Lyndon B. Johnson      |
|   35 | Democratic                                   | John F. Kennedy        |
|   34 | Republican                                   | Dwight D. Eisenhower   |
|   33 | Democratic                                   | Harry S. Truman        |
|   32 | Democratic                                   | Franklin D. Roosevelt  |
|   31 | Republican                                   | Herbert Hoover         |
|   30 | Republican                                   | Calvin Coolidge        |
|   29 | Republican                                   | Warren G. Harding      |
|   28 | Democratic                                   | Woodrow Wilson         |
|   27 | Republican                                   | William Howard Taft    |
|   26 | Republican                                   | Theodore Roosevelt     |
|   25 | Republican                                   | William McKinley       |
|   24 | Democratic                                   | Grover Cleveland       |
|   23 | Republican                                   | Benjamin Harrison      |
|   22 | Democratic                                   | Grover Cleveland       |
|   21 | Republican                                   | Chester A. Arthur      |
|   20 | Republican                                   | James A. Garfield      |
|   19 | Republican                                   | Rutherford B. Hayes    |
|   18 | Republican                                   | Ulysses S. Grant       |
|   17 | National Union[n]Democratic                  | Andrew Johnson         |
|   16 | RepublicanNational Union[l]                  | Abraham Lincoln        |
|   15 | Democratic                                   | James Buchanan         |
|   14 | Democratic                                   | Franklin Pierce        |
|   13 | Whig                                         | Millard Fillmore       |
|   12 | Whig                                         | Zachary Taylor         |
|   11 | Democratic                                   | James K. Polk          |
|   10 | Whig[j]Unaffiliated                          | John Tyler             |
|    9 | Whig                                         | William Henry Harrison |
|    8 | Democratic                                   | Martin Van Buren       |
|    7 | Democratic                                   | Andrew Jackson         |
|    6 | Democratic- Republican[f]National Republican | John Quincy Adams      |
|    5 | Democratic- Republican                       | James Monroe           |
|    4 | Democratic- Republican                       | James Madison          |
|    3 | Democratic- Republican                       | Thomas Jefferson       |
|    2 | Federalist                                   | John Adams             |
|    1 | Unaffiliated                                 | George Washington      |

Generate a response with low randomness. Please provide a clear and structured answer to the following question

Produce a markdown table of U.S. presidents since Franklin Delano Roosevelt, in reverse chronological order.
Each row in the table should contain the following fields:
- `term`: the number of the president, with Washington. as 1 and Obama as 44
- `party`: the party affiliation of the president, one of {Dem., Rep., Other}
- `president`: the last name of the president; give only the last name

Column headings shall be lowercase.
President last name shall be a single word with initial letter uppercased,
for example Bush rather than bush.
Be sure to avoid including Hoover in the table,
nor anyone who served in the years before him.
Notice that `term` shall always be less than 48.
Do not include an entry in the table if its `term` is less than 32.
Think in steps. Verify each line of the table.
