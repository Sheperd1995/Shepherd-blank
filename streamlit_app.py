import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse

st.set_page_config(page_title="Victory Lab - Store Audit", layout="wide", initial_sidebar_state="expanded")

# ---------- STYLE ----------
st.markdown("""
<style>
.main { background-color: #F2F2F2; }
h1, h2, h3 { color: #0093DD; }
.stButton>button { background-color: #0093DD; color: white; border-radius: 8px; padding: 10px 20px; }
.score-box { background: #E57373; padding: 20px; text-align: center; font-size: 32px; font-weight: bold; color: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

YOUR_WHATSAPP = "27813024555"

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Score Sheet"

# ---------- DATA ----------
GENERAL = [
    "Staff arrive on time?",
    "Inspect is trading hours are visible on store window?",
    "Is the store window clean?",
    "Is the closing/opening procedure followed?",
    "Doors Opening at right time?",
    "Greeter at the doors?",
    "Staff using the finger print reader?",
    "Is staff consistently signing clocking register?",
    "Count store float with manager on duty?",
    "Is the float and Banking Register Updated?",
    "Morning Meets - A. Are meetings performed and recorded?",
    "Morning Meets - B. Is the Greeter Function Planned?",
    "Morning Meets - C. Are Lunch Breaks Planned?",
    "Morning Meets - D. Are associates signing attendance of Morning Meeting?",
    "Store Vibe - Is the music on?",
    "Store Vibe - Is the music playing from the Pc?",
    "Store Vibe - Is the TV Playing?",
    "Store Vibe - Is the content on the TV correct?",
    "Cashdesk - Is the cashdesk area clean and neat?",
    "Cashdesk - Are cables neat?",
    "Cashdesk - Is the Team viewer running?",
    "Cashdesk - Is the computer time and date correct?",
    "Cashdesk - Is iconnect running?",
    "Cashdesk - Is the store checking emails?",
]
STOREOP = [
    "Confirm that store management perform regular spot checks on the fitting rooms.",
    "Confirm that the fitting room is clean, eg no cluster, no tags, no hangers",
    "Confirm if there are no expired Laybuys",
    "Check if the stockroom is neat and tidy",
    "Check if there is no stock lying around (if yes select no)",
    "Check if fixtures / marketing / hangers are neatly separated",
    "Is there core stock in the stockroom",
    "Are boxes labelled neatly",
    "Confirm that the Electric Board has electric switches properly labelled and that the board is fitted with a door. Confirm that electrical wiring / cabling is neatly and safely secured and there are no open light and plug fittings.",
    "Plug points on Sales Floor to be fitted with plug cover",
    "Confirm the store's air-conditioning system is fully operational and is serviced regularly as per the conditions of the Rental Contract.",
    "Inspect if the store Has a fire extinguisher",
    "Inspect if the fire extinguisher is compliant",
    "Confirm if the store is performing security at Sales Floor",
    "Confirm if the Alarm test is done as Per Procedure",
    "Confirm if the store emails the OPS / AM the alarm reference for Alarm Test",
    "Is store fridge working?",
    "Is the store lights in order?",
]
ADMIN = [
    "Is the store admin presentation neat and tidy",
    "Are banking in order?",
    "Are cards and cash balancing?",
    "Is there payment wrong tenders? (Cash punched instead of Card etc)",
    "Is the sales book in order?",
    "Is all the manuals sales accounted for and processed correct?",
    "Are the slips signed, dated and cancelled?",
    "Is all petty cash slips in order?",
    "Are all petty cash slips filed in sequence?",
    "Is there reference numbers in petty cash slips?",
    "Is the petty cash supporting dockets cancelled, dated and signed?",
    "Is all refund slips in order?",
    "Is all refund slips filed in a sequency?",
    "Is there customer details and original slip accounted for?",
    "Are the supporting refund slips signed, dated and cancelled?",
    "Is the reference for the refunds attached?",
    "Delivery - Inspect if there are no transfers older than a month",
    "Delivery - Check if the transfer were followed up with stock department",
    "Delivery - Check if delivery notes are accounted for: Transfer Numbers Confirmed, Signed and dated",
    "Delivery - Confirm if stock is booked correctly",
    "Delivery - Confirm if stock transfer is authorised with reference numbers",
]
HANGER = [
    "Do associate know how to generate the stock report?",
    "Do associate know how to count?",
    "Do associate know how to categorise stock as per departments?",
    "Confirm if counts are filed?",
    "Confirm if counts are calculated correct?",
]
MERCH = [
    "Check if the Store Windows are clean",
    "Window visuals great - Displaying current season, trend and styles",
    "Window banners - Up and correct",
    "Nesting tables - Full and strong stock display - Current season / theme",
    "Nesting tables - All Promo signage up and visible (If applicable)",
    "Denim wall - Hanging denim running lowest price to highest price point",
    "Denim Wall - Promo shelve talkers up and visible.",
    "Denim Wall - Size stickers visible on all denim",
    "T-Shirt Bay - T-Shirt boxes displaying newness - latest tee's",
    "T-Shirt Bay - Attractive displays on peg wall (Shoes, Caps etc.)",
    "T-Shirt Bay - Flat pack standard great with visible size stickers on all Tee's",
    "T-Shirt Bay - Promotional signage / shelve talkers up and visible",
    "Primo Wall - Primo shelve talkers up and visible",
    "Primo Wall - All similar types/styles grouped together for ease of shopping",
    "Primo Wall - Newness / Latest product highlighted central and prominent on wall",
    "Sale rail - Well merchandised with all sale signage and hanger tags visible",
    "Footwear stand / gondola - Fully merchandised with all footwear stock",
    "Footwear stand / gondola - All footwear merchandised by brand and then by type",
    "Footwear stand / gondola - All footwear signage up and visible",
    "Accessories - All accessories merchandised neatly and grouped",
    "General - All mannequins dressed properly and showing VL trends",
    "General - Overall flat packing standards great",
    "General - VL Stickers visible on all hangers",
    "General - Cash desk clean with perfumes displayed neatly",
    "General - Walls looking full with proper face outs (Outfits)",
]
STAFF_TL = [
    "Dresses in line with VL Culture - Trend of product we sell",
    "Displays positive, good energy every day",
    "Reports daily figures every day",
    "Gives feedback as per schedule on time",
    "Approaches and assists customers - 2 metre rule",
    "Actions / React to instructions / notes timously",
    "Submits hanger count accurate and on time",
    "Ensures store merchandise standards consistently great",
    "Ensures accurate stock booking in",
    "Assists in visuals and merchandising",
    "Ensures admin done and up to date",
    "Fully understands VL Culture document",
    "Fully abides and live by VL Culture",
    "Follows instructions immediately and properly",
    "Ensures accurate cash ups",
    "Follows up on any store issues",
    "Counts accurately",
    "Ensures customer service is consistent up to standard",
]
STAFF_ASSOC = [
    "Arrives at work on time / 15-20 mins before trade time",
    "Clocks in and out at all times",
    "Dresses in line with VL Culture - Trend of product we sell",
    "Displays positive, good energy",
    "Displays interest in store performance",
    "Adheres to greeter roster - Does greeter shifts",
    "Approaches and assists customers - 2 metre rule",
    "Talks to customers about in-store promo's",
    "Pushes add-on sales",
    "Productive throughout the day",
    "Checks incoming stock correctly",
    "Assists in visuals and merchandising",
    "Assists in housekeeping and cleaning store daily",
    "Fully understands VL Culture document",
    "Fully abides and live by VL Culture",
    "Follows instructions immediately and properly",
    "Rings up sales accurately",
    "Assists with counts",
    "Counts accurately",
    "Ensures store operates smooth in manager absence",
]

# ---------- HELPERS ----------
def get_points(prefix, count):
    pts = 0
    for i in range(count):
        if st.session_state.get(f"{prefix}_{i}") == "Yes":
            pts += 5
    return pts

def get_all_scores():
    g_pts = get_points("gen", len(GENERAL)); g_pct = g_pts/120*100
    s_pts = get_points("store", len(STOREOP)); s_pct = s_pts/90*100
    a_pts = get_points("admin", len(ADMIN)); a_pct = a_pts/105*100
    h_pts = get_points("hanger", len(HANGER)); h_pct = h_pts/25*100
    m_pts = get_points("merch", len(MERCH)); m_pct = m_pts/125*100
    tl_pts = get_points("staff_tl", len(STAFF_TL))
    assoc_pts = get_points("staff_assoc", len(STAFF_ASSOC))
    staff_pts = tl_pts + assoc_pts; staff_pct = staff_pts/190*100
    total = (g_pct + s_pct + a_pct + h_pct + m_pct + staff_pct) / 6
    return {
        "General": (g_pts, 120, g_pct),
        "Store Operation": (s_pts, 90, s_pct),
        "Admin": (a_pts, 105, a_pct),
        "Hanger Count": (h_pts, 25, h_pct),
        "Merchandise": (m_pts, 125, m_pct),
        "Staff Review": (staff_pts, 190, staff_pct),
        "TOTAL": (total, 100, total),
        "TL": (tl_pts, 90, tl_pts/90*100),
        "Assoc": (assoc_pts, 100, assoc_pts/100*100),
    }

def checklist(title, questions, prefix, max_points, show_comment=False):
    st.subheader(f"{title} ({max_points} points)")
    for i, q in enumerate(questions):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{i+1}.** {q}")
        with col2:
            st.radio("Response", ["--", "Yes", "No"], key=f"{prefix}_{i}", horizontal=True, label_visibility="collapsed")
        if show_comment:
            st.text_input("Comment", key=f"{prefix}_c_{i}", label_visibility="collapsed", placeholder="Comment")
        st.divider()
    pts = get_points(prefix, len(questions))
    pct = pts / max_points * 100 if max_points else 0
    st.success(f"{title} Score: {pts} / {max_points} - {pct:.2f}%")
    if st.button(f"✅ Finish {title} & View Score Sheet", use_container_width=True, key=f"finish_{prefix}"):
        st.session_state.page = "Score Sheet"
        st.rerun()
    return pts, pct

def build_full_csv():
    scores = get_all_scores()
    rows = []
    rows.append(["VICTORY LAB - STORE AUDIT - FULL SCORES"])
    rows.append(["Region", st.session_state.get("region","")])
    rows.append(["Store", st.session_state.get("store","")])
    rows.append(["Store Code", st.session_state.get("store_code","")])
    rows.append(["Date of Com", str(st.session_state.get("date_com",""))])
    rows.append(["DATE OF LAST AM CHECK", str(st.session_state.get("last_check",""))])
    rows.append(["Manager Name", st.session_state.get("manager","")])
    rows.append(["Area Manager", st.session_state.get("am","")])
    rows.append(["Auditor Name", st.session_state.get("auditor","")])
    rows.append(["Date Complete", str(st.session_state.get("date_complete",""))])
    rows.append(["SCORE OF LAST AM CHECK", st.session_state.get("last_score","")])
    rows.append([])
    rows.append(["CONTROL AREA", "SCORE", "MAX", "PERCENTAGE"])
    for area in ["General","Store Operation","Admin","Hanger Count","Merchandise","Staff Review"]:
        pts, mx, pct = scores[area]
        rows.append([area, pts, mx, f"{pct:.2f}%"])
    rows.append(["TOTAL SCORE", f"{scores['TOTAL'][0]:.2f}%", "", ""])
    rows.append(["Team Leader Score", scores["TL"][0], 90, f"{scores['TL'][2]:.2f}%"])
    rows.append(["Associate Score", scores["Assoc"][0], 100, f"{scores['Assoc'][2]:.2f}%"])
    rows.append([])
    rows.append(["DETAILED ANSWERS"])
    rows.append(["Section", "No", "Question", "Answer", "Points", "Comment"])
    def add_detail(section, questions, prefix):
        for i, q in enumerate(questions):
            ans = st.session_state.get(f"{prefix}_{i}", "--")
            pts = 5 if ans == "Yes" else 0
            comment = st.session_state.get(f"{prefix}_c_{i}", "")
            rows.append([section, i+1, q, ans, pts, comment])
    add_detail("General", GENERAL, "gen")
    add_detail("Store Operation", STOREOP, "store")
    add_detail("Admin", ADMIN, "admin")
    add_detail("Hanger Count", HANGER, "hanger")
    add_detail("Merchandise", MERCH, "merch")
    add_detail("Staff Review - Team Leader", STAFF_TL, "staff_tl")
    add_detail("Staff Review - Associate", STAFF_ASSOC, "staff_assoc")
    rows.append([])
    rows.append(["Checker Name", st.session_state.get("checker_name","")])
    rows.append(["Checker Designation", st.session_state.get("checker_desig","")])
    df = pd.DataFrame(rows)
    return df.to_csv(index=False, header=False).encode('utf-8')

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>VICTORY <span style='color:#2E9BD6;'>LAB</span></h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>STORE AUDIT</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        num = st.text_input("Employee Number", placeholder="2222222222")
        pwd = st.text_input("Password", type="password", placeholder="********")
        if st.button("LOG IN", use_container_width=True):
            if num == "2222222222" and pwd == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong number or password")
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.title("VICTORY LAB")
pages = ["Score Sheet", "General", "Store Operation", "Admin", "Hanger Count", "Merchandise", "Staff Review", "Feedback", "AI Assistant"]
choice = st.sidebar.radio("Go to:", pages, index=pages.index(st.session_state.page))
st.session_state.page = choice
st.sidebar.markdown("---")
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()

# ---------- PAGES ----------
if choice == "Score Sheet":
    st.header("Score Sheet")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Region", key="region")
        st.text_input("Store", key="store")
        st.text_input("Store Code", key="store_code")
        st.date_input("Date of Com", date.today(), key="date_com")
        st.date_input("DATE OF LAST AM CHECK", date.today(), key="last_check")
    with col2:
        st.text_input("Manager Name", key="manager")
        st.text_input("Area Manager", key="am")
        st.text_input("Auditor Name", key="auditor")
        st.date_input("Date Complete", date.today(), key="date_complete")
        st.text_input("SCORE OF LAST AM CHECK", key="last_score")

    st.markdown("---")
    st.subheader("CONTROL AREA - SCORES")
    scores = get_all_scores()
    data = []
    for area in ["General","Store Operation","Admin","Hanger Count","Merchandise","Staff Review"]:
        pts, mx, pct = scores[area]
        data.append([area, "High Risk", f"{pts} / {mx}", f"{pct:.2f}%"])
    df_summary = pd.DataFrame(data, columns=["CONTROL AREA", "RISK", "SCORE", "PERCENTAGE"])
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    total = scores["TOTAL"][0]
    st.markdown(f"<div class='score-box'>TOTAL SCORE: {total:.2f}%</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("DETAILS OF ASSOCIATE COMPLETING CHECK")
    st.text_input("NAME", key="checker_name")
    st.text_input("DESIGNATION", key="checker_desig")
    st.caption("I, the above mentioned Line Manager, hereby confirm that I have completed this Checklist and the answers given are a true reflection of the stores risk.")

    csv_data = build_full_csv()
    st.download_button("📥 Download FULL Scores as CSV (All Control Areas + All Answers)", csv_data, "victory_lab_full_scores.csv", "text/csv", use_container_width=True)

    st.markdown("---")
    st.subheader("Send Score Sheet on WhatsApp")
    wa_text = f"VICTORY LAB - STORE AUDIT\nStore: {st.session_state.get('store','')} ({st.session_state.get('store_code','')})\nRegion: {st.session_state.get('region','')}\nManager: {st.session_state.get('manager','')}\nDate: {st.session_state.get('date_complete','')}\n\nCONTROL AREA SCORES:\n"
    for area in ["General","Store Operation","Admin","Hanger Count","Merchandise","Staff Review"]:
        pts, mx, pct = scores[area]
        wa_text += f"{area}: {pts}/{mx} = {pct:.2f}%\n"
    wa_text += f"\nTOTAL SCORE: {total:.2f}%\nChecker: {st.session_state.get('checker_name','')}"
    wa_link = f"https://wa.me/{YOUR_WHATSAPP}?text={urllib.parse.quote(wa_text)}"
    st.link_button("📱 Send Score Sheet to WhatsApp (0813024555)", wa_link, use_container_width=True)
    st.caption("This will open WhatsApp with all scores already typed. Just press Send.")

elif choice == "General":
    checklist("General", GENERAL, "gen", 120)
elif choice == "Store Operation":
    checklist("Store Operation", STOREOP, "store", 90)
elif choice == "Admin":
    checklist("Admin", ADMIN, "admin", 105)
elif choice == "Hanger Count":
    checklist("Hanger Count", HANGER, "hanger", 25, show_comment=True)
    st.markdown("### Hanger Count 2 - Conduct with Manager on duty")
    st.text_input("What is the overall variance for the store?", key="variance")
    st.selectbox("Is the variance that as what they reported in the previous week", ["--", "Yes", "No"], key="var_prev")
    st.selectbox("Is the variance the same?", ["--", "Yes", "No"], key="var_same")
    st.text_input("Is there any action required?", key="var_action")
    if st.button("✅ Finish Hanger Count & View Score Sheet", use_container_width=True):
        st.session_state.page = "Score Sheet"
        st.rerun()
elif choice == "Merchandise":
    checklist("Merchandising and Visual Standards", MERCH, "merch", 125)
elif choice == "Staff Review":
    st.header("Staff Review - Total 190 Points")
    st.text_input("Team Leader Name", key="tl_name")
    tl_pts, tl_pct = checklist("Team Leader (18 Q = 90 pts)", STAFF_TL, "staff_tl", 90, show_comment=True)
    st.text_input("Associate Name", key="assoc_name")
    assoc_pts, assoc_pct = checklist("Associate (20 Q = 100 pts)", STAFF_ASSOC, "staff_assoc", 100, show_comment=True)
    combined = tl_pts + assoc_pts
    st.success(f"Staff Review Total: {combined} / 190 - {combined/190*100:.2f}%")
    if st.button("✅ Finish Staff Review & View Score Sheet", use_container_width=True):
        st.session_state.page = "Score Sheet"
        st.rerun()

elif choice == "Feedback":
    st.header("Send Feedback on WhatsApp")
    st.write("Tell us what went wrong. It will open WhatsApp to 0813024555.")
    scores = get_all_scores()
    name = st.text_input("Your Name")
    store = st.text_input("Store Name / Store Code")
    message = st.text_area("Your Feedback / Problem", placeholder="Example: The General score is not updating...")
    if st.button("Send Feedback on WhatsApp", use_container_width=True):
        if not name or not message:
            st.error("Please fill in your name and feedback")
        else:
            full_text = f"Hi Victory Lab! Feedback from {name}\nStore: {store}\nScores - Total: {scores['TOTAL'][0]:.2f}% | General: {scores['General'][2]:.2f}% | Merch: {scores['Merchandise'][2]:.2f}% | Admin: {scores['Admin'][2]:.2f}%\n\n{message}"
            wa_link = f"https://wa.me/{YOUR_WHATSAPP}?text={urllib.parse.quote(full_text)}"
            st.success("Tap below to send on WhatsApp:")
            st.link_button("📱 Open WhatsApp & Send", wa_link, use_container_width=True)

elif choice == "AI Assistant":
    st.header("🤖 Victory Lab AI Assistant - Like Google AI Studio")
    st.write("Ask me anything about the audit. Example: What is hanger count? How do I improve Merchandise?")
    use_gemini = False
    model = None
    try:
        import google.generativeai as genai
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            use_gemini = True
    except:
        use_gemini = False
    if "chat" not in st.session_state:
        st.session_state.chat = [{"role": "assistant", "content": "Hi! I'm your Victory Lab Robot. Ask me about General, Admin, Merchandise, Hanger Count or Staff Review."}]
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    question = st.chat_input("Type your question here...")
    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        q = question.lower()
        if use_gemini and model:
            with st.spinner("Thinking..."):
                prompt = f"You are Victory Lab AI Assistant for a clothing store in South Africa. Help staff with store audits, customer service, merchandising. Be short, simple, friendly. Question: {question}"
                try:
                    resp = model.generate_content(prompt)
                    answer = resp.text
                except Exception as e:
                    answer = "Sorry, Gemini is not available now. Try again."
            st.session_state.chat.append({"role": "assistant", "content": answer})
            st.rerun()
        else:
            if "hanger" in q:
                answer = "Hanger Count = Count all stock by department. 5 questions, 25 points. Check: Can staff generate report? Can they count? Can they categorise? Are counts filed? Calculated correctly?"
            elif "general" in q:
                answer = "General has 24 questions, 120 points. Checks: Staff on time, Trading hours, Window clean, Opening procedure, Greeter, Fingerprint, Float, Morning Meeting, Music, TV, Cashdesk."
            elif "admin" in q:
                answer = "Admin has 21 questions, 105 points. Checks: Banking, Cards/cash balancing, Sales book, Petty cash filed in sequence, Refund slips signed, Transfers not older than a month."
            elif "merchandise" in q or "visual" in q:
                answer = "Merchandise has 25 questions, 125 points. Checks: Windows, Nesting tables, Denim wall lowest to highest, T-Shirt Bay, Primo Wall, Sale rail, Footwear, Accessories, Mannequins, VL Stickers."
            elif "score" in q or "total" in q:
                s = get_all_scores()
                answer = f"Your Total is average of 6 sections. Current: General {s['General'][2]:.2f}%, Store Op {s['Store Operation'][2]:.2f}%, Admin {s['Admin'][2]:.2f}%, Hanger {s['Hanger Count'][2]:.2f}%, Merch {s['Merchandise'][2]:.2f}%, Staff {s['Staff Review'][2]:.2f}% = TOTAL {s['TOTAL'][0]:.2f}%"
            elif "hello" in q or "hi" in q:
                answer = "Hello! How can I help you with your store audit today?"
            else:
                answer = f"I can help with General, Store Operation, Admin, Hanger Count, Merchandise, Staff Review, or Scores. Try: 'What is Hanger Count?' You asked: {question}"
            st.session_state.chat.append({"role": "assistant", "content": answer})
            st.rerun()
