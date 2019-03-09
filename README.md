This is a placeholder README. If you read this sentence, then this work is completely not ready, and in progress.

Inspired by:
1. Facebook's internal web framework
2. https://github.com/mikeland86/graphp
3. https://github.com/schrockn/graphscale
4. Database schema inspirations:


References:
- Scaling Pinterest: http://highscalability.com/blog/2013/4/15/scaling-pinterest-from-0-to-10s-of-billions-of-page-views-a.html
- https://medium.com/@Pinterest_Engineering/sharding-pinterest-how-we-scaled-our-mysql-fleet-3f341e96ca6f
    - ID: 64 = 2 reserve bits | 16 bit Shard ID | 10 bit object type |  36 bit local ID: auto increment ID
        - Question: how is this local ID created initially?
- Instagram: https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c
- Uber: https://eng.uber.com/schemaless-part-one/
- Uber Mysql > Postgres https://eng.uber.com/mysql-migration/
- Square’s Vitess series: https://medium.com/square-corner-blog/sharding-cash-10280fa3ef3b
