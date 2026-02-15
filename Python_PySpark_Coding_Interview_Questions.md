# Python & PySpark Coding Interview Questions
## U.S. Bank - Senior Software Engineer - Analytics & AI

---

## Python Coding Questions (20 Questions)

### Data Structures & Algorithms (5 questions)

1. **Two Sum Problem**
   - Given an array of integers and a target sum, return indices of two numbers that add up to the target.
   - Follow-up: What if the array is sorted? How would you optimize?

2. **Find Duplicates in Transaction Data**
   - Given a list of transaction IDs, find all duplicates and return them along with their count.
   - Optimize for time and space complexity.

3. **Merge Overlapping Time Intervals**
   - Given a list of time intervals (start, end), merge all overlapping intervals.
   - Example: [(1,3), (2,6), (8,10), (15,18)] → [(1,6), (8,10), (15,18)]

4. **Implement LRU Cache**
   - Design and implement a Least Recently Used (LRU) cache with get() and put() operations.
   - Both operations should run in O(1) time.

5. **Valid Parentheses/Brackets**
   - Given a string containing brackets '(', ')', '{', '}', '[', ']', determine if the input is valid.
   - All open brackets must be closed by the same type in correct order.

---

### Data Processing & Manipulation (5 questions)

6. **Process CSV Data**
   ```python
   # Given a CSV file with customer transactions:
   # customer_id, transaction_date, amount, category
   # Write a function to:
   # - Calculate total spending per customer
   # - Find top 10 customers by spending
   # - Calculate average transaction amount by category
   ```

7. **Data Cleaning Function**
   ```python
   # Write a function to clean messy data:
   # - Remove null values
   # - Handle missing data (forward fill, backward fill, mean imputation)
   # - Remove duplicates
   # - Convert data types appropriately
   # - Handle outliers
   ```

8. **JSON Data Flattening**
   ```python
   # Given nested JSON data structure:
   {
       "customer": {
           "id": 123,
           "name": "John",
           "accounts": [
               {"type": "checking", "balance": 5000},
               {"type": "savings", "balance": 15000}
           ]
       }
   }
   # Flatten it to a dictionary or DataFrame
   ```

9. **Time Series Data Aggregation**
   ```python
   # Given transaction data with timestamps:
   # - Aggregate by day, week, month
   # - Calculate rolling averages (7-day, 30-day)
   # - Detect anomalies (transactions > 2 std deviations)
   ```

10. **Data Validation Pipeline**
    ```python
    # Create a validation framework to check:
    # - Data types match schema
    # - Required fields are not null
    # - Values fall within expected ranges
    # - Foreign key constraints are maintained
    # Return detailed error report
    ```

---

### Pandas Operations (5 questions)

11. **GroupBy and Aggregation**
    ```python
    # Given a DataFrame with columns: customer_id, product_id, quantity, price, date
    # Calculate:
    # - Total revenue per customer
    # - Most purchased products
    # - Monthly sales trends
    # - Customer lifetime value
    ```

12. **Merge and Join Operations**
    ```python
    # Given three DataFrames:
    # - customers (customer_id, name, segment)
    # - transactions (transaction_id, customer_id, amount, date)
    # - products (product_id, transaction_id, product_name, category)
    # 
    # Perform complex joins to create a unified view
    # Handle missing values and duplicates
    ```

13. **Pivot and Reshape Data**
    ```python
    # Transform transaction data from long format to wide format
    # Create pivot tables showing:
    # - Products (rows) vs Months (columns) with sales values
    # - Multi-level indexing for hierarchical data
    ```

14. **Window Functions in Pandas**
    ```python
    # Calculate:
    # - Running total of transactions per customer
    # - Rank customers by transaction amount within each month
    # - Calculate percentage change from previous transaction
    ```

15. **Handle Missing Data Strategically**
    ```python
    # Given financial data with missing values:
    # - Identify patterns in missing data
    # - Implement different imputation strategies
    # - Compare results and justify approach
    ```

---

### API and Data Integration (3 questions)

16. **REST API Client**
    ```python
    # Create a robust API client that:
    # - Handles authentication (OAuth, API keys)
    # - Implements retry logic with exponential backoff
    # - Handles rate limiting
    # - Parses and validates responses
    # - Logs errors appropriately
    ```

17. **Async Data Fetching**
    ```python
    # Use asyncio/aiohttp to fetch data from multiple endpoints concurrently
    # Implement error handling and timeout management
    # Aggregate results from multiple sources
    ```

18. **Database Connection and Query**
    ```python
    # Connect to SQL database using SQLAlchemy or psycopg2
    # Execute parameterized queries safely (prevent SQL injection)
    # Handle connection pooling
    # Implement transaction management
    ```

---

### Testing and Quality (2 questions)

19. **Unit Testing with pytest**
    ```python
    # Write comprehensive unit tests for a data processing function:
    # - Test edge cases (empty data, null values, duplicates)
    # - Use fixtures and parametrize
    # - Mock external dependencies
    # - Test exception handling
    ```

20. **Data Quality Checks**
    ```python
    # Implement automated data quality checks:
    # - Schema validation
    # - Statistical profiling
    # - Anomaly detection
    # - Data lineage tracking
    ```

---

## PySpark Coding Questions (20 Questions)

### PySpark Fundamentals (5 questions)

21. **RDD vs DataFrame vs Dataset**
    ```python
    # Explain differences and when to use each
    # Convert between RDD and DataFrame
    # Demonstrate transformations and actions
    ```

22. **Word Count with PySpark**
    ```python
    # Classic MapReduce problem:
    # - Read text file
    # - Split into words
    # - Count occurrences
    # - Sort by frequency
    # Optimize for large files
    ```

23. **Filter and Select Operations**
    ```python
    # Given a large transaction dataset:
    # - Filter transactions above threshold
    # - Select specific columns
    # - Apply multiple conditions efficiently
    # - Use column expressions
    ```

24. **Join Operations in PySpark**
    ```python
    # Perform different types of joins:
    # - Inner join
    # - Left/Right outer join
    # - Full outer join
    # - Handle skewed data in joins
    # Broadcast join for small tables
    ```

25. **UDF (User Defined Functions)**
    ```python
    # Create and optimize UDFs:
    # - Regular UDF
    # - Pandas UDF (vectorized)
    # - Compare performance
    # Apply complex transformations
    ```

---

### Data Processing & ETL (5 questions)

26. **Read and Write Different Formats**
    ```python
    # Read/Write data in multiple formats:
    # - CSV, JSON, Parquet, Avro, ORC
    # - Handle schema inference vs explicit schema
    # - Partition data efficiently
    # - Configure compression
    ```

27. **Data Deduplication**
    ```python
    # Remove duplicate records from large dataset:
    # - Based on single column
    # - Based on multiple columns
    # - Keep first/last occurrence
    # - Handle partial duplicates
    ```

28. **Window Functions**
    ```python
    # Implement window operations:
    # - Ranking (rank, dense_rank, row_number)
    # - Running totals and cumulative sums
    # - Lead and lag functions
    # - Partition by multiple columns
    ```

29. **Aggregations and GroupBy**
    ```python
    # Complex aggregation scenarios:
    # - Multiple aggregation functions
    # - GroupBy with multiple columns
    # - Filter after aggregation (having clause)
    # - Rollup and cube operations
    ```

30. **Handle Null Values**
    ```python
    # Null handling strategies:
    # - Fill nulls with specific values
    # - Drop rows with nulls
    # - Replace nulls based on conditions
    # - Coalesce multiple columns
    ```

---

### Performance Optimization (5 questions)

31. **Partition Management**
    ```python
    # Optimize partitioning:
    # - Repartition vs Coalesce
    # - Determine optimal partition count
    # - Partition by specific columns
    # - Handle data skew
    ```

32. **Caching and Persistence**
    ```python
    # When and how to cache DataFrames:
    # - cache() vs persist()
    # - Storage levels (MEMORY_ONLY, MEMORY_AND_DISK, etc.)
    # - Unpersist when done
    # - Monitor cache usage
    ```

33. **Broadcast Variables**
    ```python
    # Optimize joins with broadcast:
    # - When to use broadcast joins
    # - Create and use broadcast variables
    # - Memory considerations
    # - Performance comparison
    ```

34. **Optimize Shuffle Operations**
    ```python
    # Minimize shuffle overhead:
    # - Identify operations that cause shuffles
    # - Use narrow transformations when possible
    # - Configure shuffle partitions
    # - Salting for skewed data
    ```

35. **Query Execution Plan Analysis**
    ```python
    # Analyze and optimize queries:
    # - Use explain() to view execution plan
    # - Identify bottlenecks
    # - Optimize transformations
    # - Compare different approaches
    ```

---

### Streaming & Real-time Processing (3 questions)

36. **Structured Streaming Basics**
    ```python
    # Implement streaming application:
    # - Read from streaming source (Kafka, socket)
    # - Apply transformations
    # - Write to sink
    # - Handle late data and watermarks
    ```

37. **Windowing in Streaming**
    ```python
    # Implement time-based windows:
    # - Tumbling windows
    # - Sliding windows
    # - Session windows
    # - Aggregations over windows
    ```

38. **Stateful Streaming Operations**
    ```python
    # Maintain state across batches:
    # - UpdateStateByKey
    # - MapGroupsWithState
    # - Handle state timeout
    # - Checkpointing
    ```

---

### Advanced Scenarios (4 questions)

39. **Handle Skewed Data**
    ```python
    # Strategies for data skew:
    # - Detect skewed keys
    # - Salting technique
    # - Isolated broadcast join
    # - Custom partitioner
    ```

40. **Complex Data Transformations**
    ```python
    # Given nested JSON data in DataFrame:
    # - Explode arrays
    # - Flatten nested structures
    # - Handle schema evolution
    # - Type casting and validation
    ```

41. **Incremental Data Processing**
    ```python
    # Implement incremental load:
    # - Track processed data (watermark)
    # - Process only new/changed records
    # - Handle late-arriving data
    # - Maintain idempotency
    ```

42. **Machine Learning Pipeline**
    ```python
    # Build ML pipeline with PySpark:
    # - Feature engineering (VectorAssembler, StringIndexer)
    # - Train-test split
    # - Model training (RandomForest, GBT)
    # - Hyperparameter tuning (CrossValidator)
    # - Model evaluation and deployment
    ```

---

### Integration with Azure (3 questions)

43. **Read from Azure Data Lake**
    ```python
    # Configure Spark to read from ADLS Gen2:
    # - Authentication setup
    # - Read Parquet/CSV files
    # - Handle partition pruning
    # - Optimize read performance
    ```

44. **Write to Azure Synapse**
    ```python
    # Write PySpark DataFrame to Synapse:
    # - Use JDBC/PolyBase
    # - Bulk insert optimization
    # - Handle data types mapping
    # - Error handling and retry logic
    ```

45. **Integrate with Azure Databricks**
    ```python
    # Databricks-specific optimizations:
    # - Use Delta Lake format
    # - Implement Delta merge (upsert)
    # - Time travel queries
    # - Optimize write with Z-ordering
    ```

---

## System Design Questions (5 Questions)

46. **Design ETL Pipeline**
    - Design an end-to-end ETL pipeline for processing millions of daily transactions
    - Discuss data ingestion, transformation, validation, and loading
    - Handle failures and implement monitoring

47. **Real-time Fraud Detection System**
    - Design a system to detect fraudulent transactions in real-time
    - Discuss data streaming, feature engineering, model serving
    - Scalability and latency requirements

48. **Data Lake Architecture**
    - Design a data lake for a banking organization
    - Discuss raw/curated/consumption layers
    - Data governance, security, and compliance
    - Query performance optimization

49. **ML Model Deployment Pipeline**
    - Design MLOps pipeline for model deployment
    - Discuss versioning, A/B testing, monitoring
    - Rollback strategies and CI/CD integration

50. **Batch Processing vs Stream Processing**
    - Compare and contrast approaches
    - When to use each
    - Hybrid architectures (Lambda/Kappa)
    - Trade-offs and considerations

---

## Preparation Tips

### For Python:
1. **Practice on LeetCode/HackerRank**: Focus on medium to hard problems
2. **Master Pandas**: GroupBy, merge, pivot, apply functions
3. **Understand Time/Space Complexity**: Big O notation
4. **Exception Handling**: Proper error handling and logging
5. **Code Quality**: Clean, readable, maintainable code with comments

### For PySpark:
1. **Understand Lazy Evaluation**: Transformations vs Actions
2. **Optimization Techniques**: Partitioning, caching, broadcast
3. **Debug Execution Plans**: Use explain() and Spark UI
4. **Know DataFrame API Well**: Prefer DataFrame over RDD
5. **Practice on Databricks Community Edition**: Free environment

### General Interview Approach:
1. **Clarify Requirements**: Ask questions before coding
2. **Think Out Loud**: Explain your thought process
3. **Start Simple**: Get a working solution first, then optimize
4. **Test Your Code**: Walk through test cases
5. **Discuss Trade-offs**: Time vs space, readability vs performance
6. **Know Your Past Projects**: Be ready to discuss in detail

### Key Concepts to Review:
- **Data Structures**: Lists, dicts, sets, heaps, trees
- **Algorithms**: Sorting, searching, dynamic programming
- **SQL**: Joins, subqueries, window functions, CTEs
- **Distributed Computing**: MapReduce paradigm, shuffling
- **Performance Tuning**: Profiling, optimization techniques
- **Testing**: Unit tests, integration tests, mocking

---

## Mock Interview Questions

Practice explaining these scenarios:

1. "Walk me through how you would process 1TB of transaction data daily"
2. "How would you optimize a slow-running PySpark job?"
3. "Explain the difference between map() and mapPartitions()"
4. "How do you handle data quality issues in production pipelines?"
5. "What's your approach to debugging a failed Spark job?"

---

## Online Resources

- **PySpark Documentation**: https://spark.apache.org/docs/latest/api/python/
- **LeetCode**: Python and SQL problems
- **Databricks Training**: Free courses on Apache Spark
- **Real Python**: Advanced Python tutorials
- **Spark by Examples**: PySpark examples and tutorials

Good luck with your interview! 🚀
