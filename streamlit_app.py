import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse
import base64
import io
from PIL import Image

st.set_page_config(page_title="Victory Lab - Store Audit", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.main { background-color: #F2F2F2; }
h1, h2, h3 { color: #0093DD; }
.stButton>button { background-color: #0093DD; color: white; border-radius: 8px; padding: 10px 20px; }
.score-box { background: #E57373; padding: 20px; text-align: center; font-size: 32px; font-weight: bold; color: white; border-radius: 10px; }
.top-box { background: white; border: 2px solid #0093DD; border-radius: 10px; padding: 8px; text-align: center; }
.top-total { background: #0093DD; color: white; border-radius: 10px; padding: 8px; text-align: center; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

YOUR_WHATSAPP = "27813024555"

# ---------- PERSISTENT STORAGE - SCORES NEVER CLEAR ----------
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "info" not in st.session_state:
    st.session_state.info = {}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Score Sheet"

def save_answer(key, widget_key):
    if widget_key in st.session_state:
        st.session_state.answers[key] = st.session_state[widget_key]
def save_info(key, widget_key):
    if widget_key in st.session_state:
        st.session_state.info[key] = st.session_state[widget_key]
def get_answer(key):
    return st.session_state.answers.get(key, "--")
def get_info(key, default=""):
    return st.session_state.info.get(key, default)

# ---------- DATA ----------
GENERAL = ["Staff arrive on time?","Inspect is trading hours are visible on store window?","Is the store window clean?","Is the closing/opening procedure followed?","Doors Opening at right time?","Greeter at the doors?","Staff using the finger print reader?","Is staff consistently signing clocking register?","Count store float with manager on duty?","Is the float and Banking Register Updated?","Morning Meets - A. Are meetings performed and recorded?","Morning Meets - B. Is the Greeter Function Planned?","Morning Meets - C. Are Lunch Breaks Planned?","Morning Meets - D. Are associates signing attendance of Morning Meeting?","Store Vibe - Is the music on?","Store Vibe - Is the music playing from the Pc?","Store Vibe - Is the TV Playing?","Store Vibe - Is the content on the TV correct?","Cashdesk - Is the cashdesk area clean and neat?","Cashdesk - Are cables neat?","Cashdesk - Is the Team viewer running?","Cashdesk - Is the computer time and date correct?","Cashdesk - Is iconnect running?","Cashdesk - Is the store checking emails?"]
STOREOP = ["Confirm that store management perform regular spot checks on the fitting rooms.","Confirm that the fitting room is clean, eg no cluster, no tags, no hangers","Confirm if there are no expired Laybuys","Check if the stockroom is neat and tidy","Check if there is no stock lying around (if yes select no)","Check if fixtures / marketing / hangers are neatly separated","Is there core stock in the stockroom","Are boxes labelled neatly","Confirm that the Electric Board has electric switches properly labelled and that the board is fitted with a door. Confirm that electrical wiring / cabling is neatly and safely secured and there are no open light and plug fittings.","Plug points on Sales Floor to be fitted with plug cover","Confirm the store's air-conditioning system is fully operational and is serviced regularly as per the conditions of the Rental Contract.","Inspect if the store Has a fire extinguisher","Inspect if the fire extinguisher is compliant","Confirm if the store is performing security at Sales Floor","Confirm if the Alarm test is done as Per Procedure","Confirm if the store emails the OPS / AM the alarm reference for Alarm Test","Is store fridge working?","Is the store lights in order?"]
ADMIN = ["Is the store admin presentation neat and tidy","Are banking in order?","Are cards and cash balancing?","Is there payment wrong tenders? (Cash punched instead of Card etc)","Is the sales book in order?","Is all the manuals sales accounted for and processed correct?","Are the slips signed, dated and cancelled?","Is all petty cash slips in order?","Are all petty cash slips filed in sequence?","Is there reference numbers in petty cash slips?","Is the petty cash supporting dockets cancelled, dated and signed?","Is all refund slips in order?","Is all refund slips filed in a sequency?","Is there customer details and original slip accounted for?","Are the supporting refund slips signed, dated and cancelled?","Is the reference for the refunds attached?","Delivery - Inspect if there are no transfers older than a month","Delivery - Check if the transfer were followed up with stock department","Delivery - Check if delivery notes are accounted for: Transfer Numbers Confirmed, Signed and dated","Delivery - Confirm if stock is booked correctly","Delivery - Confirm if stock transfer is authorised with reference numbers"]
HANGER = ["Do associate know how to generate the stock report?","Do associate know how to count?","Do associate know how to categorise stock as per departments?","Confirm if counts are filed?","Confirm if counts are calculated correct?"]
MERCH = ["Check if the Store Windows are clean","Window visuals great - Displaying current season, trend and styles","Window banners - Up and correct","Nesting tables - Full and strong stock display - Current season / theme","Nesting tables - All Promo signage up and visible (If applicable)","Denim wall - Hanging denim running lowest price to highest price point","Denim Wall - Promo shelve talkers up and visible.","Denim Wall - Size stickers visible on all denim","T-Shirt Bay - T-Shirt boxes displaying newness - latest tee's","T-Shirt Bay - Attractive displays on peg wall (Shoes, Caps etc.)","T-Shirt Bay - Flat pack standard great with visible size stickers on all Tee's","T-Shirt Bay - Promotional signage / shelve talkers up and visible","Primo Wall - Primo shelve talkers up and visible","Primo Wall - All similar types/styles grouped together for ease of shopping","Primo Wall - Newness / Latest product highlighted central and prominent on wall","Sale rail - Well merchandised with all sale signage and hanger tags visible","Footwear stand / gondola - Fully merchandised with all footwear stock","Footwear stand / gondola - All footwear merchandised by brand and then by type","Footwear stand / gondola - All footwear signage up and visible","Accessories - All accessories merchandised neatly and grouped","General - All mannequins dressed properly and showing VL trends","General - Overall flat packing standards great","General - VL Stickers visible on all hangers","General - Cash desk clean with perfumes displayed neatly","General - Walls looking full with proper face outs (Outfits)"]
STAFF_TL = ["Dresses in line with VL Culture - Trend of product we sell","Displays positive, good energy every day","Reports daily figures every day","Gives feedback as per schedule on time","Approaches and assists customers - 2 metre rule","Actions / React to instructions / notes timously","Submits hanger count accurate and on time","Ensures store merchandise standards consistently great","Ensures accurate stock booking in","Assists in visuals and merchandising","Ensures admin done and up to date","Fully understands VL Culture document","Fully abides and live by VL Culture","Follows instructions immediately and properly","Ensures accurate cash ups","Follows up on any store issues","Counts accurately","Ensures customer service is consistent up to standard"]
STAFF_ASSOC = ["Arrives at work on time / 15-20 mins before trade time","Clocks in and out at all times","Dresses in line with VL Culture - Trend of product we sell","Displays positive, good energy","Displays interest in store performance","Adheres to greeter roster - Does greeter shifts","Approaches and assists customers - 2 metre rule","Talks to customers about in-store promo's","Pushes add-on sales","Productive throughout the day","Checks incoming stock correctly","Assists in visuals and merchandising","Assists in housekeeping and cleaning store daily","Fully understands VL Culture document","Fully abides and live by VL Culture","Follows instructions immediately and properly","Rings up sales accurately","Assists with counts","Counts accurately","Ensures store operates smooth in manager absence"]

# ---------- HELPERS ----------
def get_points(prefix, count):
    pts = 0
    for i in range(count):
        if st.session_state.answers.get(f"{prefix}_{i}") == "Yes":
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
    return {"General": (g_pts, 120, g_pct),"Store Operation": (s_pts, 90, s_pct),"Admin": (a_pts, 105, a_pct),"Hanger Count": (h_pts, 25, h_pct),"Merchandise": (m_pts, 125, m_pct),"Staff Review": (staff_pts, 190, staff_pct),"TOTAL": (total, 100, total),"TL": (tl_pts, 90, tl_pts/90*100),"Assoc": (assoc_pts, 100, assoc_pts/100*100)}

def show_top_scores():
    s = get_all_scores()
    st.markdown(f"### 🏪 Store: {get_info('store') or 'No Store Yet'} | Total: {s['TOTAL'][0]:.2f}%")
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    with c1: st.markdown(f"<div class='top-box'><b>General</b><br>{s['General'][0]}/{s['General'][1]}<br>{s['General'][2]:.1f}%</div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='top-box'><b>Store Op</b><br>{s['Store Operation'][0]}/{s['Store Operation'][1]}<br>{s['Store Operation'][2]:.1f}%</div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='top-box'><b>Admin</b><br>{s['Admin'][0]}/{s['Admin'][1]}<br>{s['Admin'][2]:.1f}%</div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='top-box'><b>Hanger</b><br>{s['Hanger Count'][0]}/{s['Hanger Count'][1]}<br>{s['Hanger Count'][2]:.1f}%</div>", unsafe_allow_html=True)
    with c5: st.markdown(f"<div class='top-box'><b>Merch</b><br>{s['Merchandise'][0]}/{s['Merchandise'][1]}<br>{s['Merchandise'][2]:.1f}%</div>", unsafe_allow_html=True)
    with c6: st.markdown(f"<div class='top-box'><b>Staff</b><br>{s['Staff Review'][0]}/{s['Staff Review'][1]}<br>{s['Staff Review'][2]:.1f}%</div>", unsafe_allow_html=True)
    with c7: st.markdown(f"<div class='top-total'>TOTAL<br>{s['TOTAL'][0]:.2f}%</div>", unsafe_allow_html=True)
    st.markdown("---")

def checklist(title, questions, prefix, max_points, show_comment=False):
    st.subheader(f"{title} ({max_points} points)")
    for i, q in enumerate(questions):
        key = f"{prefix}_{i}"; wkey = f"w_{prefix}_{i}"
        saved = get_answer(key)
        idx = ["--", "Yes", "No"].index(saved) if saved in ["--", "Yes", "No"] else 0
        col1, col2 = st.columns([3, 1])
        with col1: st.write(f"**{i+1}.** {q}")
        with col2: st.radio("Response", ["--", "Yes", "No"], index=idx, key=wkey, horizontal=True, label_visibility="collapsed", on_change=save_answer, args=(key, wkey))
        if show_comment:
            ckey = f"{prefix}_c_{i}"; cwkey = f"wc_{prefix}_{i}"
            st.text_input("Comment", value=st.session_state.answers.get(ckey, ""), key=cwkey, label_visibility="collapsed", placeholder="Comment", on_change=save_answer, args=(ckey, cwkey))
        st.divider()
    pts = get_points(prefix, len(questions)); pct = pts / max_points * 100 if max_points else 0
    st.success(f"{title} Score: {pts} / {max_points} - {pct:.2f}%")
    if st.button(f"✅ Finish {title} & View Score Sheet", use_container_width=True, key=f"finish_{prefix}"):
        st.session_state.page = "Score Sheet"; st.rerun()
    return pts, pct

def info_input(label, key, placeholder=""):
    wkey = f"info_w_{key}"
    st.text_input(label, value=get_info(key, ""), key=wkey, placeholder=placeholder, on_change=save_info, args=(key, wkey))

def build_full_csv():
    scores = get_all_scores()
    rows = []
    rows.append(["VICTORY LAB - STORE AUDIT - FULL SCORES"])
    rows.append(["Region", get_info("region")]); rows.append(["Store", get_info("store")]); rows.append(["Store Code", get_info("store_code")])
    rows.append(["Date of Com", get_info("date_com")]); rows.append(["DATE OF LAST AM CHECK", get_info("last_check")])
    rows.append(["Manager Name", get_info("manager")]); rows.append(["Area Manager", get_info("am")]); rows.append(["Auditor Name", get_info("auditor")])
    rows.append(["Date Complete", get_info("date_complete")]); rows.append(["SCORE OF LAST AM CHECK", get_info("last_score")]); rows.append([])
    rows.append(["CONTROL AREA", "SCORE", "MAX", "PERCENTAGE"])
    for area in ["General","Store Operation","Admin","Hanger Count","Merchandise","Staff Review"]:
        pts, mx, pct = scores[area]; rows.append([area, pts, mx, f"{pct:.2f}%"])
    rows.append(["TOTAL SCORE", f"{scores['TOTAL'][0]:.2f}%", "", ""])
    rows.append(["Team Leader Score", scores["TL"][0], 90, f"{scores['TL'][2]:.2f}%"]); rows.append(["Associate Score", scores["Assoc"][0], 100, f"{scores['Assoc'][2]:.2f}%"]); rows.append([])
    rows.append(["DETAILED ANSWERS"]); rows.append(["Section", "No", "Question", "Answer", "Points", "Comment"])
    def add_detail(section, questions, prefix):
        for i, q in enumerate(questions):
            ans = st.session_state.answers.get(f"{prefix}_{i}", "--"); pts = 5 if ans == "Yes" else 0; comment = st.session_state.answers.get(f"{prefix}_c_{i}", "")
            rows.append([section, i+1, q, ans, pts, comment])
    add_detail("General", GENERAL, "gen"); add_detail("Store Operation", STOREOP, "store"); add_detail("Admin", ADMIN, "admin"); add_detail("Hanger Count", HANGER, "hanger"); add_detail("Merchandise", MERCH, "merch"); add_detail("Staff Review - Team Leader", STAFF_TL, "staff_tl"); add_detail("Staff Review - Associate", STAFF_ASSOC, "staff_assoc")
    rows.append([]); rows.append(["Checker Name", get_info("checker_name")]); rows.append(["Checker Designation", get_info("checker_desig")])
    df = pd.DataFrame(rows); return df.to_csv(index=False, header=False).encode('utf-8')

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>VICTORY <span style='color:#2E9BD6;'>LAB</span></h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>STORE AUDIT</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        num = st.text_input("Employee Number", placeholder="2222222222"); pwd = st.text_input("Password", type="password", placeholder="********")
        if st.button("LOG IN", use_container_width=True):
            if num == "2222222222" and pwd == "123456":
                st.session_state.logged_in = True; st.rerun()
            else: st.error("Wrong number or password")
    st.stop()

# ---------- SIDEBAR - AI ASSISTANT AND FEEDBACK REMOVED ----------
st.sidebar.title("VICTORY LAB")
pages = ["Score Sheet", "General", "Store Operation", "Admin", "Hanger Count", "Merchandise", "Staff Review", "📸 Photo Check - Meta AI"]
if "nav" not in st.session_state: st.session_state.nav = st.session_state.page
choice = st.sidebar.radio("Go to:", pages, index=pages.index(st.session_state.page), key="nav")
st.session_state.page = choice
st.sidebar.markdown("---")
if st.sidebar.button("Log Out"): st.session_state.logged_in = False; st.rerun()
if st.sidebar.button("🔄 Start New Audit (Clear All)"): st.session_state.answers = {}; st.session_state.info = {}; st.rerun()

# ---------- TOP SCORE BAR ON EVERY PAGE ----------
show_top_scores()

# ---------- PAGES ----------
if choice == "Score Sheet":
    st.header("Score Sheet")
    col1, col2 = st.columns(2)
    with col1:
        info_input("Region", "region"); info_input("Store", "store"); info_input("Store Code", "store_code"); info_input("Date of Com", "date_com"); info_input("DATE OF LAST AM CHECK", "last_check")
    with col2:
        info_input("Manager Name", "manager"); info_input("Area Manager", "am"); info_input("Auditor Name", "auditor"); info_input("Date Complete", "date_complete"); info_input("SCORE OF LAST AM CHECK", "last_score")
    st.markdown("---")
    st.subheader("CONTROL AREA - SCORES")
    scores = get_all_scores()
    data = []
    for area in ["General","Store Operation","Admin","Hanger Count","Merchandise","Staff Review"]:
        pts, mx, pct = scores[area]; data.append([area, "High Risk", f"{pts} / {mx}", f"{pct:.2f}%"])
    df_summary = pd.DataFrame(data, columns=["CONTROL AREA", "RISK", "SCORE", "PERCENTAGE"])
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    total = scores["TOTAL"][0]
    st.markdown(f"<div class='score-box'>TOTAL SCORE: {total:.2f}%</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("DETAILS OF ASSOCIATE COMPLETING CHECK")
    info_input("NAME", "checker_name"); info_input("DESIGNATION", "checker_desig")
    st.caption("I, the above mentioned Line Manager, hereby confirm that I have completed this Checklist and the answers given are a true reflection of the stores risk.")
    csv_data = build_full_csv()
    st.download_button("📥 Download FULL Scores as CSV (All Control Areas + All Answers)", csv_data, "victory_lab_full_scores.csv", "text/csv", use_container_width=True)
    st.markdown("---")
    st.subheader("Send Score Sheet on WhatsApp")
    wa_text = f"VICTORY LAB - STORE AUDIT\nStore: {get_info('store')} ({get_info('store_code')})\nRegion: {get_info('region')}\nManager: {get_info('manager')}\nDate: {get_info('date_complete')}\n\nCONTROL AREA SCORES:\n"
    for area in ["General","Store Operation","Admin","Hanger Count","Merchandise","Staff Review"]:
        pts, mx, pct = scores[area]; wa_text += f"{area}: {pts}/{mx} = {pct:.2f}%\n"
    wa_text += f"\nTOTAL SCORE: {total:.2f}%\nChecker: {get_info('checker_name')}"
    wa_link = f"https://wa.me/{YOUR_WHATSAPP}?text={urllib.parse.quote(wa_text)}"
    st.link_button("📱 Send Score Sheet to WhatsApp (0813024555)", wa_link, use_container_width=True)
elif choice == "General": checklist("General", GENERAL, "gen", 120)
elif choice == "Store Operation": checklist("Store Operation", STOREOP, "store", 90)
elif choice == "Admin": checklist("Admin", ADMIN, "admin", 105)
elif choice == "Hanger Count":
    checklist("Hanger Count", HANGER, "hanger", 25, show_comment=True)
    st.markdown("### Hanger Count 2 - Conduct with Manager on duty")
    info_input("What is the overall variance for the store?", "variance")
    for k, lab in [("var_prev", "Is the variance that as what they reported in the previous week"), ("var_same", "Is the variance the same?")]:
        wkey = f"w_{k}"; saved = get_answer(k); idx = ["--", "Yes", "No"].index(saved) if saved in ["--", "Yes", "No"] else 0
        st.selectbox(lab, ["--", "Yes", "No"], index=idx, key=wkey, on_change=save_answer, args=(k, wkey))
    info_input("Is there any action required?", "var_action")
    if st.button("✅ Finish Hanger Count & View Score Sheet", use_container_width=True): st.session_state.page = "Score Sheet"; st.rerun()
elif choice == "Merchandise": checklist("Merchandising and Visual Standards", MERCH, "merch", 125)
elif choice == "Staff Review":
    st.header("Staff Review - Total 190 Points")
    info_input("Team Leader Name", "tl_name")
    tl_pts, tl_pct = checklist("Team Leader (18 Q = 90 pts)", STAFF_TL, "staff_tl", 90, show_comment=True)
    info_input("Associate Name", "assoc_name")
    assoc_pts, assoc_pct = checklist("Associate (20 Q = 100 pts)", STAFF_ASSOC, "staff_assoc", 100, show_comment=True)
    combined = tl_pts + assoc_pts
    st.success(f"Staff Review Total: {combined} / 190 - {combined/190*100:.2f}%")
    if st.button("✅ Finish Staff Review & View Score Sheet", use_container_width=True): st.session_state.page = "Score Sheet"; st.rerun()
elif choice == "📸 Photo Check - Meta AI":
    st.header("📸 Photo Check - Corrected by Meta AI (Llama)")
    check_type = st.selectbox("What are you checking?", ["Stockroom - Neat, labelled, no stock on floor","General - Window clean, Trading hours visible, Cashdesk clean","Merchandise - Nesting tables full, Denim wall lowest to highest, Mannequins dressed","Store Operation - Fitting rooms clean, No cluster, No tags","Admin - Admin presentation neat and tidy","Cashdesk - Clean, cables neat, perfumes displayed","Layby - Bags filed neatly, labels visible, no piling"])
    photo = st.file_uploader("Take / Upload Photo", type=["jpg", "jpeg", "png"]); store_name_photo = st.text_input("Store Name", key="photo_store")
    if photo:
        st.image(photo, caption="Your Photo", use_container_width=True)
        if st.button("🤖 Check With Meta AI", use_container_width=True):
            with st.spinner("Meta AI is checking your photo against VL Standard..."):
                try:
                    img_bytes = photo.getvalue(); b64 = base64.b64encode(img_bytes).decode("utf-8")
                    from groq import Groq; client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    prompt = f"You are Victory Lab Store Audit Expert. Standard: {check_type} Store: {store_name_photo}. Give VERDICT PASS/FAIL, SCORE /5, WHAT IS WRONG, HOW TO CORRECT IT NOW, HOW TO KEEP IT RIGHT. Short, direct."
                    response = client.chat.completions.create(model="meta-llama/llama-4-scout-17b-16e-instruct", messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}], max_tokens=1000)
                    result = response.choices[0].message.content; st.success("✅ Meta AI Check Complete"); st.markdown(result)
                    wa_text = f"VL PHOTO CHECK - {store_name_photo}\nStandard: {check_type}\n\n{result}"; wa_link = f"https://wa.me/{YOUR_WHATSAPP}?text={urllib.parse.quote(wa_text)}"; st.link_button("📱 Send This Photo Check to WhatsApp (0813024555)", wa_link, use_container_width=True)
                except Exception as e:
                    try:
                        import google.generativeai as genai; genai.configure(api_key=st.secrets["GEMINI_API_KEY"]); model2 = genai.GenerativeModel("gemini-1.5-flash"); img = Image.open(io.BytesIO(img_bytes)); resp = model2.generate_content([f"Check this photo against: {check_type}. Give VERDICT, SCORE /5, WHAT IS WRONG, HOW TO CORRECT IT NOW.", img]); st.success("✅ AI Check Complete"); st.markdown(resp.text)
                    except: st.error("No AI Key found. Add GROQ_API_KEY in Streamlit Secrets."); st.info(f"Error: {e}")
