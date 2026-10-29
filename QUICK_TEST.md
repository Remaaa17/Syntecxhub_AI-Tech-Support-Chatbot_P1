# Quick Test Instructions

## Server is Already Running
The server is running on **Terminal ID 18** at `http://localhost:5000`

Just refresh your browser to see the fixes!

---

## What Was Fixed

### 1. ✅ Blank Tabs Issue - FIXED
**Problem**: Analytics, History, and Settings tabs showed blank content
**Root Cause**: Missing `.hidden` CSS class
**Solution**: Added `.hidden { display: none !important; }` to CSS

### 2. ✅ Navigation Switching - FIXED
**Problem**: Tab switching used wrong view names
**Solution**: Added view name mapping (chat → chatView, analytics → analyticsView, etc.)

### 3. ✅ ROM vs RAM Query - ALREADY FIXED
**Problem**: "What is ROM?" returned RAM answer
**Solution**: Changed keyword matching to use word boundaries (`\b` regex pattern)

---

## Test It Now

### Test 1: Check All Tabs Work
1. Open `http://localhost:5000` in browser
2. Click **Chat** tab - Should show chat interface ✓
3. Click **Analytics** tab - Should show charts and stats ✓
4. Click **History** tab - Should show conversation history ✓
5. Click **Settings** tab - Should show settings and project info ✓

### Test 2: Test ROM vs RAM
1. Go to **Chat** tab
2. Type: **"What is RAM?"**
   - Expected: Answer about Random Access Memory ✓
3. Type: **"What is ROM?"**
   - Expected: Answer about Read-Only Memory (firmware, BIOS) ✓
   - Should NOT show RAM answer

### Test 3: Test Analytics Charts
1. Have a few conversations first (ask 3-5 questions)
2. Click **Analytics** tab
3. Should see:
   - Total Messages count (updates in real-time)
   - Resolved Issues count
   - Sentiment chart (doughnut)
   - Top Issues chart (bar)
   - Messages timeline (line)

### Test 4: Test History
1. After conversations, click **History** tab
2. Should see list of all conversations with:
   - Timestamps
   - Sentiment badges
   - Question/answer previews
   - Metadata
3. Click any conversation to see full details

### Test 5: Test AI Fallback (Unknown Questions)
These questions are NOT in knowledge base, should trigger Groq AI:
- "What is Docker?"
- "Explain microservices"
- "How do I use Kubernetes?"

Note: Requires Groq API key in `.env` file

---

## 5 Quick Test Questions

1. **"What is RAM?"** - Should explain Random Access Memory
2. **"What is ROM?"** - Should explain Read-Only Memory (NOT RAM!)
3. **"My WiFi is not working"** - Should give troubleshooting steps
4. **"Computer is running slow"** - Should give performance tips
5. **"What is Docker?"** - Should use AI fallback (if API key set)

---

## How to Check Browser Console

### Chrome/Edge:
1. Press `F12` or `Ctrl+Shift+I`
2. Click **Console** tab
3. Look for messages like:
   - "Switching to view: analyticsView"
   - "Showing view: analyticsView"
   - "Creating sentiment chart..."

### What You Should NOT See:
- ❌ "View not found" errors
- ❌ JavaScript errors
- ❌ Chart.js errors
- ❌ 404 errors

---

## Expected Behavior

### All Tabs Should:
- Switch smoothly without delay
- Show content immediately
- Not show blank screens
- Work on first click

### Chat Should:
- Accept messages
- Show typing indicator
- Display bot responses with metadata
- Track sentiment and confidence

### Analytics Should:
- Show real-time statistics
- Render all 3 charts
- Update when you refresh
- Handle empty state gracefully

### History Should:
- List all conversations
- Show timestamps
- Display sentiment badges
- Allow clicking to view details

### Settings Should:
- Show all project information
- Display feature list
- Show tech stack badges
- Allow saving preferences

---

## If Something Doesn't Work

### Refresh the page
- `Ctrl+F5` (hard refresh)
- Clears cache and reloads everything

### Check Console for errors
- Press `F12` → Console tab
- Look for red error messages

### Verify server is running
- Should see terminal with Flask running
- Should say "Running on http://127.0.0.1:5000"

### Check API key (for AI fallback)
- Open `.env` file
- Should have: `GROQ_API_KEY=gsk_...`

---

## All Changes Committed ✅

**Commit**: "Fix: Resolve blank tabs issue and improve navigation"

**Files Changed**:
- `static/css/style.css` - Added `.hidden` class
- `static/js/chat.js` - Fixed `switchView()` function
- `TEST_GUIDE.md` - Comprehensive test documentation
- `QUICK_TEST.md` - This file!

**GitHub**: Pushed to main branch ✓

---

## Summary

Everything is fixed and ready to test! Just refresh your browser at `http://localhost:5000` and try clicking through all the tabs. They should all work perfectly now.

The ROM vs RAM issue was already fixed in the previous changes (word boundary matching), so "What is ROM?" will now give you the correct answer about Read-Only Memory.

**Ready to test!** 🚀
