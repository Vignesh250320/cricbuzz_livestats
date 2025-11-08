# 📥 Data Ingestion Guide

## ✅ What Was Created

A new **Data Ingestion page** that fetches data from Cricbuzz API and inserts it into **your existing database schema**.

### Key Features:
1. ✅ **Works with your current schema** (Players, Matches, Teams, Venues, Series)
2. ✅ **Fetches real data** from Cricbuzz API
3. ✅ **Preview before insert** - see data before adding to DB
4. ✅ **Automatic mapping** - handles team/venue/series relationships
5. ✅ **Duplicate prevention** - won't insert same records twice

---

## 🚀 How to Use

### Step 1: Run Your App
```bash
streamlit run app.py
```

### Step 2: Navigate to Data Ingestion
Click **📥 Data Ingestion** in the sidebar

### Step 3: Fetch Data
1. Select a data source:
   - **Matches - Recent** (recommended to start)
   - **Matches - Live**
   - **Matches - Upcoming**
   - **Players - Top Run Scorers**
   - **Players - Top Wicket Takers**

2. Click **🔄 Fetch Data**

3. Preview the data that was fetched

### Step 4: Insert to Database
1. Click **💾 Insert into Database**
2. The system will automatically:
   - Insert Teams
   - Insert Venues
   - Insert Series
   - Insert Matches
   - Link everything properly

### Step 5: Verify
- Check the **Database Stats** at the bottom
- Go to **SQL Practice Queries** to see your queries return more data!

---

## 📊 Recommended Sequence

### 1. First Run - Get Matches
```
1. Fetch "Matches - Recent"
2. Insert to DB
3. You'll get: Teams, Venues, Series, and Matches
```

### 2. Second Run - Get Players
```
1. Fetch "Players - Top Run Scorers"
2. Insert to DB
3. You'll get: Player stats updated
```

### 3. Third Run - More Matches
```
1. Fetch "Matches - Upcoming"
2. Insert to DB
3. More matches added
```

---

## 🎯 Expected Results

**Before:** Only 5 sample matches
**After:** 20-50+ real matches from Cricbuzz API

### Your SQL Queries Will Show:
- ✅ Real team names (India, Australia, England, etc.)
- ✅ Real player data (Virat Kohli, Rohit Sharma, etc.)
- ✅ Real venues (Wankhede, MCG, Lord's, etc.)
- ✅ More rows in all queries!

---

## ⚠️ Important Notes

### API Rate Limits
- RapidAPI has rate limits (check your plan)
- If you get errors, wait a few minutes

### Data Quality
- API data may not have all fields populated
- Some matches may have NULL team_ids if teams aren't in DB yet
- Run Teams fetch before Matches for best results

### Database
- Uses your existing schema
- Safe - won't overwrite existing data
- Uses INSERT IGNORE and duplicate checks

---

## 🐛 Troubleshooting

### "No data returned from API"
- Check your RAPIDAPI_KEY in `.env`
- Verify your RapidAPI subscription is active
- Try a different endpoint

### "Error inserting..."
- Some data may be incomplete from API
- This is normal - the system skips invalid records
- Check the success count to see what was inserted

### "Teams not found"
- Fetch "Matches - Recent" first
- This will populate teams automatically

---

## 📈 Next Steps

After populating data:
1. Go to **SQL Practice Queries**
2. Run your 25 queries
3. See real, meaningful results!
4. Download CSV exports
5. Analyze trends and patterns

---

## 🎉 Summary

You now have:
- ✅ Working data ingestion
- ✅ Your original 25 SQL queries (no changes needed)
- ✅ Ability to populate real data from Cricbuzz
- ✅ Best of both worlds!

**Enjoy your fully populated cricket database!** 🏏
