import sqlite3

connection = sqlite3.connect("snooker.db")
cursor = connection.cursor()

# Delete all match results
cursor.execute("""
DELETE FROM matches
""")

# Reset all fixtures back to Scheduled
cursor.execute("""
UPDATE fixtures
SET status = 'Scheduled'
""")

connection.commit()

# Check that results were deleted
cursor.execute("SELECT COUNT(*) FROM matches")
match_count = cursor.fetchone()[0]

print("========================================")
print("       DATABASE RESET COMPLETE")
print("========================================")
print("Matches remaining:", match_count)
print("All fixtures are now Scheduled.")
print("Players have NOT been deleted.")
print("========================================")

connection.close()
