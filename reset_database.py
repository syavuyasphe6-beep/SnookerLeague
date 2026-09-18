from database import get_connection


connection = get_connection()
cursor = connection.cursor()


# ==========================================
# DELETE ALL MATCH RESULTS
# ==========================================

cursor.execute("""
DELETE FROM matches
""")


# ==========================================
# RESET ALL FIXTURES
# ==========================================

cursor.execute("""
UPDATE fixtures
SET status = 'Scheduled'
""")


connection.commit()


# ==========================================
# CHECK RESULTS
# ==========================================

cursor.execute("""
SELECT COUNT(*)
FROM matches
""")

match_count = cursor.fetchone()[0]


print("========================================")
print("       DATABASE RESET COMPLETE")
print("========================================")
print("Matches remaining:", match_count)
print("All fixtures are now Scheduled.")
print("Players have NOT been deleted.")
print("========================================")


cursor.close()
connection.close()