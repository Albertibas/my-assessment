"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)

NOTE:
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""


def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    #Join the credit and customer tables using CustomerID as the link. (1-to-1 relationship)
    #The group by applies the average function per class

    qry = """
    SELECT AVG(cu.Income) as AverageIncome, cr.CustomerClass FROM customers AS cu 
    INNER JOIN credit AS cr ON cr.CustomerID = cu.CustomerID 
    GROUP BY CustomerClass
    """

    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

    #Join of tables "customers" and "loans" in order to get rejections by province. 
    #Use multiple clause CASE to standardize the naming of provinces

    qry = """
    SELECT Count(l.ApprovalStatus) AS RejectedApplications, 
    CASE
        WHEN UPPER(c.Region) IN ('LP','LIMPOPO') THEN 'LP'
        WHEN UPPER(c.Region) IN ('KZN','KWAZULU-NATAL') THEN 'KZN'
        WHEN UPPER(c.Region) IN ('FS','FREESTATE') THEN 'FS'
        WHEN UPPER(c.Region) IN ('EC','EASTERNCAPE') THEN 'EC'
        WHEN UPPER(c.Region) IN ('WC','WESTERNCAPE') THEN 'WC'
        WHEN UPPER(c.Region) IN ('NC','NORTHERNCAPE') THEN 'NC'
        WHEN UPPER(c.Region) IN ('NW','NORTHWEST','NORTH-WEST') THEN 'NW'
        WHEN UPPER(c.Region) IN ('GT','GAUTENG') THEN 'GT'
        WHEN UPPER(c.Region) IN ('MP','MPUMALANGA') THEN 'MP'
    END AS Province 
    FROM customers AS c 
    INNER JOIN loans AS l ON l.CustomerID = c.CustomerID
    WHERE l.ApprovalStatus = 'Rejected'
    GROUP BY Province
    """

    return qry


def question_3():
    """
    Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    #Two SQL statements are included into the same query.
    #The first creates a table with the relevant information.
    #The second copies data from three different tables into that table. 
    
    qry = """
    CREATE TABLE financing (CustomerID INT, --CustomerID not used as primary key, due to duplicates in database.
    Income DECIMAL,
    LoanAmount DECIMAL,
    LoanTerm INT,
    InterestRate DECIMAL,
    ApprovalStatus VARCHAR(50),
    CreditScore INT);
    
    INSERT INTO financing (CustomerID, Income, LoanAmount, LoanTerm, InterestRate, ApprovalStatus, CreditScore)
    SELECT c.CustomerID, c.Income, l.LoanAmount, l.LoanTerm, l.InterestRate, l.ApprovalStatus, cr.CreditScore
    FROM customers AS c
    INNER JOIN loans AS l ON l.CustomerID = c.CustomerID
    INNER JOIN credit AS cr ON cr.CustomerID = c.CustomerID
    """

    return qry


# Question 4 and 5 are linked


def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time.
    Null values to be filled with 0.

    Hint: there should be 12x CustomerID = 1.
    """

    #It should be noted that the answers for Question 4 to 7 make heavy use of Artificial Intelligence LLM's

    qry = """
    
    CREATE TABLE timeline AS
    SELECT -- Use Coalesce to insert zeroes where needed
    c.CustomerID, m.MonthName, COALESCE(r.num_repayments, 0)   AS NumberOfRepayments, COALESCE(r.total_amount,   0.0) AS AmountTotal
    FROM
    customers AS c
    CROSS JOIN months AS m
    LEFT JOIN (
        SELECT CustomerID,
        EXTRACT(MONTH FROM (RepaymentDate AT TIME ZONE TimeZone) AT TIME ZONE 'Europe/London')::INT AS month_id,
            COUNT(*)    AS num_repayments,
            SUM(Amount) AS total_amount
        FROM
            repayments
        WHERE
            ((RepaymentDate AT TIME ZONE TimeZone) AT TIME ZONE 'Europe/London')::time
                BETWEEN '06:00' AND '18:00'
        GROUP BY
            CustomerID,
            month_id
    ) AS r
      ON c.CustomerID = r.CustomerID
     AND m.MonthID    = r.month_id
    ORDER BY
    c.CustomerID,
    m.MonthID;
    
    """

    return qry


def question_5():
    """
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """

    qry = """
SELECT
  CustomerID,

  -- January
  SUM(CASE WHEN MonthName = 'January'   THEN NumberOfRepayments ELSE 0 END)::INT AS JanuaryRepayments,
  SUM(CASE WHEN MonthName = 'January'   THEN AmountTotal        ELSE 0 END)        AS JanuaryTotal,

  -- February
  SUM(CASE WHEN MonthName = 'February'  THEN NumberOfRepayments ELSE 0 END)::INT AS FebruaryRepayments,
  SUM(CASE WHEN MonthName = 'February'  THEN AmountTotal        ELSE 0 END)        AS FebruaryTotal,

  -- March
  SUM(CASE WHEN MonthName = 'March'     THEN NumberOfRepayments ELSE 0 END)::INT AS MarchRepayments,
  SUM(CASE WHEN MonthName = 'March'     THEN AmountTotal        ELSE 0 END)        AS MarchTotal,

  -- April
  SUM(CASE WHEN MonthName = 'April'     THEN NumberOfRepayments ELSE 0 END)::INT AS AprilRepayments,
  SUM(CASE WHEN MonthName = 'April'     THEN AmountTotal        ELSE 0 END)        AS AprilTotal,

  -- May
  SUM(CASE WHEN MonthName = 'May'       THEN NumberOfRepayments ELSE 0 END)::INT AS MayRepayments,
  SUM(CASE WHEN MonthName = 'May'       THEN AmountTotal        ELSE 0 END)        AS MayTotal,

  -- June
  SUM(CASE WHEN MonthName = 'June'      THEN NumberOfRepayments ELSE 0 END)::INT AS JuneRepayments,
  SUM(CASE WHEN MonthName = 'June'      THEN AmountTotal        ELSE 0 END)        AS JuneTotal,

  -- July
  SUM(CASE WHEN MonthName = 'July'      THEN NumberOfRepayments ELSE 0 END)::INT AS JulyRepayments,
  SUM(CASE WHEN MonthName = 'July'      THEN AmountTotal        ELSE 0 END)        AS JulyTotal,

  -- August
  SUM(CASE WHEN MonthName = 'August'    THEN NumberOfRepayments ELSE 0 END)::INT AS AugustRepayments,
  SUM(CASE WHEN MonthName = 'August'    THEN AmountTotal        ELSE 0 END)        AS AugustTotal,

  -- September
  SUM(CASE WHEN MonthName = 'September' THEN NumberOfRepayments ELSE 0 END)::INT AS SeptemberRepayments,
  SUM(CASE WHEN MonthName = 'September' THEN AmountTotal        ELSE 0 END)        AS SeptemberTotal,

  -- October
  SUM(CASE WHEN MonthName = 'October'   THEN NumberOfRepayments ELSE 0 END)::INT AS OctoberRepayments,
  SUM(CASE WHEN MonthName = 'October'   THEN AmountTotal        ELSE 0 END)        AS OctoberTotal,

  -- November
  SUM(CASE WHEN MonthName = 'November'  THEN NumberOfRepayments ELSE 0 END)::INT AS NovemberRepayments,
  SUM(CASE WHEN MonthName = 'November'  THEN AmountTotal        ELSE 0 END)        AS NovemberTotal,

  -- December
  SUM(CASE WHEN MonthName = 'December'  THEN NumberOfRepayments ELSE 0 END)::INT AS DecemberRepayments,
  SUM(CASE WHEN MonthName = 'December'  THEN AmountTotal        ELSE 0 END)        AS DecemberTotal

FROM
  timeline
GROUP BY
  CustomerID;
    """

    return qry


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these question.


def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """

    qry = """
        -- 1) Build the corrected_customers table
        CREATE TABLE corrected_customers AS
        WITH numbered AS (
          SELECT
            CustomerID,
            Age,
            Gender,
            ROW_NUMBER()   OVER (PARTITION BY Gender ORDER BY CustomerID) AS rn,
            COUNT(*)       OVER (PARTITION BY Gender)             AS cnt
          FROM customers
        )
        SELECT
          c1.CustomerID,
          c1.Age                           AS Age,
          
          -- compute the shifting index: (rn − 3) mod cnt + 1
          c2.Age                           AS CorrectedAge,
          
          c1.Gender
        FROM numbered AS c1
        JOIN numbered AS c2
          ON c1.Gender = c2.Gender
         AND c2.rn = ((c1.rn + c1.cnt - 3) % c1.cnt) + 1
        ORDER BY
          c1.Gender,
          c1.CustomerID
        ;
        
        SELECT * FROM corrected_customers
    """

    return qry


def question_7():
    """
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`
    """

    qry = """
            -- 1) Add the two new columns
        ALTER TABLE corrected_customers
          ADD COLUMN AgeCategory TEXT;

        ALTER TABLE corrected_customers
          ADD COLUMN Rank INTEGER;
        
        -- 2) Populate AgeCategory by corrected age
        UPDATE corrected_customers
        SET AgeCategory = CASE
            WHEN CorrectedAge < 20              THEN 'Teen'
            WHEN CorrectedAge >= 20
              AND CorrectedAge < 30            THEN 'Young Adult'
            WHEN CorrectedAge >= 30
              AND CorrectedAge < 60            THEN 'Adult'
            WHEN CorrectedAge >= 60             THEN 'Pensioner'
            ELSE 'Unknown'
          END;
        
        -- 3) Build a helper expression to count each customer’s repayments
        WITH repay_counts AS (
          SELECT
            CustomerID,
            COUNT(*) AS cnt
          FROM repayments
          GROUP BY CustomerID
        ),
        
        -- 4) Join counts into corrected_customers, defaulting to zero
        with_counts AS (
          SELECT
            cc.CustomerID,
            cc.Age,
            cc.CorrectedAge,
            cc.Gender,
            cc.AgeCategory,
            COALESCE(rc.cnt, 0) AS repay_count
          FROM
            corrected_customers AS cc
            LEFT JOIN repay_counts AS rc USING (CustomerID)
        )
        
        -- 5) Use DENSE_RANK over each AgeCategory (highest repay_count → rank=1)
        UPDATE corrected_customers AS dst
        SET Rank = src.rnk
        FROM (
          SELECT
            CustomerID,
            DENSE_RANK() OVER (
              PARTITION BY AgeCategory
              ORDER BY repay_count DESC
            ) AS rnk
          FROM with_counts
        ) AS src
        WHERE dst.CustomerID = src.CustomerID;
        
        -- 6) Finally, see the results
        SELECT
          CustomerID,
          Age,
          CorrectedAge,
          Gender,
          AgeCategory,
          Rank
        FROM corrected_customers
        ORDER BY AgeCategory, Rank, CustomerID;
    """

    return qry
